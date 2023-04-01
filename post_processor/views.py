import json

from django.http import JsonResponse, FileResponse
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .models import Study


@csrf_exempt
def handle_request(request):
    if request.method == 'GET':
        return get_visualization(request)
    elif request.method == 'POST':
        return update_database(request)

    return Response(status=status.HTTP_400_BAD_REQUEST)


def get_visualization(request):
    library_layout = request.GET.get('library_layout', None)
    library_source = request.GET.get('library_source', None)

    query_set = Study.objects.all()

    if library_layout:
        query_set = query_set.filter(library_layout=library_layout)
    if library_source:
        query_set = query_set.filter(library_source=library_source)

    for item in query_set:
        print(item.id)
        print(item.feature_table_path)

    qzv = open('/Users/burak/PycharmProjects/SimpleAPI/simple_api/api_app/taxonomy.qzv', 'rb')

    return FileResponse(qzv)


def update_database(request):
    studies = json.loads(request.body)

    for s in studies:
        if 'id' not in s:
            continue
        study = Study(id=s['id'],
                      library_layout=s.get('library_layout', None),
                      library_source=s.get('library_source', None),
                      feature_table_path=s.get('feature_table_path', None),
                      taxonomy_results_path=s.get('taxonomy_results_path', None))
        study.save()

    return Response(status=status.HTTP_201_CREATED)