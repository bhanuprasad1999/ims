from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return JsonResponse(data={'message':'Username, email and password are required'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return JsonResponse(data={'message':'Username already exists'}, status=400)
    
    if User.objects.filter(email=email).exists():
        return JsonResponse(data={'message':'Email already exists'}, status=400)
    

    user = User(username=username, email=email)
    user.set_password(password)
    user.save()

    return JsonResponse(data={'message':'User Registered successfully'}, status=201)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        # Create tokens
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return JsonResponse({
            'refresh': str(refresh),
            'access': access
        }, status=200)
    
    return JsonResponse(data={'message':'Invalid credentials'}, status=400)