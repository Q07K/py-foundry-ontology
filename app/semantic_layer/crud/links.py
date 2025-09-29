from neo4j import Driver

from app.semantic_layer.models.base import LinkType


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

    with driver.session() as session:
        result = session.run(
            query=query,
            parameters={
                "from_id": link.from_object_id,
                "to_id": link.to_object_id,
                "properties": link.properties,
            },
        )

    return link if result else None


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
