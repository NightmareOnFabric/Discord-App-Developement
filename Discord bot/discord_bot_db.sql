CREATE DATABASE discord_bot_db;

USE discord_bot_db;


CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    discord_id VARCHAR(20) UNIQUE NOT NULL,
    username VARCHAR(100),
    score INT DEFAULT 0,
    messages TEXT,
    messages0 TEXT,
    messages1 TEXT,
    messages2 TEXT,
    messages3 TEXT,
    messages4 TEXT,
    messages5 TEXT,
    messages6 TEXT,
    messages7 TEXT,
    messages8 TEXT,
    messages9 TEXT
);

CREATE TABLE IF NOT EXISTS user_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(45) NOT NULL,
    servidor VARCHAR(255) NOT NULL,
    canal VARCHAR(255) NOT NULL,
	username VARCHAR(255) NOT NULL,
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

