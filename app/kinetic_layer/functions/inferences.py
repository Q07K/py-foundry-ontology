from neo4j import Driver


def infer_customer_preferences(driver: Driver, customer_id: str) -> list[str]:
    """고객 선호도 추론"""
    query = """
    MATCH (c:Customer {id: $customerId})-[:ORDERS]->(m:MenuItem)
          -[:BELONGS_TO]->(mc:MenuCategory)
    WITH mc.name as category, count(*) as frequency
    WHERE frequency >= 3
    RETURN category
    ORDER BY frequency DESC
    LIMIT 5
    """
    result = driver.session().run(query, {"customerId": customer_id})
    return [r["category"] for r in result]


def find_similar_customers(
    driver: Driver,
    customer_id: str,
    limit: int = 10,
) -> list[dict]:
    """유사 고객 Jaccard 유사도로 찾기"""
    query = """
    MATCH (c1:Customer {id: $customerId})-[:ORDERS]->(m:MenuItem)
          -[:BELONGS_TO]->(mc:MenuCategory)
    WITH c1, collect(DISTINCT mc.name) as c1Categories
    
    MATCH (c2:Customer)-[:ORDERS]->(m2:MenuItem)
          -[:BELONGS_TO]->(mc2:MenuCategory)
    WHERE c2.id <> $customerId
    WITH c1, c2, c1Categories, collect(DISTINCT mc2.name) as c2Categories
    
    // Jaccard 유사도 계산
    WITH c2,
         [cat IN c1Categories WHERE cat IN c2Categories] as commonCategories,
         c1Categories + [cat IN c2Categories WHERE NOT cat IN c1Categories] as allCategories
    
    RETURN 
        c2.id as customerId,
        c2.name as name,
        toFloat(size(commonCategories)) / size(allCategories) as similarity
    ORDER BY similarity DESC
    LIMIT $limit
    """

    with driver.session() as session:
        result = session.run(
            query, {"customerId": customer_id, "limit": limit}
        )
        return [
            {
                "customerId": record["customerId"],
                "name": record["name"],
                "similarity": record["similarity"],
            }
            for record in result
        ]
