from django.db.models import Q


def filter_private_server_user(queryset, params):
    
    qf = Q()
    q = params.get('search_query')
    if q != '':
        qf = qf | Q(user__username__icontains=q)
        qf = qf | Q(user__first_name__icontains=q)
        qf = qf | Q(user__last_name__icontains=q)
        qf = qf | Q(user__email__icontains=q)
        qf = qf | Q(private_server__ip__icontains=q)
        qf = qf | Q(private_server__name__icontains=q)
        qf = qf | Q(private_server__username__icontains=q)
        qf = qf | Q(private_server__city__icontains=q)
        qf = qf | Q(private_server__country__icontains=q)
        qf = qf | Q(private_server__provider__name__icontains=q)
    
    return queryset.filter(qf) if qf else queryset
