from rest_framework import serializers

from .login_serializer import LoginSerializer


class OpenVpnLoginSerializer(LoginSerializer):
    secret = serializers.CharField()


class OpenVpnConnectSerializer(serializers.Serializer):
    secret = serializers.CharField()
    username = serializers.CharField()
    # server_ip = serializers.IPAddressField(protocol='IPv4')


class OpenvpnSessionsSerializer(serializers.Serializer):
    name = serializers.CharField()
    sessions = serializers.IntegerField()
