from neo4j import Driver, GraphDatabase

from app.core.config import get_settings


def connection() -> Driver:
    """Neo4j 드라이버 연결

    Returns
    -------
    Driver
        Neo4j 드라이버 인스턴스
    """
    settings = get_settings()
    return GraphDatabase.driver(
        uri=settings.neo4j_url,
        auth=(settings.neo4j_username, settings.neo4j_password),
    )


def disconnect(driver: Driver) -> None:
    """Neo4j 드라이버 연결 해제

    Parameters
    ----------
    driver : Driver
        Neo4j 드라이버 인스턴스
    """

    driver.close()
