from django.urls import path
from .views import ItemList, ItemDetail, LocationList, LocationDetail, DescriptionList, DescriptionItemDetail, DescriptionLocationDetail

urlpatterns = [
    path('item/', ItemList.as_view()),
    path('item/<int:pk>/', ItemDetail.as_view()),
    path('location/', LocationList.as_view()),
    path('location/<int:pk>/', LocationDetail.as_view()),
    path('description/', DescriptionList.as_view(), name='Description List'),
    path('description/item/<int:pk>/', DescriptionItemDetail.as_view(), name='Item Description Detail'),
    path('description/location/<int:pk>/', DescriptionLocationDetail.as_view(), name='Location Description Detail')
]
