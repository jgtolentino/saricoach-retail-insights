CREATE SCHEMA IF NOT EXISTS saricoach;


        CREATE TABLE IF NOT EXISTS saricoach.brands (
            brand_id INT PRIMARY KEY,
            brand_name TEXT,
            category TEXT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.products (
            product_id INT PRIMARY KEY,
            sku TEXT,
            barcode TEXT,
            brand_id INT,
            product_name TEXT,
            category TEXT,
            pack_size TEXT,
            pack_type TEXT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.stores (
            product_name TEXT,
            category TEXT,
            pack_size TEXT,
            pack_type TEXT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.stores (
            store_id INT PRIMARY KEY,
            store_name TEXT,
            region TEXT,
            city TEXT,
            barangay TEXT,
            store_type TEXT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.transactions (
            transaction_id TEXT PRIMARY KEY,
            store_id INT,
            tx_timestamp TIMESTAMP,
            total_amount FLOAT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.transaction_lines (
            transaction_id TEXT,
            line_no INT,
            product_id INT,
            brand_id INT,
            quantity INT,
            price_unit FLOAT,
            subtotal FLOAT,
            PRIMARY KEY (transaction_id, line_no)
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.shelf_vision_events (
            id TEXT PRIMARY KEY,
            store_id INT,
            event_timestamp TIMESTAMP,
            brand_id INT,
            facings INT,
            share_of_shelf FLOAT,
            oos_flag BOOLEAN,
            confidence FLOAT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.stt_events (
            id TEXT PRIMARY KEY,
            store_id INT,
            event_timestamp TIMESTAMP,
            brand_id INT,
            raw_text TEXT,
            intent_label TEXT,
            sentiment_score FLOAT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.weather_daily (
            id TEXT PRIMARY KEY,
            store_id INT,
            date DATE,
            temp_c FLOAT,
            rainfall_mm FLOAT,
            condition TEXT
        );
        
        CREATE TABLE IF NOT EXISTS saricoach.foot_traffic_daily (
            id TEXT PRIMARY KEY,
            store_id INT,
            date DATE,
            traffic_index FLOAT
        );
        
INSERT INTO saricoach.brands (brand_id, brand_name, category) VALUES
(1, 'Test Brand', 'Snacks');

INSERT INTO saricoach.products (product_id, sku, barcode, brand_id, product_name, category, pack_size, pack_type) VALUES
(101, '101', '4800000000101', 1, 'Test Product', 'Snacks', '1 unit', 'pack');

INSERT INTO saricoach.stores (store_id, store_name, region, city, barangay, store_type) VALUES
(1, 'Aling Nena Sari-Sari Store #1 – Manila', 'NCR', 'Manila', 'Barangay 1', 'sari-sari');

INSERT INTO saricoach.transactions (transaction_id, store_id, tx_timestamp, total_amount) VALUES
('ord1', 1, '2025-12-01T23:17:47.208752', 30);

INSERT INTO saricoach.transaction_lines (transaction_id, line_no, product_id, brand_id, quantity, price_unit, subtotal) VALUES
('ord1', 1, 101, 1, 2, 15, 30);

INSERT INTO saricoach.shelf_vision_events (id, store_id, event_timestamp, brand_id, facings, share_of_shelf, oos_flag, confidence) VALUES
('55cc1958-2489-47a9-bb03-f3c9a3ec2cc1', 1, '2025-12-01T08:00:00', 1, 3, 1.0, False, 0.9513431675034443);

INSERT INTO saricoach.weather_daily (id, store_id, date, temp_c, rainfall_mm, condition) VALUES
('13a31d24-96ef-4d99-920c-dc5b4e8bbc9c', 1, '2025-12-01', 30.7, 0.0, 'Cloudy');

INSERT INTO saricoach.foot_traffic_daily (id, store_id, date, traffic_index) VALUES
('067b5717-0dfd-43fb-b37e-a676f8a8f30b', 1, '2025-12-01', 113.7);

