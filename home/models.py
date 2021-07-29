from django.db import models

# Create your models here.
class Locations(models.Model):
    locationid = models.CharField(max_length=50, blank = False)

    def __str__(self):
        return self.locationid
    


class Product(Locations):
    
    ProductId = models.CharField(max_length=100, blank = False)
    qt = models.IntegerField()

    def __str__(self):
        return '{} {} {}'.format(self.ProductId, self.qt, self.locationid)
    
    
class ProductMovement(Product):
    
    movementId = models.CharField(max_length=50, blank = False)
    timestamp = models.TimeField(auto_now=True, auto_now_add=False)
    from_location = models.CharField(max_length=50, blank = True)
    to_location  = models.CharField(max_length=50, blank = True)
    qty = models.IntegerField(blank = False)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.movementId, self.timestamp, self.from_location, self.to_location, self.qty, self.ProductId)
