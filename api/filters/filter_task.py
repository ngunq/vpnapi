from django.db.models import Q


def filter_task(queryset, params):
    qf = Q()
    q = params.get('search_query')
    if q != '':
        qf = qf | Q(status__icontains=q)
        qf = qf | Q(task_name__icontains=q)

    date_filter = params.get('date_filter')
    if date_filter is not None:
        qf = qf | Q(date_created__date=date_filter)

    return queryset.filter(qf) if qf else queryset
