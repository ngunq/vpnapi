import logging

from django.conf import settings
from django.db import transaction
from django.db.models import F
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.models import AppUser, PublicServer, PublicServerOpenvpnSession, PrivateServerVmOpenvpnSession, \
    PrivateServerVM
from api.serializers import OpenVpnLoginSerializer, OpenVpnConnectSerializer

logger = logging.getLogger('openvpn')


@extend_schema(
    request=OpenVpnLoginSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([])
@transaction.atomic
def open_vpn_login(request):
    serializer = OpenVpnLoginSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    if serializer.data.get('secret') != settings.OPENVPN_SECRET:
        return Response('secret error', status=status.HTTP_400_BAD_REQUEST)

    user: AppUser = AppUser.objects.select_for_update().get(username=serializer.data.get('username'))

    # if user.openvpn_sessions >= user.openvpn_sessions_limit:
    #     return Response('sessions limit exceeded', status=status.HTTP_400_BAD_REQUEST)
    # user.openvpn_sessions = F('openvpn_sessions') + 1
    user.save()
    return Response('ok')


@extend_schema(
    request=OpenVpnConnectSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([])
@transaction.atomic
def open_vpn_connect(request):
    logger.info('openvpn connect requested')
    serializer = OpenVpnConnectSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as e:
        logger.error(e)
        raise
    if serializer.data.get('secret') != settings.OPENVPN_SECRET:
        logger.error('secret error')
        return Response('secret error', status=status.HTTP_400_BAD_REQUEST)

    try:
        user: AppUser = AppUser.objects.select_for_update().get(username=serializer.data.get('username'))
    except AppUser.DoesNotExist:
        logger.error(f'invalid username')
        return Response('invalid username', status=status.HTTP_400_BAD_REQUEST)

    if user.is_suspended:
        return Response('user is suspended', status=status.HTTP_400_BAD_REQUEST)

    server = None
    found = 0
    forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forward_for:
        ip = forward_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    # ip = request.data.get('server_ip')
    logger.info(f'calling openvpn connect from {ip}')
    try:
        server = PublicServer.objects.get(ip=ip)
    except PublicServer.DoesNotExist:
        pass
    else:
        found = 1

    try:
        server = PrivateServerVM.objects.get(ip=ip)
    except PrivateServerVM.DoesNotExist:
        pass
    else:
        found = 2

    if server is None:
        logger.error(f'no server found with ip: {ip}')
        return Response('invalid ip', status=status.HTTP_400_BAD_REQUEST)

    if user.openvpn_sessions >= user.openvpn_sessions_limit:
        logger.error(f'session limit exceeded for user {user.username}')
        return Response('sessions limit exceeded', status=status.HTTP_400_BAD_REQUEST)
    logger.info(f'current sessions before connection: {user.openvpn_sessions}')
    user.openvpn_sessions += 1
    user.save()
    user.refresh_from_db()
    if found == 1:
        qs = PublicServerOpenvpnSession.objects.all()
        session = qs.create(server=server, user=user)
        session.save()
    else:
        qs = PrivateServerVmOpenvpnSession.objects.all()
        session = qs.create(server_vm=server, user=user)
        session.save()

    
    logger.info(f'openvpn connect success and row created in db: current user_sessions: {user.openvpn_sessions}')
    return Response('ok')


@extend_schema(
    request=OpenVpnConnectSerializer,
    responses=None
)
@api_view(['POST'])
@permission_classes([])
@transaction.atomic
def open_vpn_disconnect(request):
    logger.info('openvpn disconnect requested')
    serializer = OpenVpnConnectSerializer(data=request.data)
    try:
        serializer.is_valid(raise_exception=True)
    except ValidationError as e:
        logger.error(e)
        raise
    if serializer.data.get('secret') != settings.OPENVPN_SECRET:
        logger.error('secret error')
        return Response('secret error', status=status.HTTP_400_BAD_REQUEST)

    try:
        user: AppUser = AppUser.objects.select_for_update().get(username=serializer.data.get('username'))
    except AppUser.DoesNotExist:
        logger.error('invalid username')
        return Response('invalid username', status=status.HTTP_400_BAD_REQUEST)

    server = None
    found = 0
    forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forward_for:
        ip = forward_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    logger.info(f'calling openvpn disconnect from {ip}')
    try:
        server = PublicServer.objects.get(ip=ip)
    except PublicServer.DoesNotExist:
        pass
    else:
        found = 1

    try:
        server = PrivateServerVM.objects.get(ip=ip)
    except PrivateServerVM.DoesNotExist:
        pass
    else:
        found = 2

    if server is None:
        logger.error(f'no server found with ip: {ip}')
        return Response('invalid ip', status=status.HTTP_400_BAD_REQUEST)

    if found == 1:
        qs = PublicServerOpenvpnSession.objects.all()
        session = qs.filter(server=server, user=user).first()
        session.delete()
    else:
        qs = PrivateServerVmOpenvpnSession.objects.all()
        session = qs.filter(server_vm=server, user=user).first()
        session.delete()

    
    if user.openvpn_sessions == 0:
        logger.error("user don't have sessions")
        return Response('no sessions', status=status.HTTP_400_BAD_REQUEST)
    user.openvpn_sessions = F('openvpn_sessions') - 1
    user.save()

    logger.info(f'disconnect sucess user {user.username} now have: {user.openvpn_sessions}')
    return Response('ok')
