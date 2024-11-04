from django.shortcuts import render

from rest_framework.response import Response

from rest_framework import generics, status

from rest_framework.views import APIView

from django.contrib.auth import authenticate

from user.models import UserModel

from rest_framework.permissions import AllowAny

from user.serializers import LoginSerializers, RegisterSerializers

from rest_framework.authtoken.models import Token 


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializers
    queryset = UserModel.objects.all()
    permission_classes = [AllowAny] 


class LoginView(APIView):
    serializer_class = LoginSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            response = {
                "token": token.key,
                "username": user.username,
                "phone_number": user.phone_number
            }
            return Response(response, status=status.HTTP_200_OK)
        
        return Response({
            "success": False,
            "message": "Invalid credentials"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    # def perform_create(self, serializer):
    #     user = serializer.save()
    #     serializer.is_valid(raise_exception=True)
    #     user.set_password(serializer.validated_date['password'])
    #     user.save()
    #     return user