from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view

from inventory.models import InventoryModel

import json

@api_view(['GET'])
def ping(request):
    return JsonResponse(data={"data":"PONG"}, status=200)


@api_view(['POST'])
def create_item(request):
    try:
        data = json.loads(request.body)
        ims_obj = InventoryModel(**data)
        ims_obj.save()
        return JsonResponse(data={'data':request.data}, status=201)
    except TypeError as e:
        return JsonResponse(data={'message': str(e)}, status=400)


@api_view(['GET'])
def read_all_items(request):
    data = list(InventoryModel.objects.values())
    if len(data) == 0:
        return JsonResponse(data={'message':'No items'}, status=204)
    return JsonResponse(data={'data':data}, status=200)


@api_view(['GET', 'PUT', 'DELETE'])
def manipulation_on_item(request):
    try:
        item_id = request.GET.get('item_id')
        data = InventoryModel.objects.get(id=item_id)

        if request.method == 'GET':
            data = model_to_dict(data)
            data = {'data': data}
            status = 200

        elif request.method == 'PUT':
            data = json.loads(request.body)
            InventoryModel.objects.filter(id=item_id).update(**data)
            data = {'data': 'Successfully updated'}
            status = 201

        elif request.method == 'DELETE':
            InventoryModel.objects.filter(id=item_id).delete()
            data = {'message':'Successfully deleted'}
            status = 200

        return JsonResponse(data=data, status=status)
    
    except InventoryModel.DoesNotExist:
        return JsonResponse(data={'message':'Item not found'}, status=404)


