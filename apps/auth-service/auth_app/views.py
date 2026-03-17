from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .rabbitmq import publish_user_created

User = get_user_model()

@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok"})

@api_view(["POST"])
def signup(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response(
            {"error": "username, email and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "username already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "email already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    publish_user_created(user)

    refresh = RefreshToken.for_user(user)

    return Response(
        {
            "message": "User created successfully",
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
        status=status.HTTP_201_CREATED,
    )