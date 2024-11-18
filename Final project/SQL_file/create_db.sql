CREATE DATABASE IF NOT EXISTS anime_db;

USE anime_db;

CREATE TABLE IF NOT EXISTS animes_nltk (
    ID INT PRIMARY KEY,
    Title VARCHAR(255),
    Recap TEXT,
    Genres TEXT,
    Noun LONGTEXT,
    Verb LONGTEXT,
    Adj LONGTEXT,
    NA LONGTEXT
);

CREATE TABLE IF NOT EXISTS animes_spacy (
    ID INT PRIMARY KEY,
    Title VARCHAR(255),
    Recap TEXT,
    Genres TEXT,
    Noun LONGTEXT,
    Verb LONGTEXT,
    Adj LONGTEXT,
    NA LONGTEXT
);
