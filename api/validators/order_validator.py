import re
from abc import abstractmethod
from .validator import Validator
from typing import List

class OrderIdValidator(Validator):
    def validate(self, data) -> dict:
        if "id" not in data or len(data["id"]) == 0:
            return {"status": False, "message": "ID is empty"}
        return {"status": True, "message": "success"}
        
class OrderNameValidator(Validator):
    def validate(self, data) -> dict:
        if "name" not in data or len(data["name"]) == 0:
            return {"status": False, "message": "Name is empty"}
        if not re.match(pattern=r"^[a-zA-Z ]+$", string=data["name"]):
            return {"status": False, "message": "Name contains non-English characters"}
        if data["name"][0].islower():
            return {"status": False, "message": "Name is not capitalized"}
        return {"status": True, "message": "success"}
        
class OrderAddressCityValidator(Validator):
    def validate(self, data) -> dict:
        if "address_city" not in data or len(data["address_city"]) == 0:
            return {"status": False, "message": "City is empty"}
        return {"status": True, "message": "success"}
        
class OrderAddressDistrictValidator(Validator):
    def validate(self, data)-> dict:
        if "address_district" not in data or len(data["address_district"]) == 0:
            return {"status": False, "message": "District is empty"}
        return {"status": True, "message": "success"}

class OrderAddressStreetValidator(Validator):
    def validate(self, data) -> dict:
        if "address_street" not in data or len(data["address_street"]) == 0:
            return {"status": False, "message": "Street is empty"}
        return {"status": True, "message": "success"}
        
class OrderCurrencyValidator(Validator):
    def validate(self, data) -> dict:
        if "currency" not in data or len(data["currency"]) == 0:
            return {"status": False, "message": "Currency is empty"}
        
        if data["currency"] != "TWD" and data["currency"] != "USD":
            return {"status": False, "message": "Curreny format is wrong"}
        elif data["currency"] == "USD":
            data["price"] *= 31
        return {"status": True, "message": "success"}

class OrderPriceValidator(Validator):
    def validate(self, data) -> dict:
        if "price" not in data or len(data["price"]) == 0:
            return {"status": False, "message": "Price is empty"}
        
        # parse price to integer before price validation
        if re.match(pattern=r"^[0-9]+$", string=data["price"]):
            data["price"] = int(data["price"])
        else:
            return {"status": False, "message": "Price is not a number"}
        
        if data["price"] > 2000:
            return {"status": False, "message": "Price is over 2000"}
        return {"status": True, "message": "success"}
    
class OrderValidateManager:
    validators: List[Validator] = [
        OrderIdValidator(),
        OrderNameValidator(),
        OrderAddressCityValidator(),
        OrderAddressDistrictValidator(),
        OrderAddressStreetValidator(),
        OrderCurrencyValidator(),
        OrderPriceValidator()
    ]

    def __init__(self, data) -> None:
        # extract address details
        if "address" in data:
            address = data.pop("address", None)
            if address:
                data["address_city"] = address["city"]
                data["address_district"] = address["district"]
                data["address_street"] = address["street"]

        self.data = data

    def validate(self) -> dict:
        for validator in self.validators:
            result = validator.validate(data=self.data)
            if not result["status"]:
                return result
        return {"status": True, "message": "success"}