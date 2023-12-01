from django.db.models import Q


def filter_proxmox_subnet(queryset, params):
    qf = Q()
    q = params.get('search_query')
    if q != '':
        # qf = qf | Q(pr_subnet__icontains=q)
        qf = qf | Q(mask__icontains=q)
        qf = qf | Q(gateway__icontains=q)

        qf = qf | Q(private_serverip__icontains=q)
        qf = qf | Q(private_servername__icontains=q)
        qf = qf | Q(private_serverusername__icontains=q)
        qf = qf | Q(private_servercity__icontains=q)
        qf = qf | Q(private_servercountry__icontains=q)
        qf = qf | Q(private_serverhostname__icontains=q)
        qf = qf | Q(private_serverproxmox_default_volume__icontains=q)
        qf = qf | Q(private_serverproxmox_node_name__icontains=q)
        qf = qf | Q(private_serverproxmox_default_disk__icontains=q)

    return queryset.filter(qf) if qf else queryset
