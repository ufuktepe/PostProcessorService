import json
import logging
import os
from time import strftime

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response

from config.settings import S3_MERGED_RESULTS_PATH
from .models import Status
from .tasks import create_results_csv
from .tasks import merge_results

logger = logging.getLogger(__name__)


@csrf_exempt
def test(request):
    return HttpResponse("Post Processor API Test Page.")


@csrf_exempt
def handle_request(request):
    """
    Create workers to merge the results and create the results csv file.
    """
    logger.debug(f'Received {request.method} request.')

    if request.method != 'POST':
        logger.info('Received invalid request.')
        return Response(status=status.HTTP_400_BAD_REQUEST)

    request_body = json.loads(request.body)
    run_ids_str = request_body.get('run_ids', None)

    if run_ids_str is None:
        logger.error(f'Missing run ID in request.')
        return Response(status=status.HTTP_400_BAD_REQUEST)

    run_ids = run_ids_str.split()

    feature_table_paths, taxonomy_results_paths = get_file_paths(run_ids)

    timestamp = strftime('%Y%m%d-%H%M%S')

    try:
        worker_merge_results = merge_results.delay(feature_table_paths, taxonomy_results_paths, timestamp)
    except ValueError as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    output_dir = os.path.join(S3_MERGED_RESULTS_PATH, timestamp + '-' + worker_merge_results.task_id)

    try:
        worker_create_results_csv = create_results_csv.delay(run_ids, output_dir)
    except ValueError as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response = JsonResponse({'merge_results_task_id': worker_merge_results.task_id,
                             'create_csv_task_id': worker_create_results_csv.task_id,
                             'timestamp': timestamp})

    # response.headers['Access-Control-Allow-Origin'] = '*'

    return response


def get_file_paths(run_ids):
    """
    Return file path strings for feature tables and taxonomy results
    """
    feature_table_paths = ''
    taxonomy_results_paths = ''

    for run_id in run_ids:
        try:
            run_status = Status.objects.get(pk=run_id)
        except Status.DoesNotExist:
            # Skip the run id
            continue

        # Build file paths
        output_path = run_status.output_path

        if not output_path:
            # Skip the run id
            continue

        feature_table_path = os.path.join(output_path, f'{run_id}_feature-table.qza')
        taxonomy_results_path = os.path.join(output_path, f'{run_id}_taxonomy.qza')

        # Verify that files exist
        if not os.path.isfile(feature_table_path):
            continue
        if not os.path.isfile(taxonomy_results_path):
            continue

        feature_table_paths += feature_table_path + ' '
        taxonomy_results_paths += taxonomy_results_path + ' '

    return feature_table_paths, taxonomy_results_paths
