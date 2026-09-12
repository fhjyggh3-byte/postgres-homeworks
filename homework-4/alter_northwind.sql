-- Подключиться к БД Northwind и сделать следующие изменения:

-- 1. Добавить ограничение на поле unit_price таблицы products (цена должна быть больше 0)
ALTER TABLE products DROP CONSTRAINT IF EXISTS chk_unit_price_positive;
ALTER TABLE products ADD CONSTRAINT chk_unit_price_positive CHECK (unit_price > 0);

-- 2. Добавить ограничение, что поле discontinued таблицы products может содержать только значения 0 или 1
ALTER TABLE products DROP CONSTRAINT IF EXISTS chk_discontinued_values;
ALTER TABLE products ADD CONSTRAINT chk_discontinued_values CHECK (discontinued IN (0, 1));

-- 3. Создать новую таблицу, содержащую все продукты, снятые с продажи (discontinued = 1)
DROP TABLE IF EXISTS discontinued_products;
CREATE TABLE discontinued_products AS
SELECT * FROM products WHERE discontinued = 1;

-- 4. Удалить из products товары, снятые с продажи (discontinued = 1)
-- Сначала удаляем связанные записи из order_details, чтобы не нарушить foreign key
DELETE FROM order_details
WHERE product_id IN (SELECT product_id FROM products WHERE discontinued = 1);

-- Теперь удаляем сами продукты
DELETE FROM products WHERE discontinued = 1;
