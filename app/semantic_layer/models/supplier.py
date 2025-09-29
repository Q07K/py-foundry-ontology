from app.semantic_layer.models.base import (
    ObjectInstance,
    ObjectTypeSchema,
    PropertyType,
)

TYPE = "Supplier"


class SupplierSchema(ObjectTypeSchema):
    """공급업체 비즈니스 객체 타입 스키마 정의 모델"""

    type: str = TYPE
    properties_schema: dict[str, PropertyType] = {
        "name": PropertyType.STRING,
        "contact_info": PropertyType.STRING,
    }
    description: str = "메뉴 재료를 공급하는 업체"
    primary_key: str = "supplier_id"
    title_key: str = "name"


class Supplier(ObjectInstance):
    """공급업체 비즈니스 객체 모델"""

    def __init__(self, supplier_id: str, name: str, contact_info: str) -> None:
        super().__init__(
            type=TYPE,
            primary_value=supplier_id,
            properties={
                "name": name,
                "contact_info": contact_info,
            },
        )
