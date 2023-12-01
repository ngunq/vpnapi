from django.db.models import Q


def filter_account(queryset, params):
    qf = Q()
    q = params.get('search_query')
    if q != '':
        qf = qf | Q(username__icontains=q)
        qf = qf | Q(firstname__icontains=q)
        qf = qf | Q(lastname__icontains=q)
        qf = qf | Q(email__icontains=q)

    user_type_filter = params.get('user_type_filter')
    if user_type_filter is not None and user_type_filter != -1:
        qf = qf | Q(transport=user_type_filter)
    return queryset.filter(qf) if qf else queryset
