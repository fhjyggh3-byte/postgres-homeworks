"""Скрипт для заполнения данными таблиц в БД Postgres."""
import csv
import os
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "north",
    "user": "postgres",
    "password": "postgres"
}

DATA_FOLDER = "north_data"


def load_csv_to_table(table_name, file_name, columns):
    """Загружает CSV-файл в указанную таблицу."""
    file_path = os.path.join(DATA_FOLDER, file_name)
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)

            placeholders = ", ".join(["%s"] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

            for row in reader:
                if not row or all(cell.strip() == "" for cell in row):
                    continue
                cleaned_row = [cell if cell.strip() != "" else None for cell in row]
                cur.execute(query, cleaned_row)

        conn.commit()
        print(f"Данные успешно загружены в таблицу '{table_name}'")

    except Exception as e:
        print(f"Ошибка при загрузке {table_name}: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()


if __name__ == "__main__":
    load_csv_to_table(
        table_name="employees",
        file_name="employees_data.csv",
        columns=["employee_id", "first_name", "last_name", "title", "birth_date", "notes"]
    )

    load_csv_to_table(
        table_name="customers",
        file_name="customers_data.csv",
        columns=["customer_id", "company_name", "contact_name"]
    )

    load_csv_to_table(
        table_name="orders",
        file_name="orders_data.csv",
        columns=["order_id", "customer_id", "employee_id", "order_date", "ship_city"]
    )
