from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item, Location
from .serializers import ItemSerializer, LocationSerializer

class ItemList(generics.ListCreateAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        queryset = Item.objects.all()
        location = self.request.query_params.get('location', '')
        if location:
            # queryset = queryset.filter(item_location=location)
            queryset = Item.objects.filter(item_location=location)
        return queryset

class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.all()

class LocationList(generics.ListCreateAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()

class DescriptionList(APIView):
    def get(self, request, format=None):

        item_filter = request.query_params.get('item', '')
        location_filter = request.query_params.get('location', '')

        items = Item.objects.filter(item_name__contains=item_filter)\
              if item_filter else Item.objects.all()

        serialized_items = ItemSerializer(items, many=True)
        if not serialized_items.data:
            return Response(data='Nothing to display :(', status=400)
        
        description = '**Summary:**\n'
        for idx, item in enumerate(serialized_items.data):
            item_name = item['item_name']

            location = None
            if location_filter:
                if Location.objects.filter(id=item['item_location'], location_name__contains=location_filter).exists():
                    location = Location.objects.get(id=item['item_location'], location_name__contains=location_filter)
                else:
                    description += f'{idx+1}. {item_name} doesn\'t exist in {location_filter}!'
            else:
                location = Location.objects.get(pk=item['item_location'])

            if location is not None:
                serialized_location = LocationSerializer(location)
                location_name = serialized_location.data['location_name']
                description += f'{idx+1}. {item_name} is located in {location_name}.\n'

        return Response(data=description, status=status.HTTP_200_OK)

class DescriptionItemDetail(APIView):
    def get(self, request, pk):
        if not Item.objects.filter(pk=pk).exists():
            return Response('The item does not exist!', status=status.HTTP_404_NOT_FOUND)
        
        item = Item.objects.get(pk=pk)
        serialized_item = ItemSerializer(item)

        location = Location.objects.get(pk=serialized_item.data['item_location'])
        serialized_location = LocationSerializer(location)

        return Response(( f'The selected item \'{serialized_item.data['item_name']}\' '
                          f'is located in the \'{serialized_location.data['location_name']}\'.' ),
                         status=status.HTTP_200_OK)

class DescriptionLocationDetail(APIView):
    def get(self, request, pk):
        if not Location.objects.filter(pk=pk).exists():
            return Response('No such location!', status=status.HTTP_404_NOT_FOUND)
        
        # location = Location.objects.get(pk=pk).pk
        location = Location.objects.get(pk=pk)
        location = LocationSerializer(location).data

        items = Item.objects.filter(item_location=location['id'])
        serialized_items = ItemSerializer(items, many=True)
        
        if serialized_items.data:
            items_in_location = ', '.join([item['item_name'] for item in serialized_items.data])
            return Response(f'The \'{location['location_name']}\' contains: {items_in_location}.')
        else:
            return Response(f'This {location['location_name']} does not contain any items!', status=status.HTTP_200_OK)