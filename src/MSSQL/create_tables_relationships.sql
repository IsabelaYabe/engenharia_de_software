CREATE TABLE IF NOT EXISTS comments_profile (
    id VARCHAR(36) PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS complaints_profile (
    id VARCHAR(36) PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS owners_profile (
    id VARCHAR(36) PRIMARY KEY,
    ownername VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL, 
    filast_name VARCHAR(50) NOT NULL,
    birthdate DATE,
    phone_number VARCHAR(20),
    address VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS products_profile (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS users_profile (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL, 
    last_name VARCHAR(50) NOT NULL,
    birthdate DATE,
    phone_number VARCHAR(20),
    address VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS vending_machines_profile (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS add_product (
    id VARCHAR(36) PRIMARY KEY,
    owner_id VARCHAR(36) UNIQUE NOT NULL,
    product_id VARCHAR(36) UNIQUE NOT NULL,
    vending_machine_id VARCHAR(36) UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL,
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machine(id), 
    FOREIGN KEY (product_id) REFENCES products(id)
    FOREIGN KEY (owner_id) REFENCES owners(id)
);

CREATE TABLE IF NOT EXISTS create_vending_machine (
    id VARCHAR(36) PRIMARY KEY,
    owner_id VARCHAR(36) UNIQUE NOT NULL,
    vending_machine_id VARCHAR(36) UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owners(id),
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machine(id),
);

CREATE TABLE IF NOT EXISTS favorite_vending_machine (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) UNIQUE NOT NULL,
    vending_machine_id VARCHAR(36) UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machine(id),
);

CREATE TABLE IF NOT EXISTS product_complaint (
    id VARCHAR(36) PRIMARY KEY,
    complaint_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS product_review (
    id VARCHAR(36) PRIMARY KEY,
    comment_id VARCHAR(36) NOT NULL,
    product_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comment_id) REFERENCES comments(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS purchase_transaction (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) UNIQUE NOT NULL,
    product_id VARCHAR(36) UNIQUE NOT NULL,
    vending_machine_id VARCHAR(36) UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL,
    amount_paid_per_unit DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machine(id)
);

CREATE TABLE IF NOT EXISTS vending_machine_complaint (
    id VARCHAR(36) PRIMARY KEY,
    complaint_id VARCHAR(36) NOT NULL,
    vending_machine_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (complaint_id) REFERENCES complaints(id),
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machine(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS vending_machine_review (
    id VARCHAR(36) PRIMARY KEY,
    comment_id VARCHAR(36) NOT NULL,
    vending_machine_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (comment_id) REFERENCES comments(id),
    FOREIGN KEY (vending_machine_id) REFERENCES vending_machine(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);