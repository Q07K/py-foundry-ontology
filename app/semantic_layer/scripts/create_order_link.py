import pandas as pd

from app.database import neo4j_client
from app.semantic_layer.services.order_link_services import create_order_link
from app.semantic_layer.utils.excel_parser import parse_excel_file

# Driver 연결
driver = neo4j_client.connection()

df = parse_excel_file(
    file_path="data/지피티스퀘어_온톨로지실습_202509.xlsx",
    sheet_name="4.데이터_구매이력",
)

df = df[["User", "MenuItem", "Quantity", "Date"]].dropna()

for _, row in df.iterrows():
    customer_name = row["User"]
    menu_item_name = row["MenuItem"]
    quantity = int(row["Quantity"]) if not pd.isna(row["Quantity"]) else 1
    order_date = row["Date"] if not pd.isna(row["Date"]) else None

    is_created_order_link = create_order_link(
        driver=driver,
        customer_name=customer_name,
        menu_item_name=menu_item_name,
        quantity=quantity,
        order_date=order_date,
    )

    print(
        f"Created order link for {customer_name} -> {menu_item_name}"
        f": {is_created_order_link}"
    )
