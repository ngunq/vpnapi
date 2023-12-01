from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import camelize
from rest_framework.renderers import JSONRenderer


class ApiRenderer(JSONRenderer):
    json_underscoreize = api_settings.JSON_UNDERSCOREIZE

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = camelize(data, **self.json_underscoreize)

        res = {}
        status_code = renderer_context['response'].status_code

        path = renderer_context['request'].path
        path = path.lower()

        if str(status_code).startswith('2'):
            res['success'] = data
        else:
            res['fail'] = data
            renderer_context['response'].\
                status_code = 200 if status_code != 401 and 'login' not in path else status_code

        return super().render(res, accepted_media_type, renderer_context)
