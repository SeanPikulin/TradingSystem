from dataclasses import dataclass


@dataclass
class OfferData:
    id: str
    price: float
    status: str
    store_name: str
    product_id: str
    product_name: str
    username: str