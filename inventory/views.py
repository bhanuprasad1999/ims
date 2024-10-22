import json

from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core.cache import cache

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from inventory.models import InventoryModel


@api_view(['GET'])
def ping(request):
    return JsonResponse(data={"data":"PONG"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_item(request):
    try:
        data = json.loads(request.body)
        ims_obj = InventoryModel(**data)
        ims_obj.save()
        return JsonResponse(data={'data':request.data}, status=201)
    except TypeError as e:
        return JsonResponse(data={'message': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_all_items(request):
    data = list(InventoryModel.objects.values())
    if len(data) == 0:
        return JsonResponse(data={'message':'No items'}, status=204)
    return JsonResponse(data={'data':data}, status=200)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def manipulation_on_item(request):
    try:
        item_id = request.GET.get('item_id')
        cache_data = cache.get(item_id)
        data = cache_data

        if data is None:
            data = InventoryModel.objects.get(id=item_id)
            cache.set(item_id, data, timeout=60)

        if request.method == 'GET':
            data = model_to_dict(data)
            data = {'data': data}
            status = 200

        elif request.method == 'PUT':
            data = json.loads(request.body)
            InventoryModel.objects.filter(id=item_id).update(**data)
            if cache_data is not None:
                cache.delete(item_id)
            data = {'message':'Successfully updated'}
            status = 201

        elif request.method == 'DELETE':
            InventoryModel.objects.filter(id=item_id).delete()
            if cache_data is not None:
                cache.delete(item_id)
            data = {'message':'Successfully deleted'}
            status = 200

        return JsonResponse(data=data, status=status)
    
    except InventoryModel.DoesNotExist:
        return JsonResponse(data={'message':'Item not found'}, status=404)
    
    except Exception:
        return JsonResponse(data={'message':'Something went wrong!'}, status=400)


