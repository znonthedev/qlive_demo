import string
import random
from uuid import UUID
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from .models import Account,PasswordRest
from .function import send_otp_email



# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(style={"input_type": "password"})

#     def validate(self, data):
#         user = authenticate(**data)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Incorrect Credentials")
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        # Check if the user with the given username exists
        try:
            user = Account.objects.get(username=username)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Incorrect username")

        # Verify the provided password
        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")

        return user
    
class LogoutSerializer(serializers.Serializer):
    pass




class RegisterStaffSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        help_text="Enter confirm password",
        style={"input_type": "password"},
    )

    class Meta:
        model = Account
        fields = ["username", "email", "phone", "password", "password2"]

        read_only_fields = ("password2",)

        # extra_kwargs = {
        #     "password": {"write_only": True},
        #     # 'password2':{'write_only':True}
        # }


    def create(self, validated_data):
        password = self.validated_data["password"]


        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Passwords must match."})
        else:
            user = Account.objects.create(
                username=validated_data["username"],
                email=validated_data["email"],
                phone=self.validated_data["phone"],
            ) 

            # Set the hashed password
            user.set_password(validated_data["password"])

            # Set the raw_password attribute
            user.raw_password = validated_data["password"]
            user.role = "staff"
            user.save()
            return user
        

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "username",
            "is_staff",
            "is_admin",
            "is_active",
            "role",
            "email",
            "is_staff",
            "phone",
            "password",
            "raw_password",
        )

class UpdateStaffPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['password']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.raw_password = validated_data["password"]
        instance.save()
        return instance

        
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = Account.objects.get(email=value)
        except Account.DoesNotExist:
            raise serializers.ValidationError("Invalid email address.")
        return value

    def save(self):
        user = Account.objects.get(email=self.validated_data['email'])
        
        # Generate 4-digit OTP
        otp = ''.join(random.choices(string.digits, k=4))
        
        # Save OTP in PasswordRest model
        password_reset_instance = PasswordRest.objects.create(account=user, otp=otp)
        print(otp)
        
        # Send the OTP via email (implement send_otp_email function)
        send_otp_email(user.email, otp)

        return {'otp_instance': password_reset_instance.id, 'parent_serializer_context': self.context}
        
class OTPConfirmationSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=4)
    token = serializers.CharField()

    def validate(self, data):
        # Validate OTP against the stored OTP in PasswordRest
        try:
            password_reset_instance = PasswordRest.objects.get(pk=data['token'], is_active=True)
            if password_reset_instance.otp != data['otp']:
                raise serializers.ValidationError("Invalid OTP.")
        except PasswordRest.DoesNotExist:
            raise serializers.ValidationError("Invalid token.")
        
        return data

    
class PasswordConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)
    token = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self):
        try:
            token_uuid = UUID(str(self.validated_data['token']))
            print(f"Token UUID: {token_uuid}")
            user = PasswordRest.objects.get(pk=token_uuid, is_active=True).account
            user.password = make_password(self.validated_data['password'])
            user.save()
        except PasswordRest.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired token.")
        except Exception as e:
            raise serializers.ValidationError(f"An error occurred: {str(e)}")