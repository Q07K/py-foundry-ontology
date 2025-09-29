from app.semantic_layer.models.base import (
    ObjectInstance,
    ObjectTypeSchema,
    PropertyType,
)

TYPE = "MenuCategory"


class MenuCategorySchema(ObjectTypeSchema):
    """메뉴 카테고리 비즈니스 객체 타입 스키마 정의 모델"""

    type: str = TYPE
    properties_schema: dict[str, PropertyType] = {
        "name": PropertyType.STRING,
    }
    description: str = "메뉴 카테고리"
    primary_key: str = "menu_category_id"
    title_key: str = "name"


class MenuCategory(ObjectInstance):
    """메뉴 카테고리 비즈니스 객체 모델"""

    def __init__(self, menu_category_id: str, name: str) -> None:
        super().__init__(
            type=TYPE,
            primary_value=menu_category_id,
            properties={
                "name": name,
            },
        )
