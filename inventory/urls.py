

from django.urls import path
from inventory.views import create_item, manipulation_on_item, ping, read_all_items

urlpatterns = [
    path('ping/', ping),
    path('items/',read_all_items, name='items'),
    path('item/create', create_item, name='create'),
    path('items/get_item', manipulation_on_item, name='get-item'),
    path('items/update_item', manipulation_on_item, name='update-item'), 
    path('items/delete_item', manipulation_on_item, name='delete-item'), 
]
