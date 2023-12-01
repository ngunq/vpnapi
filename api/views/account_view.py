from dj_rest_auth.registration.views import RegisterView
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


from api.filters import filter_account
from api.helpers import Paginator, sort_queryset, get_model_fields
from api.models import AppUser
from api.serializers import UserDetailsSerializer, AppUserQueryParamsSerializer, ObjectIdSerializer, \
    PasswordResetSerializer, AccountUpdateSerializer, SuspendClientSerializer, UpdateSessionsLimitSerializer
from api.tasks import handle_proxmox_start, handle_proxmox_stop, suspend_user


@extend_schema(
    responses=UserDetailsSerializer,
    request=None
)
@api_view(['GET'])
def get_user_details(request):
    user = request.user
    serializer = UserDetailsSerializer(user)
    return Response(serializer.data)


@extend_schema(
    responses=UserDetailsSerializer(many=True),
    request=AppUserQueryParamsSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def get_accounts(request):
    queryset = AppUser.objects.all()

    query_params = AppUserQueryParamsSerializer(data=request.data)
    query_params.is_valid(raise_exception=True)

    queryset = filter_account(queryset, query_params.data)
    fields = get_model_fields(AppUser)
    queryset = sort_queryset(queryset, query_params.data, fields, 'username')

    paginator = Paginator(queryset, query_params.data)
    queryset = paginator.paginate_queryset()

    serializer = UserDetailsSerializer(queryset, many=True)
    return Response(paginator.get_paginated_response(serializer.data))


@extend_schema(
    responses=UserDetailsSerializer,
    request=AccountUpdateSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_user(request):
    user = get_object_or_404(AppUser, id=request.data.get('id'))
    serializer = UserDetailsSerializer(user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    ret = UserDetailsSerializer(user)
    return Response(ret.data)


@extend_schema(
    responses=None,
    request=ObjectIdSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_account_status(request):
    user = get_object_or_404(AppUser, id=request.data.get('id'))
    user.is_superuser = not user.is_superuser
    user.save()
    admin = 'admin' if user.is_superuser else 'client'
    return Response(f'user is now {admin}')


@extend_schema(
    responses=None,
    request=PasswordResetSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def reset_password(request):
    serializer = PasswordResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(AppUser, id=serializer.data.get('id'))
    user.set_password(serializer.data.get('password'))
    user.save()
    return Response('password updated')


@extend_schema(
    responses=None,
    request=ObjectIdSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def delete_account(request):
    user = get_object_or_404(AppUser, id=request.data.get('id'))
    user.delete()
    return Response('user deleted')


@extend_schema(
    responses=None,
    request=SuspendClientSerializer
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
@transaction.atomic()
def suspend_account(request):
    serializer = SuspendClientSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(AppUser, id=serializer.data.get('id'))
    if not serializer.data.get('suspend'):
        user.is_suspended = False
        if user.private_server_vm:
            user.private_server_vm.is_enabled = True
            task = handle_proxmox_start.delay(user.private_server_vm.id)
        return Response('user is now not suspended' +
                        f' and the vm is being started {task.id}' if user.private_server_vm else '')

    user.is_suspended = True
    user.openvpn_sessions = 0
    user.wireguard_sessions = 0

    task1 = suspend_user.delay(user.id)
    res = 'suspend user task: ' + task1.id
    if user.private_server_vm:
        user.private_server_vm.is_enabled = False
        user.private_server_vm.save()
        task2 = handle_proxmox_stop.delay(user.private_server_vm.id)
        res = res + '\nvm stop task: ' + task2.id
    user.save()
    return Response('user suspended ' + res)


class RegisterViewV2(RegisterView):
    """
    register new user \n
    userType field is \n
    1: private_user \n
    2: public_user
    """

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    responses=None,
    request=UpdateSessionsLimitSerializer()
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_openvpn_session_limit(request):
    serializer = UpdateSessionsLimitSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(AppUser, id=serializer.data.get('id'))
    user.openvpn_sessions_limit = serializer.data.get('limit')
    user.save()
    return Response('ok')


@extend_schema(
    responses=None,
    request=UpdateSessionsLimitSerializer()
)
@api_view(['POST'])
@permission_classes([IsAdminUser])
def update_wireguard_session_limit(request):
    serializer = UpdateSessionsLimitSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(AppUser, id=serializer.data.get('id'))
    user.wireguard_sessions_limit = serializer.data.get('limit')
    user.save()
    return Response('ok')
