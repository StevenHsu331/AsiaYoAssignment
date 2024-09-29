from django.db import models

class Order(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=128)
    address_city = models.CharField(max_length=128)
    address_district = models.CharField(max_length=128)
    address_street = models.CharField(max_length=128)
    price = models.IntegerField(null=True)
    currency = models.CharField(max_length=8)

    def __str__(self) -> str:
        return f"""
            id: {self.id}, 
            name: {self.name}, 
            city: {self.address_city}, 
            district: {self.address_district}, 
            street: {self.address_street}, 
            price: {self.price}, 
            currency: {self.currency}
        """
