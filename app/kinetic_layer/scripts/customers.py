from app.database import neo4j_client
from app.kinetic_layer.functions.calculates import (
    calculate_customer_order_total,
    get_customer_order_history,
)
from app.kinetic_layer.functions.inferences import (
    find_similar_customers,
    infer_customer_preferences,
)

driver = neo4j_client.connection()
result = calculate_customer_order_total(
    driver,
    "사용자30",
    "2024-06-11",
)

print(f"Result: {result}")


result = get_customer_order_history(
    driver,
    "사용자30",
)

# print(f"Result: {result}")

inference_result = infer_customer_preferences(
    driver,
    "customer_30",
)

print(f"Inference Result: {inference_result}")


result = find_similar_customers(
    driver,
    "customer_30",
    limit=5,
)
print(f"Similar Customers: {result}")
