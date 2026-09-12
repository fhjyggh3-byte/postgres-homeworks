CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_date DATE,
    notes TEXT
);

CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(100),
    contact_name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(10) REFERENCES customers(customer_id),
    employee_id INT REFERENCES employees(employee_id),
    order_date DATE,
    amount NUMERIC(10, 2)
);-- SQL-команды для создания таблиц
