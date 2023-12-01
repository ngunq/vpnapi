from django.db.models import Q


def filter_provider(queryset, params):
    
    qf = Q()
    q = params.get('search_query')
    if q != '':
        qf = qf | Q(name__icontains=q)
    
    return queryset.filter(qf) if qf else queryset
