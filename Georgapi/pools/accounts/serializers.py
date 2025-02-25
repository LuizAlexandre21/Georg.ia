from rest_framework import serializers
from .models import User_Info

class UserSerializer(serializers.ModelSerializer):
    # Campo password configurado como write_only para evitar que seja retornado na resposta
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User_Info 
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'address',
            'date_of_birth',
            'created_at',
            'updated_at',
            'is_active',
            'is_staff',
            'password'
        ]
        read_only_fields = ['created_at', 'updated_at', 'is_active', 'is_staff']

    def create(self, validated_data):
        # Cria o usuário utilizando o método create_user, que deve criptografar a senha
        user = User_Info.objects.create_user(
            username = validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            address=validated_data.get('address', ''),
            date_of_birth=validated_data.get('date_of_birth', None),
        )
        return user
