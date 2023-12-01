from django.db.models import Q


def filter_mgmt_whitelisted_ip(queryset, params):
    
    qf = Q()
    q = params.get('search_query')
    if q != '':
        qf = qf | Q(ip__icontains=q)
        qf = qf | Q(name__icontains=q)
    
    return queryset.filter(qf) if qf else queryset
