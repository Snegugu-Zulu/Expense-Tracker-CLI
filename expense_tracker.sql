CREATE DATABASE IF NOT EXISTS expense_tracker;
USE expense_tracker;

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    category_id INT,
    expense_date DATE NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

INSERT IGNORE INTO categories (name) VALUES 
    ('Food'),
    ('Transport'),
    ('Entertainment'),
    ('Bills'),
    ('Shopping'),
    ('Healthcare'),
    ('Other');