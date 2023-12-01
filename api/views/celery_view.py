from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from api.filters import filter_task
from api.helpers import Paginator, get_model_fields, sort_queryset
from api.serializers import ObjectIdSerializer, BaseQueryParamsSerializer, TaskSerializer, IdListSerializer, \
    TaskQueryParamsSerializer
from celery.result import AsyncResult
from django_celery_results.models import TaskResult


@extend_schema(
    responses=TaskSerializer(many=True),
    request=IdListSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_task_status(request):
    serializer = IdListSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    tasks = TaskResult.objects.filter(task_id__in=serializer.data.get('ids'))
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@extend_schema(
    request=TaskQueryParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_tasks_list(request):
    # Assuming you have a custom task table in your MySQL database where Celery stores results
    # Replace 'your_task_table' with the actual table name
    queryset = TaskResult.objects.all()

    query_params = TaskQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_task(queryset, query_params.data)
    fields = get_model_fields(TaskResult)
    queryset = sort_queryset(queryset, query_params.data, fields, 'date_done')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = TaskSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)
