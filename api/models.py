from django.db import models

class Location(models.Model):
    location_name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.location_name

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    date_added = models.DateField(auto_now_add=True)
    item_location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.item_name