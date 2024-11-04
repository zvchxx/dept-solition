from rest_framework import serializers

from user.models import UserModel

from rest_framework.validators import UniqueValidator


class RegisterSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(max_length=20, validators=[
        UniqueValidator(queryset=UserModel.objects.all(), message='This phone number is already registered')
    ])


    class Meta:
        model = UserModel
        fields = ['username', 'phone_number', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    

    def validate_phone_number(self, phone_number: str):
        phone_number = phone_number.strip()
        if not phone_number.startswith('+998'):
            raise serializers.ValidationError("Invalid phone number format. It should start with '+998'.")
        if not phone_number[4:].isdigit():
            raise serializers.ValidationError("Invalid phone number format. It should contain only digits only.")
        return phone_number
    

    def create(self, validated_data):
        validated_data.pop('confirm_password')  
        user = UserModel.objects.create_user(**validated_data)  
        return user
    
    
class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
