from django.urls import path
from .views import ItemListView, ItemCreateView, ItemToggleView

app_name = 'app'

urlpatterns = [
    path('', ItemListView.as_view(), name='item_list'),
    path('items/create/', ItemCreateView.as_view(), name='item_create'),
    path('items/<int:pk>/toggle/', ItemToggleView.as_view(), name='item_toggle'),
]
