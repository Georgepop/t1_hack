from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User
def check_password(password:str)->bool:
    up_case_flag = False
    low_case_flag = False
    dig_flag = False
    spec_case = False
    for i in password:
        if i.isdigit():
            dig_flag =True
        elif i.isalpha() and i.isupper():
            up_case_flag = True
        elif i.isalpha() and i.islower():
            low_case_flag = True
        elif not(i.isalpha()) and not (i.isdigit()) and i != " ":
            spec_case = True
    if up_case_flag and low_case_flag and dig_flag and spec_case and len(password>=8):
        return True
    else:
        return False

class UserSerializer(serializers.ModelSerializer):
    access = serializers.CharField(max_length=32,required=False,default="free")
    class Meta:
        model = User
        fields = ["id","name","email","language","access","password"]

    def validate(self, data):
        password = data["password"]
        if not(check_password(password)):
            raise ValidationError("Пароль должен содержать строчные и заглавные буквы, спец символы и быть длинной"
                                  "не менее 8 символов")
        return data
    def create(self, validated_data):
        if "access" not in validated_data or not validated_data['access'].strip():
            validated_data["access"]="free"
        return super().create(validated_data)
class UserAuthSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=64)

    class Meta:
        model = User
        fields = ["id","email","password"]