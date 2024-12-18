-- Tabela `owners_profile`
CREATE TABLE IF NOT EXISTS owners_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    birthdate DATE,
    phone_number VARCHAR(20),
    address TEXT,
    budget FLOAT DEFAULT 0
);

-- Tabela `users_profile`
CREATE TABLE IF NOT EXISTS users_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    birthdate DATE,
    phone_number VARCHAR(20),
    address TEXT,
    budget FLOAT DEFAULT 0
);

-- Tabela `vending_machines_profile`
CREATE TABLE IF NOT EXISTS vending_machines_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    budget FLOAT DEFAULT 0,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES owners_profile(id) ON DELETE CASCADE
);

-- Tabela `products_profile`
CREATE TABLE IF NOT EXISTS products_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    quantity INT NOT NULL,
    vending_machine_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machines_profile(id) ON DELETE CASCADE
);

-- Tabela `product_complaint`
CREATE TABLE IF NOT EXISTS product_complaint (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);

-- Tabela `product_comment`
CREATE TABLE IF NOT EXISTS product_comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);

-- Tabela `purchase_transaction`
CREATE TABLE IF NOT EXISTS purchase_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    vending_machine_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL,
    amount_paid_per_unit FLOAT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machines_profile(id) ON DELETE CASCADE
);

-- Tabela `vending_machine_complaint`
CREATE TABLE IF NOT EXISTS vending_machine_complaint (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    vending_machine_id INT NOT NULL,
    user_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machines_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);

-- Tabela `vending_machine_comment`
CREATE TABLE IF NOT EXISTS vending_machine_comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    vending_machine_id INT NOT NULL,
    user_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machines_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);

-- Tabela `favorite_vending_machines`
CREATE TABLE IF NOT EXISTS favorite_vending_machines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vending_machine_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machines_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);

-- Tabela `favorite_products`
CREATE TABLE IF NOT EXISTS favorite_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);
