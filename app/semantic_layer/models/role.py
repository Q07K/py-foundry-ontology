from app.semantic_layer.models.base import (
    ObjectInstance,
    ObjectTypeSchema,
    PropertyType,
)

TYPE = "Role"


class RoleSchema(ObjectTypeSchema):
    """역할 비즈니스 객체 타입 스키마 정의 모델"""

    type: str = TYPE
    properties_schema: dict[str, PropertyType] = {
        "name": PropertyType.STRING,
    }
    description: str = "역할"
    primary_key: str = "role_id"
    title_key: str = "name"


class Role(ObjectInstance):
    """역할 비즈니스 객체 모델"""

    def __init__(self, role_id: str, name: str) -> None:
        super().__init__(
            type=TYPE,
            primary_value=role_id,
            properties={
                "name": name,
            },
        )
