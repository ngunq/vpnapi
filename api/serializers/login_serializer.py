# from dj_rest_auth import serializers
from dj_rest_auth.serializers import LoginSerializer as RestLogin


class LoginSerializer(RestLogin):
    email = ''
