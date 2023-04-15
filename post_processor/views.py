import json
import logging
import os
import zipfile
from time import strftime
from wsgiref.util import FileWrapper

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Status
from .tasks import merge_results

logger = logging.getLogger(__name__)


@csrf_exempt
def test(request):
    return HttpResponse("Post Processor API Test Page.")


@csrf_exempt
def handle_request(request):
    """
    Route the request.
    """
    if request.method != 'POST':
        logger.info('Received invalid request.')
        return Response(status=status.HTTP_400_BAD_REQUEST)

    request_body = json.loads(request.body)

    run_ids_str = request_body.get('run_ids', None)

    if run_ids_str is None:
        print('Invalid run IDs.')
        return Response(status=status.HTTP_400_BAD_REQUEST)

    run_ids = run_ids_str.split()

    feature_table_paths, taxonomy_results_paths = get_file_paths(run_ids)
    timestamp = strftime('%Y%m%d-%H%M%S')

    try:
        worker = merge_results.delay(feature_table_paths, taxonomy_results_paths, timestamp)
    except ValueError as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    response = JsonResponse({'task_id': worker.task_id, 'timestamp': timestamp})

    response.headers['Access-Control-Allow-Origin'] = '*'

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
