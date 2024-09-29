import re
from numpy import empty
from rest_framework import serializers
from ..models.order import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
    
    def to_representation(self, instance) -> dict:
        result = super().to_representation(instance)
        result["address"] = {
            "city": result.pop("address_city", ""),
            "district": result.pop("address_district", ""),
            "street": result.pop("address_street", ""),
        }

        return result
        