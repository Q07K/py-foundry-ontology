from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class LinkType(BaseModel):
    """비즈니스 객체 간의 링크 타입 모델"""

    from_object_type: str = Field(default=..., description="출발 객체 타입")
    from_object_id: str = Field(default=..., description="출발 객체 ID")
    to_object_type: str = Field(default=..., description="도착 객체 타입")
    to_object_id: str = Field(default=..., description="도착 객체 ID")
    link_type: str = Field(default=..., description="링크 타입")
    properties: dict[str, Any] = Field(
        default_factory=dict,
        description="링크 속성",
    )
    created_at: datetime = Field(default_factory=datetime.now)
