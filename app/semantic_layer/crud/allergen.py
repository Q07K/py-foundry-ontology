from neo4j import Driver

from app.semantic_layer.models.allergen import Allergen


def create_object(driver: Driver, data: Allergen) -> Allergen | None:
    query = f"""
    CREATE (obj:{data.type} {{
        id: $primary_value,
        created_at: datetime(),
        updated_at: datetime()
    }})
    SET obj += $properties
    RETURN obj
    """
    with driver.session() as session:
        result = session.run(
            query=query,
            parameters={
                "primary_value": data.primary_value,
                "properties": data.properties,
            },
        )

        return data if result else None
