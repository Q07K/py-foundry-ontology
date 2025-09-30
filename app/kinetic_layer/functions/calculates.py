from neo4j import Driver


def calculate_order_total(driver: Driver, order_id: str) -> float:
    with driver.session() as session:
        result = session.run(
            """
            MATCH (o:Order {id: $order_id})-[:CONTAINS]->(item:Item)
            RETURN SUM(item.price * item.quantity) AS total
            """,
            order_id=order_id,
        )
        record = result.single()
        return (
            record["total"] if record and record["total"] is not None else 0.0
        )


def calculate_customer_order_total(
    driver: Driver,
    customer_name: str,
    order_date: str = None,
) -> float:
    """
    특정 고객의 주문 총액을 계산합니다.
    order_date가 제공되면 해당 날짜의 주문만, 없으면 모든 주문을 계산합니다.
    """
    with driver.session() as session:
        if order_date:
            query = """
            MATCH (c:Customer {name: $customer_name})-[r:ORDERS]->(m:MenuItem)
            WHERE date(r.order_date) = date($order_date)
            RETURN SUM(COALESCE(m.price, 0) * r.quantity) AS total
            """
            result = session.run(
                query=query,
                customer_name=customer_name,
                order_date=order_date,
            )
        else:
            query = """
            MATCH (c:Customer {name: $customer_name})-[r:ORDERS]->(m:MenuItem)
            RETURN SUM(m.price * r.quantity) AS total
            """
            result = session.run(query, customer_name=customer_name)

        record = result.single()
        return (
            record["total"] if record and record["total"] is not None else 0.0
        )


def calculate_customer_order_total_flexible(
    driver: Driver,
    customer_name: str,
    order_date: str = None,
) -> float:
    """
    더 유연한 고객 주문 총액 계산 (다양한 날짜 형식 지원)
    """
    with driver.session() as session:
        if order_date:
            # 여러 방법으로 시도
            queries = [
                # 정확한 날짜 매칭
                """
                MATCH (c:Customer {name: $customer_name})-[r:ORDERS]->(m:MenuItem)
                WHERE date(r.order_date) = date($order_date)
                RETURN SUM(COALESCE(m.price, 0) * r.quantity) AS total
                """,
                # STARTS WITH 방식
                """
                MATCH (c:Customer {name: $customer_name})-[r:ORDERS]->(m:MenuItem)
                WHERE r.order_date STARTS WITH $order_date
                RETURN SUM(COALESCE(m.price, 0) * r.quantity) AS total
                """,
                # 문자열 매칭
                """
                MATCH (c:Customer {name: $customer_name})-[r:ORDERS]->(m:MenuItem)
                WHERE r.order_date = $order_date
                RETURN SUM(COALESCE(m.price, 0) * r.quantity) AS total
                """,
            ]

            for query in queries:
                try:
                    result = session.run(
                        query,
                        customer_name=customer_name,
                        order_date=order_date,
                    )
                    record = result.single()
                    total = (
                        record["total"]
                        if record and record["total"] is not None
                        else 0.0
                    )
                    if total > 0:
                        return total
                except (ValueError, TypeError, KeyError):
                    continue

            return 0.0
        else:
            query = """
            MATCH (c:Customer {name: $customer_name})-[r:ORDERS]->(m:MenuItem)
            RETURN SUM(m.price * r.quantity) AS total
            """
            result = session.run(query, customer_name=customer_name)
            record = result.single()
            return (
                record["total"]
                if record and record["total"] is not None
                else 0.0
            )


def calculate_menu_item_revenue(
    driver: Driver, menu_item_name: str, order_date: str = None
) -> float:
    """
    특정 메뉴 아이템의 매출을 계산합니다.
    order_date가 제공되면 해당 날짜의 매출만, 없으면 전체 매출을 계산합니다.
    """
    with driver.session() as session:
        if order_date:
            query = """
            MATCH (m:MenuItem {name: $menu_item_name})<-[r:ORDERS]-(c:Customer)
            WHERE date(r.order_date) = date($order_date)
            RETURN SUM(m.price * r.quantity) AS revenue
            """
            result = session.run(
                query, menu_item_name=menu_item_name, order_date=order_date
            )
        else:
            query = """
            MATCH (m:MenuItem {name: $menu_item_name})<-[r:ORDERS]-(c:Customer)
            RETURN SUM(m.price * r.quantity) AS revenue
            """
            result = session.run(query, menu_item_name=menu_item_name)

        record = result.single()
        return (
            record["revenue"]
            if record and record["revenue"] is not None
            else 0.0
        )


def calculate_daily_total_revenue(driver: Driver, order_date: str) -> float:
    """
    특정 날짜의 전체 매출을 계산합니다.
    """
    with driver.session() as session:
        result = session.run(
            """
            MATCH (c:Customer)-[r:ORDERS]->(m:MenuItem)
            WHERE date(r.order_date) = date($order_date)
            RETURN SUM(m.price * r.quantity) AS total_revenue
            """,
            order_date=order_date,
        )
        record = result.single()
        return (
            record["total_revenue"]
            if record and record["total_revenue"] is not None
            else 0.0
        )


def get_customer_order_history(
    driver: Driver, customer_name: str
) -> list[dict]:
    """
    특정 고객의 주문 내역을 반환합니다.
    """
    with driver.session() as session:
        result = session.run(
            """
            MATCH (c:Customer {name: $customer_name})-[r:ORDERS]->(m:MenuItem)
            RETURN m.name AS menu_item, r.quantity AS quantity, 
                   r.order_date AS order_date, m.price AS price,
                   (m.price * r.quantity) AS subtotal
            ORDER BY r.order_date DESC
            """,
            customer_name=customer_name,
        )
        return [
            {
                "menu_item": record["menu_item"],
                "quantity": record["quantity"],
                "order_date": record["order_date"],
                "price": record["price"],
                "subtotal": record["subtotal"],
            }
            for record in result
        ]


def get_menu_item_order_stats(driver: Driver, menu_item_name: str) -> dict:
    """
    특정 메뉴 아이템의 주문 통계를 반환합니다.
    """
    with driver.session() as session:
        result = session.run(
            """
            MATCH (m:MenuItem {name: $menu_item_name})<-[r:ORDERS]-(c:Customer)
            RETURN COUNT(r) AS total_orders,
                   SUM(r.quantity) AS total_quantity,
                   SUM(m.price * r.quantity) AS total_revenue,
                   AVG(r.quantity) AS avg_quantity_per_order
            """,
            menu_item_name=menu_item_name,
        )
        record = result.single()
        if record:
            return {
                "total_orders": record["total_orders"] or 0,
                "total_quantity": record["total_quantity"] or 0,
                "total_revenue": record["total_revenue"] or 0.0,
                "avg_quantity_per_order": record["avg_quantity_per_order"]
                or 0.0,
            }
        return {
            "total_orders": 0,
            "total_quantity": 0,
            "total_revenue": 0.0,
            "avg_quantity_per_order": 0.0,
        }


def calculate_date_range_revenue(
    driver: Driver, start_date: str, end_date: str
) -> float:
    """
    특정 날짜 범위의 전체 매출을 계산합니다.
    start_date, end_date: "yyyy-mm-dd" 형식
    """
    with driver.session() as session:
        result = session.run(
            """
            MATCH (c:Customer)-[r:ORDERS]->(m:MenuItem)
            WHERE r.order_date >= $start_date AND r.order_date < date($end_date) + duration('P1D')
            RETURN SUM(m.price * r.quantity) AS total_revenue
            """,
            start_date=start_date,
            end_date=end_date,
        )
        record = result.single()
        return (
            record["total_revenue"]
            if record and record["total_revenue"] is not None
            else 0.0
        )


def get_orders_by_date_range(
    driver: Driver, start_date: str, end_date: str
) -> list[dict]:
    """
    특정 날짜 범위의 모든 주문 내역을 반환합니다.
    start_date, end_date: "yyyy-mm-dd" 형식
    """
    with driver.session() as session:
        result = session.run(
            """
            MATCH (c:Customer)-[r:ORDERS]->(m:MenuItem)
            WHERE r.order_date STARTS WITH $start_date OR 
                  (r.order_date >= $start_date AND r.order_date < date($end_date) + duration('P1D'))
            RETURN c.name AS customer_name, m.name AS menu_item, 
                   r.quantity AS quantity, r.order_date AS order_date, 
                   m.price AS price, (m.price * r.quantity) AS subtotal
            ORDER BY r.order_date DESC
            """,
            start_date=start_date,
            end_date=end_date,
        )
        return [
            {
                "customer_name": record["customer_name"],
                "menu_item": record["menu_item"],
                "quantity": record["quantity"],
                "order_date": record["order_date"],
                "price": record["price"],
                "subtotal": record["subtotal"],
            }
            for record in result
        ]
