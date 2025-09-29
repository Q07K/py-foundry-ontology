from app.semantic_layer.models.base import (
    ObjectInstance,
    ObjectTypeSchema,
    PropertyType,
)

TYPE = "MenuItem"


class MenuItemSchema(ObjectTypeSchema):
    """메뉴 아이템 비즈니스 객체 타입 스키마 정의 모델"""

    type: str = TYPE
    properties_schema: dict[str, PropertyType] = {
        "name": PropertyType.STRING,
        "price": PropertyType.INTEGER,
    }
    description: str = "메뉴 아이템"
    primary_key: str = "menu_item_id"
    title_key: str = "name"


class MenuItem(ObjectInstance):
    """메뉴 아이템 비즈니스 객체 모델"""

    def __init__(self, menu_item_id: str, name: str, price: float) -> None:
        super().__init__(
            type=TYPE,
            primary_value=menu_item_id,
            properties={
                "name": name,
                "price": price,
            },
        )
