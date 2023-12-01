from django.db.models import Q


def filter_private_server_vpn(queryset, params):
    qf = Q()
    q = params.get('search_query')
    if q != '':
        qf = qf | Q(private_ip__icontains=q)
        qf = qf | Q(interface_name__icontains=q)
        qf = qf | Q(private_subnet__icontains=q)
        qf = qf | Q(private_subnet_mask__icontains=q)
        qf = qf | Q(private_ip__icontains=q)
        qf = qf | Q(dns__icontains=q)

        qf = qf | Q(port__icontains=q)
        qf = qf | Q(keep_alive__icontains=q)

        qf = qf | Q(private_server_vm__ip__icontains=q)
        qf = qf | Q(private_server_vm__name__icontains=q)
        qf = qf | Q(private_server_vm__username__icontains=q)
        qf = qf | Q(private_server_vm__hostname__icontains=q)
        qf = qf | Q(private_server_vm__vm_name__icontains=q)
        qf = qf | Q(private_server_vm__vm_bridge__icontains=q)
        qf = qf | Q(private_server_vm__vm_template__icontains=q)

        qf = qf | Q(private_server_vm__vm_id__icontains=q)
        qf = qf | Q(private_server_vm__vm_socket__icontains=q)
        qf = qf | Q(private_server_vm__vm_cores__icontains=q)
        qf = qf | Q(private_server_vm__vm_disk__icontains=q)
        qf = qf | Q(private_server_vm__vm_memory__icontains=q)

    vpn_type_filter = params.get('vpn_type_filter')
    if vpn_type_filter is not None and vpn_type_filter != -1:
        qf = qf | Q(vpn_type=vpn_type_filter)

    transport_filter = params.get('transport_filter')
    if transport_filter is not None and transport_filter != -1:
        qf = qf | Q(transport=transport_filter)

    status = params.get('status_filter')
    if status is not None:
        qf = qf | Q(status=status)

    return queryset.filter(qf) if qf else queryset
