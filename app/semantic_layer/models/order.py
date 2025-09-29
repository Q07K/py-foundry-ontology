from app.semantic_layer.models.base import (
    ObjectInstance,
    ObjectTypeSchema,
    PropertyType,
)

TYPE = "Order"


class OrderSchema(ObjectTypeSchema):
    """주문 비즈니스 객체 타입 스키마 정의 모델"""

    type: str = TYPE
    properties_schema: dict[str, PropertyType] = {
        "name": PropertyType.STRING,
        "order_date": PropertyType.DATE,
        "total_amount": PropertyType.FLOAT,
    }
    description: str = "주문"
    primary_key: str = "order_id"
    title_key: str = "name"


class Order(ObjectInstance):
    """주문 비즈니스 객체 모델"""

    def __init__(
        self, order_id: str, name: str, order_date: str, total_amount: float
    ) -> None:
        super().__init__(
            type=TYPE,
            primary_value=order_id,
            properties={
                "name": name,
                "order_date": order_date,
                "total_amount": total_amount,
            },
        )
