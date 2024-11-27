from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import UserSerializer,UserAuthSerializer
from drf_spectacular.utils import extend_schema,OpenApiResponse,OpenApiParameter
from django.contrib.auth.hashers import make_password,check_password
from .models import User

# Create your views here.

class UserRegistration(APIView):
    @extend_schema(summary="Регистрация пользователя",
                   description="Регистрирует пользователя в системе, с его именем почтой и паролем и языком",
                   request=UserSerializer,
                   responses={
                       200:OpenApiResponse(response=Response({"status":"user created","user_id":1}),description="Пользователь успешно зарегестрирован"),
                       400:OpenApiResponse(description="Не былы переданы необходимые параметры,или параметры не верные")
                   })
    def post(self,request:Request):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            password = user.data["password"]
            user.data["password"] = make_password(password,None,"pbkdf2_sha256")
            user.save()
            return Response({"status":"user created","user_id":user.data["id"]},status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)
class UserLogin(APIView):
    @extend_schema()
    def post(self,request:Request):
        login_data = UserAuthSerializer(data=request.data)
        if login_data.is_valid():
            try:
                user:User = User.objects.get(email=login_data.email)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            password = login_data["password"]
            if check_password(password,user):
                pass
                # return Response({"status":""})