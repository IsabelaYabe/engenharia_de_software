CREATE TABLE IF NOT EXISTS comments (
    id VARCHAR(36) PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS complaints (
    id VARCHAR(36) PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS owners (
    id VARCHAR(36) PRIMARY KEY,
    ownername VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    `first name` VARCHAR(50) NOT NULL, 
    `last name` VARCHAR(50) NOT NULL,
    birthdate DATE,
    `phone number` VARCHAR(20),
    address VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    `first name` VARCHAR(50) NOT NULL, 
    `last name` VARCHAR(50) NOT NULL,
    birthdate DATE,
    `phone number` VARCHAR(20),
    address VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS `vending machine` (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS `add product` (
    id VARCHAR(36) PRIMARY KEY,
    `owner id` VARCHAR(36) UNIQUE NOT NULL,
    `product id` VARCHAR(36) UNIQUE NOT NULL,
    `vending machine id` VARCHAR(36) UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL,
    FOREIGN KEY (`vending machine id`) REFERENCES `vending machine`(id), 
    FOREIGN KEY (`product id`) REFENCES products(id)
    FOREIGN KEY (`owner id`) REFENCES owners(id)
);

CREATE TABLE IF NOT EXISTS `create vending machine` (
    id VARCHAR(36) PRIMARY KEY,
    `owner id` VARCHAR(36) UNIQUE NOT NULL,
    `vending machine id` VARCHAR(36) UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`owner id`) REFERENCES owners(id),
    FOREIGN KEY (`vending machine id`) REFERENCES `vending machine`(id),
);

CREATE TABLE IF NOT EXISTS `favorite vending machine` (
    id VARCHAR(36) PRIMARY KEY,
    `user id` VARCHAR(36) UNIQUE NOT NULL,
    `vending machine id` VARCHAR(36) UNIQUE NOT NULL,
    FOREIGN KEY (`user id`) REFERENCES users(id),
    FOREIGN KEY (`vending machine id`) REFERENCES `vending machine`(id),
);

CREATE TABLE IF NOT EXISTS `product complaints` (
    id VARCHAR(36) PRIMARY KEY,
    `complaint id` VARCHAR(36) NOT NULL,
    `product id` VARCHAR(36) NOT NULL,
    `user id` VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`complaint id`) REFERENCES complaints(id),
    FOREIGN KEY (`product id`) REFERENCES products(id),
    FOREIGN KEY (`user id`) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS `product review` (
    id VARCHAR(36) PRIMARY KEY,
    `comment id` VARCHAR(36) NOT NULL,
    `product id` VARCHAR(36) NOT NULL,
    `user id` VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`comment id`) REFERENCES comments(id),
    FOREIGN KEY (`product id`) REFERENCES products(id),
    FOREIGN KEY (`user id`) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS `purchase transactions` (
    id VARCHAR(36) PRIMARY KEY,
    `user id` VARCHAR(36) UNIQUE NOT NULL,
    `product id` VARCHAR(36) UNIQUE NOT NULL,
    `vending machine id` VARCHAR(36) UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity INT NOT NULL,
    'amount paid per unit' DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (`user id`) REFERENCES users(id),
    FOREIGN KEY (`product id`) REFERENCES products(id),
    FOREIGN KEY (`vending machine id`) REFERENCES `vending machine`(id)
);

CREATE TABLE IF NOT EXISTS `vending machine complaints` (
    id VARCHAR(36) PRIMARY KEY,
    `complaint id` VARCHAR(36) NOT NULL,
    `vending machine id` VARCHAR(36) NOT NULL,
    `user id` VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`complaint id`) REFERENCES complaints(id),
    FOREIGN KEY (`vending machine id`) REFERENCES `vending machine`(id),
    FOREIGN KEY (`user id`) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS `vending machine review` (
    id VARCHAR(36) PRIMARY KEY,
    `comment id` VARCHAR(36) NOT NULL,
    `vending machine id` VARCHAR(36) NOT NULL,
    `user id` VARCHAR(36) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`comment id`) REFERENCES comments(id),
    FOREIGN KEY (`vending machine id`) REFERENCES `vending machine`(id),
    FOREIGN KEY (`user id`) REFERENCES users(id)
);