-- Run this once against your MySQL server to create the database and table
-- used by chat_storage.py / database.py.
--
-- Usage:
--   mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS chatbot_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE chatbot_db;

CREATE TABLE IF NOT EXISTS chat_history (
  id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_message  TEXT NOT NULL,
  bot_response  TEXT NOT NULL,
  model_used    VARCHAR(100) NOT NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

  INDEX idx_created_at (created_at),
  INDEX idx_model_used (model_used)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
