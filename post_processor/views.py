import json
import os
import zipfile
from wsgiref.util import FileWrapper

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Study
from .tasks import merge_results


@csrf_exempt
def handle_request(request):
    """
    Route the request.
    """
    if request.method == 'GET':
        return get_visualization(request)
    elif request.method == 'POST':
        return update_database(request)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def get_visualization(request):
    """
    Return merged visualization files.
    """
    library_layout = request.GET.get('library_layout', None)

    studies = Study.objects.all()

    # Filter studies
    if library_layout:
        studies = studies.filter(library_layout=library_layout.lower())

    feature_table_paths, taxonomy_results_paths = get_file_paths(studies)

    try:
        worker = merge_results.delay(feature_table_paths, taxonomy_results_paths)
    except ValueError as e:
        return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({'task_id': worker.task_id})


def get_results(request):
    """
    Zip the results in the temp folder and return the zip file.
    """
    output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp')

    zip_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'results.zip')
    with zipfile.ZipFile(zip_path, mode="w") as archive:
        for root, sub_dirs, file_names in os.walk(output_dir):
            for file_name in file_names:
                archive.write(os.path.join(root, file_name), arcname=file_name)

    response = HttpResponse(FileWrapper(open(zip_path, 'rb')), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="results.zip"'

    return response


@api_view(('POST',))
def update_database(request):
    """
    Extract the studies from the request and save them in the database.
    """
    studies = json.loads(request.body)

    for s in studies:
        if 'id' not in s:
            continue

        study = Study(id=s['id'],
                      library_layout=s.get('library_layout', None),
                      feature_table_path=s.get('feature_table_path', None),
                      taxonomy_results_path=s.get('taxonomy_results_path', None))
        study.save()

    return Response(status=status.HTTP_201_CREATED)


def get_file_paths(studies):
    """
    Return file path strings for feature tables and taxonomy results
    """
    feature_table_paths = ''
    taxonomy_results_paths = ''

    # Build paths for feature tables and taxonomy results.
    for study in studies:
        feature_table_paths += study.feature_table_path + ' '
        taxonomy_results_paths += study.taxonomy_results_path + ' '

    return feature_table_paths, taxonomy_results_paths
