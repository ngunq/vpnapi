import json

from rest_framework import serializers
from django_celery_results.models import TaskResult


class TaskSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    class Meta:
        model = TaskResult
        fields = ['task_id', 'task_name', 'status', 'date_created', 'date_done', 'meta', 'result']

    def get_result(self, obj):
        return json.loads(obj.result)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not isinstance(ret.get('result'), dict):
            return ret
        result = ret.pop('result')

        for k, v in result.items():
            if k.startswith('exc') and k != 'exc_message':
                continue
            if k == 'exc_message':
                ret['error'] = v
            else:
                ret[k] = v

        return ret
