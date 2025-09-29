from neo4j import Driver

from app.semantic_layer.models.base import LinkType, ObjectInstance


def create_link(driver: Driver, link: LinkType) -> LinkType | None:
    """두 객체 간의 링크(관계) 생성

    Parameters
    ----------
    driver : Driver
        Neo4j 드라이버 인스턴스
    link : LinkType
        링크 정보

    Returns
    -------
    LinkType | None
        생성된 링크 정보 또는 None
    """

    query = f"""
    MATCH (from:{link.from_object_type} {{id: $from_id}})
    MATCH (to:{link.to_object_type} {{id: $to_id}})
    CREATE (from)-[link:{link.link_type}]->(to)
    SET link += $properties, link.created_at = datetime()
    RETURN link
    """
    parameters = {
        "from_id": link.from_object_id,
        "to_id": link.to_object_id,
        "properties": link.properties,
    }

    with driver.session() as session:
        with session.begin_transaction() as tx:
            result = tx.run(query=query, parameters=parameters)
            record = result.single()
            tx.commit()

            if record:
                link.created_at = record["link"]["created_at"]
                return link

    return None


def get_links(
    driver: Driver,
    object_type: str,
    object_id: str,
    primary_key: str,
) -> list[dict]:
    query = f"""
    MATCH (obj:{object_type} {{{primary_key}: $object_id}})-[r]-(related)
    RETURN type(r) as relationship_type, 
            related as related_object,
            labels(related) as related_labels,
            r as relationship
    """

    with driver.session() as session:
        result = session.run(
            query=query,
            parameters={"object_id": object_id},
        )
        links = []
        for record in result:
            links.append(
                {
                    "relationship_type": record["relationship_type"],
                    "related_object": dict(record["related_object"]),
                    "related_labels": record["related_labels"],
                    "relationship": dict(record["relationship"]),
                }
            )
    return links


def create_object(
    driver: Driver,
    data: ObjectInstance,
) -> ObjectInstance | None:
    query = f"""
    CREATE (obj:{data.type} {{
        id: $primary_value,
        type: $type,
        created_at: datetime(),
        updated_at: datetime()
    }})
    SET obj += $properties
    RETURN obj
    """
    parameters = {
        "primary_value": data.primary_value,
        "type": data.type,
        "properties": data.properties,
    }

    with driver.session() as session:
        with session.begin_transaction() as tx:
            result = tx.run(query=query, parameters=parameters)
            record = result.single()
            tx.commit()

            if record:
                obj_data = record["obj"]
                data.created_at = obj_data["created_at"]
                data.updated_at = obj_data["updated_at"]
                return data

    return None
