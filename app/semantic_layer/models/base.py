from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PropertyType(str, Enum):
    """Foundry에서 지원하는 Property 타입"""

    STRING = "String"
    INTEGER = "Integer"
    SHORT = "Short"
    DATE = "Date"
    TIMESTAMP = "Timestamp"
    BOOLEAN = "Boolean"
    BYTE = "Byte"
    LONG = "Long"
    FLOAT = "Float"
    DOUBLE = "Double"
    DECIMAL = "Decimal"
    ARRAY = "Array"


class ObjectTypeSchema(BaseModel):
    """비즈니스 객체 타입 스키마 정의 모델"""

    type: str = Field(
        default=...,
        description=("비즈니스 객체 타입명 (예: Person, Product 등)"),
    )
    properties_schema: dict[str, PropertyType] = Field(
        default=...,
        description=(
            "객체의 속성명과 해당 속성의 데이터 타입 매핑된 딕셔너리 "
            "(예: {'name': 'String', 'age': 'Integer'})"
        ),
    )
    description: str | None = Field(
        default=None,
        description="객체 타입 설명",
    )
    primary_key: str = Field(
        default=...,
        description="객체의 primary key로 사용할 속성 필드명",
    )
    title_key: str = Field(
        default=...,
        description="객체의 제목으로 사용할 속성 필드명",
    )
    created_at: datetime = Field(default_factory=datetime.now)


class ObjectInstance(BaseModel):
    """비즈니스 객체 인스턴스 모델"""

    type: str = Field(
        default=...,
        description="비즈니스 객체 타입명 (예: Person, Product 등)",
    )
    primary_value: str = Field(
        default=...,
        description="객체의 primary key로 사용할 속성 값",
    )
    properties: dict[str, Any] = Field(
        default=...,
        description="객체의 속성명과 해당 속성 값이 매핑된 딕셔너리",
    )
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
