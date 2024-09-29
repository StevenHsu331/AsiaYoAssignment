from ..serializers.order_serializer import OrderSerializer
from rest_framework import status
from rest_framework.response import Response
from ..validators.order_validator import OrderValidateManager

class OrderService():

    def add_order(self, data) -> Response:
        validator = OrderValidateManager(data)
        valid_result = validator.validate()

        if valid_result["status"]:
            order = OrderSerializer(data=data)
            if not order.is_valid():
                return Response(data="data is not valid or id already exists", status=status.HTTP_400_BAD_REQUEST)
            try:
                order.save()
                return Response(data="success", status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data="something went wrong during the process, please try again later", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data=valid_result["message"], status=status.HTTP_400_BAD_REQUEST)
