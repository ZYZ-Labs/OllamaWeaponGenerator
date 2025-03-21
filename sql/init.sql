-- sql/init.sql
CREATE DATABASE IF NOT EXISTS weapon_db;
USE weapon_db;

-- 用户表：保存用户信息
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 武器表：保存生成的武器数据
CREATE TABLE IF NOT EXISTS weapons (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  type VARCHAR(50),
  name VARCHAR(100),
  attributes JSON,
  effects JSON,
  skills JSON,
  background TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
