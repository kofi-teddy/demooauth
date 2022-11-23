from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework import permissions

from core.serializer import UserSerializer
from rest_framework.decorators import api_view, permission_classes


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def user_list(request):
    data = User.objects.all()

    serializer = UserSerializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save()
        
    return Response({
        "status": True,
        "message": "Successful",
        "data": serializer.data
    })
