from django.db.models import Q


def filter_private_server_vm(queryset, params):
    qf = Q()
    q = params.get('search_query')
    if q != '':
        qf = qf | Q(ip__icontains=q)
        qf = qf | Q(name__icontains=q)
        qf = qf | Q(username__icontains=q)
        qf = qf | Q(hostname__icontains=q)
        qf = qf | Q(vm_name__icontains=q)
        qf = qf | Q(vm_bridge__icontains=q)
        qf = qf | Q(vm_template__icontains=q)

        qf = qf | Q(vm_id__icontains=q)
        qf = qf | Q(vm_socket__icontains=q)
        qf = qf | Q(vm_cores__icontains=q)
        qf = qf | Q(vm_disk__icontains=q)
        qf = qf | Q(vm_memory__icontains=q)

        qf = qf | Q(private_server__ip__icontains=q)
        qf = qf | Q(private_server__name__icontains=q)
        qf = qf | Q(private_server__username__icontains=q)
        qf = qf | Q(private_server__city__icontains=q)
        qf = qf | Q(private_server__country__icontains=q)
        qf = qf | Q(private_server__hostname__icontains=q)
        qf = qf | Q(private_server__proxmox_default_volume__icontains=q)
        qf = qf | Q(private_server__proxmox_node_name__icontains=q)
        qf = qf | Q(private_server__proxmox_default_disk__icontains=q)
        qf = qf | Q(private_server__provider__name__icontains=q)

    is_hardened = params.get('is_hardened_filter')
    if is_hardened is not None:
        qf = qf | Q(is_hardened=is_hardened)

    status = params.get('status_filter')
    if status is not None:
        qf = qf | Q(status=status)
    return queryset.filter(qf) if qf else queryset
