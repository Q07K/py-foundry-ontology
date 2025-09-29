from app.semantic_layer.models.base import (
    ObjectInstance,
    ObjectTypeSchema,
    PropertyType,
)

TYPE = "Employee"


class EmployeeSchema(ObjectTypeSchema):
    """직원 비즈니스 객체 타입 스키마 정의 모델"""

    type: str = TYPE
    properties_schema: dict[str, PropertyType] = {
        "name": PropertyType.STRING,
    }
    description: str = "직원"
    primary_key: str = "employee_id"
    title_key: str = "name"


class Employee(ObjectInstance):
    """직원 비즈니스 객체 모델"""

    def __init__(self, employee_id: str, name: str) -> None:
        super().__init__(
            type=TYPE,
            primary_value=employee_id,
            properties={
                "name": name,
            },
        )
