from django.core.files import File
from django.db import transaction
from django.http import Http404
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from api.filters import filter_private_server_client
from api.helpers import get_model_fields, sort_queryset, Paginator
from api.helpers.exceptions import AnsibleError
from api.models import PrivateServerVpnWireguardClient, AppUser, ServerType
from api.serializers import PrivateServerVpnWireguardClientSerializer, ObjectIdSerializer, BaseQueryParamsSerializer, PrivateServerClientsQueryParamsSerializer
from api.tasks import handle_wireguard_add_client


class PrivateServerClientsViewSet(ViewSet):
    serializer_class = PrivateServerVpnWireguardClientSerializer
    queryset = PrivateServerVpnWireguardClient.objects.all()

    def get_object(self, pk):
        return get_object_or_404(self.queryset, pk=pk)

    @transaction.atomic()
    @action(methods=['post'], detail=False, url_path='Update')
    @permission_classes([IsAdminUser])
    def _update(self, request):
        user: AppUser = get_object_or_404(AppUser, pk=request.data.get('client_id'))
        if user.wireguard_sessions >= user.wireguard_sessions_limit:
            raise AnsibleError('sessions limit exceeded')

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        new_private_vm = instance.private_server_vpn.private_server_vm
        cur = self.queryset.filter(client=user).first()
        if cur is not None and cur.private_server_vpn.private_server_vm != new_private_vm:
            raise AnsibleError('you are already connected to another vm')
        task = handle_wireguard_add_client.delay(
            instance.id,
            ServerType.PRIVATE,
            user.id,
            client_username=request.user.username,
            port=instance.private_server_vpn.port,
            interface_name=instance.private_server_vpn.interface_name,
            dns=instance.private_server_vpn.dns,
            private_ip=instance.private_server_vpn.private_ip,
            private_subnet_mask=instance.private_server_vpn.private_subnet_mask,
            keep_alive=instance.private_server_vpn.keep_alive,
            username=instance.private_server_vpn.private_server_vm.username,
            host=instance.private_server_vpn.private_server_vm.ip,
            password=instance.private_server_vpn.private_server_vm.password,
            hostname=instance.private_server_vpn.private_server_vm.hostname
        )

        return Response(f'{task.id}')

    @extend_schema(
        request=PrivateServerClientsQueryParamsSerializer
    )
    @action(methods=['post'], detail=False, url_path='GetALL')
    def get_all(self, request):
        query_params = PrivateServerClientsQueryParamsSerializer(data=request.data)
        query_params.is_valid(raise_exception=True)

        queryset = self.queryset
        queryset = filter_private_server_client(self.queryset, query_params.data)
        fields = get_model_fields(PrivateServerVpnWireguardClient)
        queryset = sort_queryset(queryset, query_params.data, fields, 'id')

        paginator = Paginator(queryset, query_params.data)
        queryset = paginator.paginate_queryset()

        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(paginator.get_paginated_response(serializer.data), status=status.HTTP_200_OK)

    @extend_schema(
        request=ObjectIdSerializer,
        responses=None
    )
    @action(methods=['post'], detail=False, url_path='Delete')
    @permission_classes([IsAdminUser])
    def delete(self, request):
        obj = self.get_object(request.data.get('id'))
        obj.delete()
        user = request.user
        user.wireguard_sessions -= 1
        user.save()
        return Response('record deleted')

    @extend_schema(
        request=inline_serializer('private_client_config_serializer', fields={'client_id': serializers.UUIDField(),
                                                                      'vm_id': serializers.UUIDField()}),
        responses=inline_serializer('private_client_config_result_serializer', fields={'config': serializers.CharField(),
                                                                               'qr_file': serializers.CharField()}),
    )
    @action(methods=['post'], detail=False, url_path='GetClientConfig', permission_classes=[])
    def get_client_config(self, request):
        obj = self.queryset.filter(private_server_vpn__private_server_vm=request.data.get('vm_id'),
                                   client__id=request.data.get('client_id')).first()
        if obj is None:
            raise Http404
        # try:
        #     config = request.build_absolute_uri(obj.config)
        #     qr_file = request.build_absolute_uri(obj.qr_file)
        # except ValueError as e:
        #     return Response(f'config or qr not found {e}', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'config': obj.config, 'qr_file': obj.qr_file})
