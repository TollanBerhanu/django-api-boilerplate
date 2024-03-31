from django.urls import path
from .views import ItemList, ItemDetail, LocationList, LocationDetail, DescriptionList, DescriptionDetail

urlpatterns = [
    path('item/', ItemList.as_view()),
    path('item/<int:pk>/', ItemDetail.as_view()),
    path('location/', LocationList.as_view()),
    path('location/<int:pk>/', LocationDetail.as_view()),
    path('description/', DescriptionList.as_view(), name='Description List'),
    path('description/<int:pk>/', DescriptionDetail.as_view(), name='Description Detail')
]
