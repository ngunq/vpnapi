from django.db.models import Q


def filter_public_server_client(queryset, params):
    qf = Q()
    q = params.get('search_query')
    if q != '':
        qf = qf | Q(client__username__icontains=q)
        qf = qf | Q(client__first_name__icontains=q)
        qf = qf | Q(client__last_name__icontains=q)
        qf = qf | Q(client__email__icontains=q)

        qf = qf | Q(public_server_vpn__private_ip__icontains=q)
        qf = qf | Q(public_server_vpn__interface_name__icontains=q)
        qf = qf | Q(public_server_vpn__private_subnet__icontains=q)
        qf = qf | Q(public_server_vpn__private_subnet_mask__icontains=q)
        qf = qf | Q(public_server_vpn__private_ip__icontains=q)
        qf = qf | Q(public_server_vpn__dns__icontains=q)
        qf = qf | Q(public_server_vpn__port__icontains=q)
        qf = qf | Q(public_server_vpn__keep_alive__icontains=q)

    user_id = params.get('user_id')
    if user_id is not None:
        qf = qf | Q(client=user_id)
    
    server_id = params.get('server_id')
    if server_id is not None:
        qf = qf | Q(public_server_vpn__public_server=server_id)
    return queryset.filter(qf) if qf else queryset
