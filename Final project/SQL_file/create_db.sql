CREATE DATABASE IF NOT EXISTS anime_db;

USE anime_db;


CREATE TABLE IF NOT EXISTS anime (
    id INT PRIMARY KEY,               
    title_romaji VARCHAR(255),         
    description TEXT                   
);

-- Create the genres table if it doesn't exist
CREATE TABLE IF NOT EXISTS genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,  
    anime_id INT,                             
    genre VARCHAR(100),                       
    FOREIGN KEY (anime_id) REFERENCES anime(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS animes (
    ID INT PRIMARY KEY,
    Title VARCHAR(255),
    Recap TEXT,
    Noun TEXT,
    Verb TEXT,
    Adj TEXT
)