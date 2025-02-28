DROP DATABASE IF EXISTS flask_api;

CREATE DATABASE flask_api;

USE flask_api;

CREATE TABLE users(
    id INT SIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    edad INT,
    numero VARCHAR(12),
    genero VARCHAR(15)
);