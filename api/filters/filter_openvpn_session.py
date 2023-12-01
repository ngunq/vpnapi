from django.db.models import Q


def filter_openvpn_session(queryset, params):
    qf = Q()
    q = params.get('search_query')
    if q != '':
        qf = qf | Q(user__username__icontains=q)
        qf = qf | Q(user__firstname__icontains=q)
        qf = qf | Q(user__lastname__icontains=q)
        qf = qf | Q(user__email__icontains=q)

        qf = qf | Q(server__ip__icontains=q)
        qf = qf | Q(server__username__icontains=q)
        qf = qf | Q(server__city__icontains=q)
        qf = qf | Q(server__country__icontains=q)
        qf = qf | Q(server__provider__name__icontains=q)
        qf = qf | Q(server__name__icontains=q)
        qf = qf | Q(server__hostname__icontains=q)

    return queryset.filter(qf) if qf else queryset
