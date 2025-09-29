from app.semantic_layer.models.base import (
    ObjectInstance,
    ObjectTypeSchema,
    PropertyType,
)

TYPE = "WorkDay"


class WorkDaySchema(ObjectTypeSchema):
    """근무일 비즈니스 객체 타입 스키마 정의 모델"""

    type: str = TYPE
    properties_schema: dict[str, PropertyType] = {
        "name": PropertyType.STRING,
    }
    description: str = "근무일"
    primary_key: str = "work_day_id"
    title_key: str = "name"


class WorkDay(ObjectInstance):
    """근무일 비즈니스 객체 모델"""

    def __init__(self, work_day_id: str, name: str) -> None:
        super().__init__(
            type=TYPE,
            primary_value=work_day_id,
            properties={
                "name": name,
            },
        )
