import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from ..models.order import Order

class TestOrderAPIs(TestCase):
    def setup(self):
        self.client = APIClient()

    def pop_and_get_new_dict(self, data: dict, key: str):
        result = data.copy()
        result.pop(key, None)
        return result

    def test_wrong_http_method(self):
        # use put
        mock_data = {
            "id": "",
            "name": "",
            "address": {
                "city": "",
                "district": "",
                "street": ""
            },
            "price": "",
            "currency": ""
        }
        res = self.client.put(path="/api/orders/", data=json.dumps(mock_data), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_empty_data(self):
        # data is empty
        mock_data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "1000",
            "currency": "TWD"
        }
        res = self.client.post(path="/api/orders/", data=json.dumps(self.pop_and_get_new_dict(mock_data, "id")), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "ID is empty")

        res = self.client.post(path="/api/orders/", data=json.dumps(self.pop_and_get_new_dict(mock_data, "name")), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "Name is empty")

        res = self.client.post(path="/api/orders/", data=json.dumps(self.pop_and_get_new_dict(mock_data, "address")), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "City is empty")

        res = self.client.post(path="/api/orders/", data=json.dumps(self.pop_and_get_new_dict(mock_data, "price")), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "Price is empty")

        res = self.client.post(path="/api/orders/", data=json.dumps(self.pop_and_get_new_dict(mock_data, "currency")), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "Currency is empty")

    def test_wrong_data_type(self):
        # price is not integer
        mock_data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "AAA",
            "currency": "TWD"
        }
        res = self.client.post(path="/api/orders/", data=json.dumps(mock_data), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "Price is not a number")

    def test_name_non_english(self):
        mock_data = {
            "id": "A0000001",
            "name": "旅館名稱",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "1800",
            "currency": "TWD"
        }
        res = self.client.post(path="/api/orders/", data=json.dumps(mock_data), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "Name contains non-English characters")

    def test_name_capitailzed(self):
        mock_data = {
            "id": "A0000001",
            "name": "melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "1800",
            "currency": "TWD"
        }
        res = self.client.post(path="/api/orders/", data=json.dumps(mock_data), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "Name is not capitalized")

    def test_price_overflow_twd(self):
        mock_data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "2050",
            "currency": "TWD"
        }
        res = self.client.post(path="/api/orders/", data=json.dumps(mock_data), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "Price is over 2000")

    def test_price_overflow_usd(self):
        mock_data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "1000",
            "currency": "USD"
        }
        res = self.client.post(path="/api/orders/", data=json.dumps(mock_data), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "Price is over 2000")

    def test_price_currency_format(self):
        mock_data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "1000",
            "currency": "JPY"
        }
        res = self.client.post(path="/api/orders/", data=json.dumps(mock_data), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "Curreny format is wrong")

    def test_duplicate_id(self):
        mock_data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "1000",
            "currency": "TWD"
        }
        res = self.client.post(path="/api/orders/", data=json.dumps(mock_data), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.post(path="/api/orders/", data=json.dumps(mock_data), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data, "data is not valid or id already exists")

    def test_success(self):
        mock_data = {
            "id": "A0000001",
            "name": "Melody Holiday Inn",
            "address": {
                "city": "taipei-city",
                "district": "da-an-district",
                "street": "fuxing-south-road"
            },
            "price": "1000",
            "currency": "TWD"
        }
        res = self.client.post(path="/api/orders/", data=json.dumps(mock_data), content_type="application/json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        