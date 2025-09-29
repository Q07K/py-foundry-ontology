from neo4j import Driver

from app.semantic_layer.models.customer import Customer

TYPE = "Customer"


def get_customer_by_name(driver: Driver, name: str) -> Customer | None:
    query = f"""
    MATCH (obj:{TYPE} {{name: $name}})
    RETURN obj
    """
    parameters = {
        "name": name,
    }
    with driver.session() as session:
        result = session.run(query, parameters)
        record = result.single()
        if record:
            node = record["obj"]
            return Customer(
                customer_id=node["id"],
                name=node["name"],
            )
    return None
