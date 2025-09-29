"""
이름	역할	근무 요일	경력
김철수	주방장(Head Chef)	월~금	15년
이영희	매니저	월~토	10년
박민수	서버	화~일	2년
안다혜	바리스타	월~금	3년



"""

# 사용자 생성
from app.database import neo4j_client
from app.semantic_layer.crud.base import create_object
from app.semantic_layer.models.customer import Customer

customers = [
    Customer(
        customer_id=f"customer_{i}",
        name=f"사용자{i}",
    )
    for i in range(1, 51)
]

# Driver 연결
driver = neo4j_client.connection()

# Object Instance 생성
for customer in customers:
    create_object(driver=driver, data=customer)
