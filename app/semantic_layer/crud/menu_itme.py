from neo4j import Driver

from app.semantic_layer.models.menu_item import MenuItem

TYPE = "MenuItem"


def get_menu_item_by_name(
    driver: Driver,
    name: str,
) -> MenuItem | None:
    query = f"""
    MATCH (obj:{TYPE} {{name: $name}})
    RETURN obj
    """
    parameters = {
        "name": name,
    }
    with driver.session() as session:
        result = session.run(query=query, parameters=parameters)
        record = result.single()
        if record:
            node = record["obj"]
            return MenuItem(
                menu_item_id=node["id"],
                name=node["name"],
                price=node["price"],
            )
    return None
