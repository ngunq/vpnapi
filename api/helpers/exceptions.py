import logging

from rest_framework.exceptions import APIException

logger = logging.getLogger('ansible')


class SortFieldError(APIException):
    def __init__(self, field):
        self.default_code = 400
        self.default_detail = f'{field} is not a valid sort field'
        super().__init__()


class AnsibleError(APIException):
    def __init__(self, e=None):
        self.default_code = 400
        self.default_detail = f'ansible failed: {e}'
        logger.error(self.default_detail)
        super().__init__()
