import random
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from accounts.serializers import UserLoginSerializer, UserSerializer, ForgetPasswordSerializer, VerifyPinSerializer
from base.utils import Util
# Create your views here.

User = get_user_model()

class LoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate existing users using their email and password.
    """
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(
            token), "access": str(token.access_token)}

        return Response(data, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class ForgetPasswordView(GenericAPIView):
    serializer_class = ForgetPasswordSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data
            user = User.objects.filter(email=email).exists()
            if not user:
                return Response({"error": "Invalid email address. Enter a correct email address"}, status=status.HTTP_400_BAD_REQUEST)
            otp = str(random.randint(100000, 999999)) #generate 6 digits random number as otp
            user.verification_code = otp
            user.save(update_fields=["verification_code"])

            #send email
            subject = "Password Reset Verification Pin"
            body = f'Your verification pin is {otp}'
            data = {"email_body": body, "to_email": email,
                    "email_subject": subject}
            Util.send_email(data)
            return Response({'message': 'Verification pin sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPinView(GenericAPIView):
    serializer_class = VerifyPinSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        verification_code = serializer.validated_data["verification_code"]

        user = User.objects.filter(email=email)
        if user.verification_code != verification_code:
            return Response({"message": "Incorrect Verification Pin."})
        user.verification_code = ""
        user.save(update_fields=["verification_code"])
        return Response({"message": "verification successful"}, status=status.HTTP_200_OK)
