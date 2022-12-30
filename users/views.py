from django.contrib.auth import authenticate, logout
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import SignUpSerializer, GetUserSerializer
from .tokens import create_jwt_pair_for_user
from rest_framework import viewsets
from .models import User
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated 
from rest_framework import permissions
from rest_framework.throttling import UserRateThrottle
# Create your views here.

#CON CLASE GENERIC APIVIEW
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    
    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {"message": "El usuario se creó correctamente", "data": serializer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#CON CLASE APIVIEW
class LoginView(APIView): 
    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)
        print(user)
        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            print(tokens)
            response = {"message": "Logeado correctamente","data": GetUserSerializer(user).data,"tokens": tokens}
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response(
                data={"message": "Correo inválido o contraseña incorrecta"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request: Request):
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)

#SOLO DE LECTURA
class GetUsers(viewsets.ReadOnlyModelViewSet):
    #permission_classes = [AllowAny]
    #throttle_classes = [UserRateThrottle]
    #permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetUserSerializer
    queryset = User.objects.all()

class LogoutView(APIView):
    def post(self, request):
        logout(request)

        return Response(status=status.HTTP_200_OK)
