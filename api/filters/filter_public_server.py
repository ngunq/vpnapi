from django.db.models import Q


def filter_public_server(queryset, params):
    qf = Q()
    q = params.get('search_query')
    if q != '':
        qf = qf | Q(ip__icontains=q)
        qf = qf | Q(username__icontains=q)
        qf = qf | Q(city__icontains=q)
        qf = qf | Q(country__icontains=q)
        qf = qf | Q(provider__name__icontains=q)
        qf = qf | Q(name__icontains=q)
        qf = qf | Q(hostname__icontains=q)

    provider = params.get('provider_filter')
    if provider != '':
        qf = qf | Q(provider__name__icontains=provider)

    ip = params.get('ip_filter')
    if ip != '':
        qf = qf | Q(ip__icontains=ip)

    is_hardened = params.get('is_hardened_filter')
    if is_hardened is not None:
        qf = qf | Q(is_hardened=is_hardened)

    status = params.get('status_filter')
    if status is not None:
        qf = qf | Q(status=status)

    return queryset.filter(qf) if qf else queryset
