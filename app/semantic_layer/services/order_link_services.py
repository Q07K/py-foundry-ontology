from datetime import datetime

from neo4j import Driver

from app.semantic_layer.crud.base import create_link
from app.semantic_layer.crud.customer import get_customer_by_name
from app.semantic_layer.crud.menu_itme import get_menu_item_by_name
from app.semantic_layer.models.base import LinkType


def create_order_link(
    driver: Driver,
    customer_name: str,
    menu_item_name: str,
    quantity: int | None = 1,
    order_date: str | None = None,
) -> bool:
    # 1. Customer 객체 검색
    customer = get_customer_by_name(driver=driver, name=customer_name)
    if not customer:
        return False

    # 2. MenuItem 객체 검색
    menu_item = get_menu_item_by_name(driver=driver, name=menu_item_name)
    if not menu_item:
        return False

    if order_date is None:
        order_date = datetime.now().date().isoformat()

    # 3. 정방향 링크 생성 (고객 -> 메뉴 아이템)
    order_link = LinkType(
        from_object_type=customer.type,
        from_object_id=customer.primary_value,
        to_object_type=menu_item.type,
        to_object_id=menu_item.primary_value,
        link_type="ORDERS",
        properties={
            "quantity": quantity,
            "order_date": order_date,
        },
    )
    result = create_link(driver=driver, link=order_link)

    # 4. 역방향 링크 생성 (메뉴 아이템 -> 고객)
    order_link_r = LinkType(
        from_object_type=menu_item.type,
        from_object_id=menu_item.primary_value,
        to_object_type=customer.type,
        to_object_id=customer.primary_value,
        link_type="ORDERED_BY",
        properties={
            "quantity": quantity,
            "order_date": order_date,
        },
    )
    result = create_link(driver=driver, link=order_link_r)
    return result is not None
