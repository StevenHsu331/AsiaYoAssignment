from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services.order_service import OrderService
from .serializers.order_serializer import OrderSerializer

@api_view(["post"])
def add_order(req):
    return OrderService().add_order(data=req.data)
    