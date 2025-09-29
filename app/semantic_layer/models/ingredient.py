from app.semantic_layer.models.base import (
    ObjectInstance,
    ObjectTypeSchema,
    PropertyType,
)

TYPE = "Ingredient"


class IngredientSchema(ObjectTypeSchema):
    """식품 재료 비즈니스 객체 타입 스키마 정의 모델"""

    type: str = TYPE
    properties_schema: dict[str, PropertyType] = {
        "name": PropertyType.STRING,
    }
    description: str = "식품 재료"
    primary_key: str = "ingredient_id"
    title_key: str = "name"


class Ingredient(ObjectInstance):
    """식품 재료 비즈니스 객체 모델"""

    def __init__(self, ingredient_id: str, name: str) -> None:
        super().__init__(
            type=TYPE,
            primary_value=ingredient_id,
            properties={
                "name": name,
            },
        )
