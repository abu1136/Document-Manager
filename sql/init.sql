CREATE DATABASE IF NOT EXISTS document_manager;
USE document_manager;

-- Users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin','user') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document sequence
CREATE TABLE IF NOT EXISTS document_sequence (
    year INT PRIMARY KEY,
    last_number INT NOT NULL
);

-- Documents
CREATE TABLE IF NOT EXISTS documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_number VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(255),
    content TEXT,
    requested_by INT,
    file_pdf VARCHAR(255),
    file_docx VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (requested_by) REFERENCES users(id)
);

-- Letterhead (NEW)
CREATE TABLE IF NOT EXISTS letterhead (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    filetype ENUM('pdf','image') NOT NULL,
    uploaded_by INT,
    active BOOLEAN DEFAULT TRUE,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);
