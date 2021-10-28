"""
These validators might be split up more
"""


def validate_merchant_exists(merchant_id: int) -> bool:
    return True


def validate_buyer_exists(buyer_id: int) -> bool:
    return True


def validate_product_exists(product_id: int) -> bool:
    return True


def validate_product_in_stock(product_id: int) -> bool:
    return True


def validate_product_merchant_relation(merchant_id: int, product_id: int) -> bool:
    return True


def validate_merchant_allows_discount(merchant_id: int) -> bool:
    return True
