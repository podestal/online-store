from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as UserRetrieveSerializer
from .models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']

class UserRetrieveSerializer(UserRetrieveSerializer):
    class Meta(UserRetrieveSerializer.Meta):
        fields = ['id', 'username', 'email', 'first_name', 'last_name']