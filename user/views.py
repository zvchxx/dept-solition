from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import authenticate
from user.models import UserModel
from rest_framework.permissions import AllowAny
from user.serializers import LoginSerializers, RegisterSerializers, UserModelSerializer
from rest_framework.authtoken.models import Token 
from rest_framework.permissions import IsAdminUser


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
    

class UserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        search_query = request.query_params.get('search', None)

        users = UserModel.objects.all()

        if search_query:
            if search_query.isdigit():
                users = users.filter(phone_number__icontains=search_query)
            else:
                users = users.filter(username__icontains=search_query)

        page = int(request.query_params.get('page', 1))
        paginator = int(request.query_params.get('paginator', 5))

        if page is not None:
            page -= 1
            users = users[page * paginator:page * paginator + paginator]

        serializer = UserModelSerializer(page, many=True)
        
        return Response({
            'total_users': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': page.number,
            'results': serializer.data
        }, status=status.HTTP_200_OK)
    

class UserDetailView(RetrieveAPIView):
    queryset = UserModel.objects.all()  
    serializer_class = UserModelSerializer 
    permission_classes = [IsAdminUser] 