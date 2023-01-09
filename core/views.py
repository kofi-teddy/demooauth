from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.serializer import UserSerializer


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



@api_view(["POST"])
@permission_classes((AllowAny,))
def login_v2(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)

