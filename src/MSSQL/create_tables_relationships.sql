-- Tabela `products_profile`
CREATE TABLE products_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    vending_machine_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machines_profile(id) ON DELETE CASCADE
);

-- Tabela `users_profile`
CREATE TABLE users_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    birthdate DATE,
    phone_number VARCHAR(20),
    address TEXT,
    budget DECIMAL(10, 2) DEFAULT 0
);

-- Tabela `vending_machines_profile`
CREATE TABLE vending_machines_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES owners_profile(id) ON DELETE CASCADE
);

-- Tabela `owners_profile`
CREATE TABLE owners_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ownername VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    birthdate DATE,
    phone_number VARCHAR(20),
    address TEXT,
    budget DECIMAL(10, 2) DEFAULT 0
);

-- Tabela `product_complaint`
CREATE TABLE product_complaint (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);

-- Tabela `product_comment`
CREATE TABLE product_comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);

-- Tabela `purchase_transaction`
CREATE TABLE purchase_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    vending_machine_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL,
    amount_paid_per_unit DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machines_profile(id) ON DELETE CASCADE
);

-- Tabela `vending_machine_complaint`
CREATE TABLE vending_machine_complaint (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    vending_machine_id INT NOT NULL,
    user_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machines_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);

-- Tabela `vending_machine_comment`
CREATE TABLE vending_machine_comment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    vending_machine_id INT NOT NULL,
    user_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machines_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);

-- Tabela `favorite_vending_machines`
CREATE TABLE favorite_vending_machines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vending_machine_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machines_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);

-- Tabela `favorite_products`
CREATE TABLE favorite_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products_profile(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_profile(id) ON DELETE CASCADE
);
