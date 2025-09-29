from app.database import neo4j_client
from app.semantic_layer.crud.base import create_link, create_object
from app.semantic_layer.models.allergen import Allergen
from app.semantic_layer.models.base import LinkType
from app.semantic_layer.models.ingredient import Ingredient
from app.semantic_layer.models.menu_category import MenuCategory
from app.semantic_layer.models.menu_item import MenuItem
from app.semantic_layer.models.supplier import Supplier

# 메뉴 아이템 생성
menu_item_margherita_pizza = MenuItem(
    menu_item_id="menu_item_001",
    name="마르게리타 피자",
    price=15000,
)
menu_item_carbonara_pasta = MenuItem(
    menu_item_id="menu_item_002",
    name="까르보나라 파스타",
    price=18000,
)
menu_item_tiramisu = MenuItem(
    menu_item_id="menu_item_003",
    name="티라미수",
    price=8000,
)
menu_item_americano = MenuItem(
    menu_item_id="menu_item_004",
    name="아메리카노",
    price=5000,
)

# 메뉴 카테고리 생성
menu_category_pizza = MenuCategory(
    menu_category_id="menu_category_001",
    name="피자",
)
menu_category_pasta = MenuCategory(
    menu_category_id="menu_category_002",
    name="파스타",
)
menu_category_desserts = MenuCategory(
    menu_category_id="menu_category_003",
    name="디저트",
)
menu_category_drinks = MenuCategory(
    menu_category_id="menu_category_004",
    name="음료",
)

# 메뉴 재료 생성
ingredient_flour = Ingredient(
    ingredient_id="ingredient_001",
    name="밀가루",
)
ingredient_tomato = Ingredient(
    ingredient_id="ingredient_002",
    name="토마토",
)
ingredient_cheese = Ingredient(
    ingredient_id="ingredient_003",
    name="치즈",
)
ingredient_basil = Ingredient(
    ingredient_id="ingredient_004",
    name="바질",
)
ingredient_dough_noodle = Ingredient(
    ingredient_id="ingredient_005",
    name="파스타 면",
)
ingredient_bacon = Ingredient(
    ingredient_id="ingredient_006",
    name="베이컨",
)
ingredient_egg = Ingredient(
    ingredient_id="ingredient_007",
    name="계란",
)
ingredient_mascarpone = Ingredient(
    ingredient_id="ingredient_008",
    name="마스카포네",
)
ingredient_espresso = Ingredient(
    ingredient_id="ingredient_009",
    name="에스프레소",
)
ingredient_cocoa_powder = Ingredient(
    ingredient_id="ingredient_010",
    name="코코아",
)
ingredient_coffee_beans = Ingredient(
    ingredient_id="ingredient_011",
    name="원두",
)
ingredient_water = Ingredient(
    ingredient_id="ingredient_012",
    name="물",
)

# 알레르기 정보 생성
allergen_gluten = Allergen(
    allergen_id="allergen_001",
    name="글루텐",
)
allergen_dairy = Allergen(
    allergen_id="allergen_002",
    name="유제품",
)
allergen_egg = Allergen(
    allergen_id="allergen_003",
    name="계란",
)
allergen_caffeine = Allergen(
    allergen_id="allergen_004",
    name="카페인",
)


# 공급업체 생성
supplier_vegetable = Supplier(
    supplier_id="supplier_001",
    name="신촌 농산물 유통센터",
    contact_info="02-222-3333",
)
supplier_italian = Supplier(
    supplier_id="supplier_002",
    name="이탈리아 직수입상",
    contact_info="070-9876-5432",
)
supplier_dairy = Supplier(
    supplier_id="supplier_003",
    name="한국 낙농 협회",
    contact_info="02-555-1212",
)

# Driver 연결
driver = neo4j_client.connection()

# Object Instance 생성
create_object(driver=driver, data=menu_item_margherita_pizza)
create_object(driver=driver, data=menu_item_carbonara_pasta)
create_object(driver=driver, data=menu_item_tiramisu)
create_object(driver=driver, data=menu_item_americano)
create_object(driver=driver, data=menu_category_pizza)
create_object(driver=driver, data=menu_category_pasta)
create_object(driver=driver, data=menu_category_desserts)
create_object(driver=driver, data=menu_category_drinks)
create_object(driver=driver, data=ingredient_flour)
create_object(driver=driver, data=ingredient_tomato)
create_object(driver=driver, data=ingredient_cheese)
create_object(driver=driver, data=ingredient_basil)
create_object(driver=driver, data=ingredient_dough_noodle)
create_object(driver=driver, data=ingredient_bacon)
create_object(driver=driver, data=ingredient_egg)
create_object(driver=driver, data=ingredient_mascarpone)
create_object(driver=driver, data=ingredient_espresso)
create_object(driver=driver, data=ingredient_cocoa_powder)
create_object(driver=driver, data=ingredient_coffee_beans)
create_object(driver=driver, data=ingredient_water)
create_object(driver=driver, data=allergen_gluten)
create_object(driver=driver, data=allergen_dairy)
create_object(driver=driver, data=allergen_egg)
create_object(driver=driver, data=allergen_caffeine)
create_object(driver=driver, data=supplier_vegetable)
create_object(driver=driver, data=supplier_italian)
create_object(driver=driver, data=supplier_dairy)

# 관계 설정
# `BELONGS_TO`<-> `HAS_ITEM` 관계 설정 (메뉴 아이템 <-> 카테고리)
data = [
    (menu_item_margherita_pizza, [menu_category_pizza]),
    (menu_item_carbonara_pasta, [menu_category_pasta]),
    (menu_item_tiramisu, [menu_category_desserts]),
    (menu_item_americano, [menu_category_drinks]),
]
for item, categories in data:
    for category in categories:
        create_link(
            driver=driver,
            link=LinkType(
                from_object_type=item.type,
                from_object_id=item.primary_value,
                to_object_type=category.type,
                to_object_id=category.primary_value,
                link_type="BELONGS_TO",
                properties={},
            ),
        )
        create_link(
            driver=driver,
            link=LinkType(
                from_object_type=category.type,
                from_object_id=category.primary_value,
                to_object_type=item.type,
                to_object_id=item.primary_value,
                link_type="HAS_ITEM",
                properties={},
            ),
        )


# `CONTAINS` <-> `IS_CONTAINED_IN` 관계 설정 (메뉴 아이템 <-> 재료)
data = [
    (
        menu_item_margherita_pizza,
        [
            ingredient_flour,
            ingredient_tomato,
            ingredient_cheese,
            ingredient_basil,
        ],
    ),
    (
        menu_item_carbonara_pasta,
        [
            ingredient_dough_noodle,
            ingredient_bacon,
            ingredient_egg,
            ingredient_cheese,
        ],
    ),
    (
        menu_item_tiramisu,
        [ingredient_mascarpone, ingredient_espresso, ingredient_cocoa_powder],
    ),
    (
        ingredient_espresso,
        [ingredient_coffee_beans, ingredient_water],
    ),
    (
        menu_item_americano,
        [ingredient_espresso, ingredient_water],
    ),
]

for item, ingredients in data:
    for ingredient in ingredients:
        create_link(
            driver=driver,
            link=LinkType(
                from_object_type=item.type,
                from_object_id=item.primary_value,
                to_object_type=ingredient.type,
                to_object_id=ingredient.primary_value,
                link_type="CONTAINS",
                properties={},
            ),
        )
        create_link(
            driver=driver,
            link=LinkType(
                from_object_type=ingredient.type,
                from_object_id=ingredient.primary_value,
                to_object_type=item.type,
                to_object_id=item.primary_value,
                link_type="IS_CONTAINED_IN",
                properties={},
            ),
        )

# `HAS_ALLERGEN` 관계 설정 (메뉴 아이템 -> 알레르기 정보)
data = [
    (
        menu_item_margherita_pizza,
        [allergen_gluten, allergen_dairy],
    ),
    (
        menu_item_carbonara_pasta,
        [allergen_gluten, allergen_dairy, allergen_egg],
    ),
    (
        menu_item_tiramisu,
        [allergen_dairy, allergen_caffeine],
    ),
    (
        menu_item_americano,
        [allergen_caffeine],
    ),
]
for item, allergens in data:
    for allergen in allergens:
        create_link(
            driver=driver,
            link=LinkType(
                from_object_type=item.type,
                from_object_id=item.primary_value,
                to_object_type=allergen.type,
                to_object_id=allergen.primary_value,
                link_type="HAS_ALLERGEN",
                properties={},
            ),
        )
        create_link(
            driver=driver,
            link=LinkType(
                from_object_type=allergen.type,
                from_object_id=allergen.primary_value,
                to_object_type=item.type,
                to_object_id=item.primary_value,
                link_type="IS_ALLERGEN_OF",
                properties={},
            ),
        )

# `SUPPLIED_BY` <-> `SUPPLIES` 관계 설정 (재료 <-> 공급업체)
data = [
    (
        supplier_vegetable,
        [ingredient_flour, ingredient_tomato, ingredient_basil],
    ),
    (
        supplier_italian,
        [ingredient_dough_noodle, ingredient_espresso],
    ),
    (
        supplier_dairy,
        [ingredient_cheese, ingredient_mascarpone, ingredient_egg],
    ),
]
for supplier, ingredients in data:
    for ingredient in ingredients:
        create_link(
            driver=driver,
            link=LinkType(
                from_object_type=ingredient.type,
                from_object_id=ingredient.primary_value,
                to_object_type=supplier.type,
                to_object_id=supplier.primary_value,
                link_type="SUPPLIES",
                properties={},
            ),
        )
        create_link(
            driver=driver,
            link=LinkType(
                from_object_type=supplier.type,
                from_object_id=supplier.primary_value,
                to_object_type=ingredient.type,
                to_object_id=ingredient.primary_value,
                link_type="SUPPLIED_BY",
                properties={},
            ),
        )

# Driver 연결 해제
neo4j_client.disconnect(driver=driver)
