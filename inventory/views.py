from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def ping(request):
    return JsonResponse(data={"data":"PONG"}, status=200)