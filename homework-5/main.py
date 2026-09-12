import json

import psycopg2

from config import config


def main():
    script_file = 'fill_db.sql'
    json_file = 'suppliers.json'
    db_name = 'my_new_db'

    params = config()
    conn = None

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                execute_sql_script(cur, script_file)
                print(f"БД {db_name} успешно заполнена")

                create_suppliers_table(cur)
                print("Таблица suppliers успешно создана")

                suppliers = get_suppliers_data(json_file)
                insert_suppliers_data(cur, suppliers)
                print("Данные в suppliers успешно добавлены")

                add_foreign_keys(cur, json_file)
                print(f"FOREIGN KEY успешно добавлены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    cur.close()
    conn.close()


def execute_sql_script(cur, script_file) -> None:
    """Выполняет скрипт из файла для заполнения БД данными."""
    with open(script_file, 'r', encoding='utf-8') as file:
        sql = file.read()
    cur.execute(sql)


def create_suppliers_table(cur) -> None:
    """Создает таблицу suppliers."""
    cur.execute("""
        CREATE TABLE suppliers (
            supplier_id SERIAL PRIMARY KEY,
            company_name VARCHAR(100) NOT NULL,
            contact VARCHAR(100),
            address VARCHAR(200),
            phone VARCHAR(50),
            fax VARCHAR(50),
            homepage TEXT
        );
    """)


def get_suppliers_data(json_file: str) -> list[dict]:
    """Извлекает данные о поставщиках из JSON-файла."""
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def insert_suppliers_data(cur, suppliers: list[dict]) -> None:
    """Добавляет данные из suppliers в таблицу suppliers."""
    for supplier in suppliers:
        cur.execute("""
            INSERT INTO suppliers (company_name, contact, address, phone, fax, homepage)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            supplier.get('company_name'),
            supplier.get('contact'),
            supplier.get('address'),
            supplier.get('phone'),
            supplier.get('fax'),
            supplier.get('homepage')
        ))


def add_foreign_keys(cur, json_file) -> None:
    """Добавляет foreign key со ссылкой на supplier_id в таблицу products."""
    # Добавляем колонку supplier_id в products
    cur.execute("ALTER TABLE products ADD COLUMN supplier_id INT;")

    # Проставляем supplier_id у товаров на основе данных из JSON
    suppliers = get_suppliers_data(json_file)
    for supplier in suppliers:
        cur.execute(
            "SELECT supplier_id FROM suppliers WHERE company_name = %s",
            (supplier['company_name'],)
        )
        row = cur.fetchone()
        if row is None:
            continue
        supplier_id = row[0]

        for product_name in supplier.get('products', []):
            cur.execute(
                "UPDATE products SET supplier_id = %s WHERE product_name = %s",
                (supplier_id, product_name)
            )

    # Добавляем внешний ключ
    cur.execute("""
        ALTER TABLE products
        ADD CONSTRAINT fk_products_suppliers
        FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id);
    """)


if __name__ == '__main__':
    main()
