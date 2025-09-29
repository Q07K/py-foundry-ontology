from app.semantic_layer.models.base import (
    ObjectInstance,
    ObjectTypeSchema,
    PropertyType,
)

TYPE = "Allergen"


class AllergenSchema(ObjectTypeSchema):
    """알레르기 비즈니스 객체 타입 스키마 정의 모델"""

    type: str = TYPE
    properties_schema: dict[str, PropertyType] = {
        "name": PropertyType.STRING,
    }
    description: str = "알레르기"
    primary_key: str = "allergen_id"
    title_key: str = "name"


class Allergen(ObjectInstance):
    """알레르기 비즈니스 객체 모델"""

    def __init__(self, allergen_id: str, name: str) -> None:
        super().__init__(
            type=TYPE,
            primary_value=allergen_id,
            properties={
                "name": name,
            },
        )
