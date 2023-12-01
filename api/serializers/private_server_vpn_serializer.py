from collections import OrderedDict

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from api.models import PrivateServerVPN, PrivateServerVM, Transport, VPNType
from .private_server_vm_serializer import PrivateServerVMRelatedSerializer


class PrivateServerVpnWireguardWriteSerializer(serializers.ModelSerializer):
    private_server_vm_id = serializers.UUIDField(write_only=True)
    private_ip = serializers.IPAddressField(protocol='IPv4', required=False)
    vpn_type = serializers.HiddenField(default=2)
    transport = serializers.HiddenField(default=2)

    class Meta:
        model = PrivateServerVPN
        fields = [
            'vpn_type',
            'transport',
            'port',
            'private_subnet',
            "private_subnet_mask",
            'private_ip',
            'interface_name',
            'private_server_vm_id',
            'dns',
            'keep_alive',
        ]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        private_server_vm_id = ret.pop('private_server_vm_id')
        private_server_vm = get_object_or_404(PrivateServerVM, id=private_server_vm_id)
        ret['private_server_vm'] = private_server_vm
        return ret


class PrivateServerVpnOpenvpnWriteSerializer(serializers.ModelSerializer):
    private_server_vm_id = serializers.UUIDField(write_only=True)
    vpn_type = serializers.HiddenField(default=1)
    tcp_port = serializers.IntegerField()
    udp_port = serializers.IntegerField()
    tcp_private_subnet = serializers.IPAddressField(protocol='IPv4')
    udp_private_subnet = serializers.IPAddressField(protocol='IPv4')
    tcp_private_subnet_mask = serializers.IntegerField()
    udp_private_subnet_mask = serializers.IntegerField()

    class Meta:
        model = PrivateServerVPN
        fields = [
            'vpn_type',
            'tcp_port',
            'udp_port',
            'tcp_private_subnet',
            'udp_private_subnet',
            "tcp_private_subnet_mask",
            "udp_private_subnet_mask",
            'private_server_vm_id',
            'dns',
        ]

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        private_server_vm_id = ret.pop('private_server_vm_id')
        private_server_vm = get_object_or_404(PrivateServerVM, id=private_server_vm_id)
        ret['private_server_vm'] = private_server_vm
        return ret

    def save(self, **kwargs):
        openvpn_data = self.validated_data.copy()
        self.validated_data['port'] = self.validated_data.pop('tcp_port')
        self.validated_data['private_subnet'] = self.validated_data.pop('tcp_private_subnet')
        self.validated_data['private_subnet_mask'] = self.validated_data.pop('tcp_private_subnet_mask')
        udp_port = self.validated_data.pop('udp_port')
        udp_private_subnet = self.validated_data.pop('udp_private_subnet')
        udp_private_subnet_mask = self.validated_data.pop('udp_private_subnet_mask')

        tcp = super().save(transport=Transport.TCP)
        self.instance = None
        self.validated_data['port'] = udp_port
        self.validated_data['private_subnet'] = udp_private_subnet
        self.validated_data['private_subnet_mask'] = udp_private_subnet_mask

        udp = super().save(transport=Transport.UDP)
        return tcp, udp, openvpn_data


class PrivateServerVpnReadSerializer(serializers.ModelSerializer):
    vpn_type = serializers.CharField(source='get_vpn_type_display', read_only=True)
    transport = serializers.CharField(source='get_transport_display', read_only=True)
    private_server_vm = PrivateServerVMRelatedSerializer(read_only=True)
    private_ip = serializers.IPAddressField(protocol='IPv4')
    id = serializers.UUIDField()

    class Meta:
        model = PrivateServerVPN
        fields = [
            'id',
            'port',
            'status',
            'config',
            'vpn_type',
            'transport',
            'private_subnet',
            "private_subnet_mask",
            'private_ip',
            'private_key',
            'public_key',
            'interface_name',
            'private_server_vm',
            'dns',
            'keep_alive',
        ]

    def to_representation(self, instance, related=False):
        ret = super().to_representation(instance)
        if related:
            return ret
        private_server_vm = ret.pop('private_server_vm')
        for k, v in private_server_vm.items():
            ret[k] = v

        return ret


class PrivateServerVpnRelatedReadSerializer(PrivateServerVpnReadSerializer):
    class Meta(PrivateServerVpnReadSerializer.Meta):
        pass

    def to_representation(self, instance, related=False):
        ret = super().to_representation(instance, related=True)
        private_server_vm = ret.pop('private_server_vm')
        ret = OrderedDict([("private_server_vpn_" + key, ret[key]) for key in ret])
        for k, v in private_server_vm.items():
            ret[k] = v

        return ret


class PrivateServerOpenVpnConfigSerializer(serializers.ModelSerializer):
    tcp_conf = serializers.SerializerMethodField()
    udp_conf = serializers.SerializerMethodField()

    class Meta:
        model = PrivateServerVM
        fields = ['tcp_conf', 'udp_conf']

    def get_tcp_conf(self, obj) -> str | None:
        vpn = get_object_or_404(obj.privateservervpn_set, vpn_type=VPNType.OPENVPN, transport=Transport.TCP)
        return vpn.config

    def get_udp_conf(self, obj) -> str | None:
        vpn = get_object_or_404(obj.privateservervpn_set, vpn_type=VPNType.OPENVPN, transport=Transport.UDP)
        return vpn.config
