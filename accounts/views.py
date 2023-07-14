import random
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from accounts import serializers
from .tasks import send_email
from .models import ActivityLog
# Create your views here.

User = get_user_model()

class LoginAPIView(GenericAPIView):
    """
    An endpoint to authenticate admin using their official Afex email and password.
    """
    authentication_classes = ()
    permission_classes = []
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = serializers.UserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(
            token), "access": str(token.access_token)}

        return Response(data, status=status.HTTP_200_OK)


class LogoutView(GenericAPIView):
    """
    An endpoint to logout authenticated user.
    """
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class ForgetPasswordView(GenericAPIView):
    serializer_class = serializers.ForgetPasswordSerializer
    authentication_classes = ()
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = User.objects.filter(email=email).get()
            if not user:
                return Response({"error": "Invalid email address. Enter a correct email address"}, status=status.HTTP_400_BAD_REQUEST)
            
            otp = str(random.randint(100000, 999999)) #generate 6 digits random number as otp
            print(len(otp))
            user.verification_code = otp
            user.save(update_fields=["verification_code"])

            #send email
            subject = "Password Reset Verification Pin"
            body = f'Your verification pin is {otp}'
            data = {"email_body": body, "to_email": email,
                    "email_subject": subject}
            send_email(data)
            return Response({'message': 'Verification pin sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPinView(GenericAPIView):
    serializer_class = serializers.VerifyPinSerializer
    authentication_classes = ()
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        verification_code = serializer.validated_data["verification_code"]

        user = User.objects.filter(email=email).get()
        print(user.verification_code)
        if user.verification_code != verification_code:
            return Response({"message": "Incorrect Verification Pin."}, status=status.HTTP_400_BAD_REQUEST)
        user.verification_code = ""
        user.save(update_fields=["verification_code"])
        return Response({"message": "verification successful"}, status=status.HTTP_200_OK)


class ResetPasswordView(GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer
    authentication_classes = ()
    permission_classes = []

    def post(self, request):
        serilizer = self.get_serializer(data=request.data)
        serilizer.is_valid(raise_exception=True)
        email = serilizer.validated_data["email"]
        new_password = serilizer.validated_data["new_password"]
        user = User.objects.filter(email=email).get()
        if user:
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid email address"}, status=status.HTTP_400_BAD_REQUEST)
    

class ActivityLogAPIView(ListAPIView):
    serializer_class = serializers.ActivityLogSerializer
    queryset = ActivityLog.objects.all()
    authentication_classes = ()
    permission_classes = []


class ActivityLogSortAPIView(GenericAPIView):
    """
    Endpoint for getting activity log sorted by date range.
    expects start date and end date
    """
    authentication_classes = ()
    permission_classes = []
    serializer_class = serializers.DateSerializer
    queryset = ActivityLog.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # format the start and end date. filter by succes is true
        start_date = serializer.validated_data["start_date"]
        end_date = serializer.validated_data["end_date"]
        queryset = self.get_queryset().filter(action_time__range=[start_date, end_date])[:20]

        serializer = serializers.ActivityLogSerializer(queryset, many=True)
        return Response({"message": "Sorted activity log", "data": serializer.data}, status=status.HTTP_200_OK)
    

# class Export