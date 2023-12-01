from django.db.models import F
from djangorestframework_camel_case.util import camel_to_underscore

from .exceptions import SortFieldError


def sort_queryset(queryset, params, fields, default_field):
    sort = params.get('sort')
    if sort != '':
        sort = camel_to_underscore(sort)
        if sort not in fields:
            raise SortFieldError(sort)
    else:
        sort = default_field

    sq = F(sort).desc() if params.get('is_desc') else F(sort).asc(nulls_last=True)
    queryset = queryset.order_by(sq)

    return queryset
