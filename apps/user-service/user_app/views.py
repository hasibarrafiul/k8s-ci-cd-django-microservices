from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User


@api_view(["GET"])
def get_users(request):
    users = list(
        User.objects.all().values("id", "auth_id", "username", "email")
    )
    return Response(users)