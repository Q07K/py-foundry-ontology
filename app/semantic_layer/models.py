from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class OntologyProperty(BaseModel):
    """OntologyProperty 모델

    Notes
    -----
    OntologyProperty는 동적, 메타데이터가 중요한 속성을 정의하는 데 사용.
    이러한 속성들은 시간에 따라 변하고 출처와 신뢰도가 중요한 데이터를 정의하는 데 사용.

    "명사"(Entity/Thing)에 해당하는 속성들을 나타냄.
    각 속성은 이름, 값, 데이터 타입, 출처 및 신뢰도를 포함.

    Parameters
    ----------
    name : str
        속성 이름.
    value : Any
        속성 값.
    data_type : str
        속성 데이터 타입 (예: "string", "integer", "float", "boolean" 등).
    source : str
        속성 출처 (예: "user_input", "system_generated" 등).
    confidence : float
        속성 신뢰도 (0.0 ~ 1.0 사이의 값, 기본값: 1.0).
    tags : list[str]
        속성 태그 (기본값: 빈 리스트).
    metadata : dict[str, Any]
        추가 메타데이터 (기본값: 빈 딕셔너리).
    """

    name: str
    value: Any
    data_type: str
    source: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class OntologyObject(BaseModel):
    """OntologyObject 모델

    Notes
    -----
    OntologyObject는 비즈니스 엔터티의 속성을 정의하는 데 사용.

    "형용사"(Attribute/Characteristic)에 해당하는 속성들을 나타냄.
    각 속성은 아이디, 타입, 정적 객체 속성, 관계 및 생성 일시를 포함.

    Parameters
    ----------
    id : str
        객체 ID.
    type : str
        객체 타입 (예: "Person", "Product", "Location" 등).
    basic_properties : dict[str, Any]
        정적 객체 속성, 잘 변하지 않는 core identity.
        (예: {"name": "John", "birth": 1990})
    relationships : list[dict[str, Any]]
        객체 관계 (각 관계는 dict 형태로 표현).
    created_at : datetime
        객체 생성 일시 (기본값: 현재 시각).
    """

    id: str
    type: str
    basic_properties: dict[str, Any] = Field(default_factory=dict)
    relationships: list[dict[str, Any]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
