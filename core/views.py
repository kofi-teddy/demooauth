from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.serializer import UserSerializer
from django.conf import settings

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


@api_view(["POST"])
def login_v3(request):
    
    username = request.data.get("username")
    password = request.data.get("password")

    try:
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(request, user)
            token = ""
            time_threshold = datetime.now()
            token_obj = AccessToken.objects.filter(user=user, expires_gt=time_threshold)
            if token_obj:
                token_obj = token_obj[0]
                token = token_obj.token
            else:
                if not Application.objects.filter(user=user.id).exists():
                    Application.objects.create(user_id=user.id, authorization_grant_type="password", cleint_type="confidential")
                app_obj = Application.objects.filter(user=user.id).first()
                if app_obj:
                    client_id =  app_obj.client_id
                    client_secret =  app_obj.client_secret
                    url = http://localhost:1200/o/token/
                    request_data =  {
                        "grant_type": "password",
                        "username": username,
                        "password": password,
                        "client_id": client_id,
                        "cleint_secret": client_secret
                    }
                    response = requests.post(url, request_data)
                    response_data = json.loads(response.text)
                token = response_data.get("access_token")
                return Response(token)      

    except Exception as e:
        return Response({
            "status": True,
            "message": "Failed",
            'ERROR': str(e)
            })


@api_view(["POST"])
def token_refresh(request):
    refresh_token = request.data.get("refresh_token")
    try:
        token_obj = RefreshToken.objects.filter(user=request.user.id).first()
        if not token_obj:
            return Response({
                "status": False,
                "message": "Invalid token"
            })
        url = http://localhost:1200/o/token/
        request_data = {
            "grant_type": "refresh_token",
            "client_id": settings.OAUTH2_CLIENT_ID,
            "client_secret": settings.OAUTH2_CLIENT_SECRET,
            "refresh_token": refresh_token
        } 
        response = requests.post(url, request_data).text
        response_data = json.loads(response)

        return Response(response_data)
        
    except Exception as e:
        return Response({
            "status": False,
            "message": "Failed",
            "ERROR": str(e)
        })


@api_view(["POST"])
def revoke_token(request):
    
    try:

        url = http://localhost:1200/o/revoke_token/ 
        request_data = {
            "client_id": settings.OAUTH2_CLIENT_ID,
            "client_secret": settings.OAUTH2_CLIENT_SECRET,
            "token": request.data.get("access_token")
        }

        response = requests.post(url, request_data).text
        # response_data = json.loads(response)

        print(response)

        return Response({
            "status": True,
            "message": "Logout successful"
        })

    except Exception as e:
        return Response({
            "status": False,
            "message": "Failed",
            "ERROR": str(e)
        })





        

