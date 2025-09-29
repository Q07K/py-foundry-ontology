from app.semantic_layer.models.base import (
    ObjectInstance,
    ObjectTypeSchema,
    PropertyType,
)

TYPE = "Customer"


class CustomerSchema(ObjectTypeSchema):
    """고객 비즈니스 객체 타입 스키마 정의 모델"""

    type: str = TYPE
    properties_schema: dict[str, PropertyType] = {
        "name": PropertyType.STRING,
    }
    description: str = "레스토랑을 이용하는 고객"
    primary_key: str = "customer_id"
    title_key: str = "name"


class Customer(ObjectInstance):
    """고객 비즈니스 객체 모델"""

    def __init__(self, customer_id: str, name: str) -> None:
        super().__init__(
            type=TYPE,
            primary_value=customer_id,
            properties={
                "name": name,
            },
        )
