CREATE DATABASE IF NOT EXISTS anime_db;

USE anime_db;

CREATE TABLE IF NOT EXISTS animes (
    ID INT PRIMARY KEY,
    Title VARCHAR(255),
    Recap TEXT,
    Genres TEXT,
    Noun LONGTEXT,
    Verb LONGTEXT,
    Adj LONGTEXT
)

-- CREATE TABLE IF NOT EXISTS anime_noun (
--     ID INT PRIMARY KEY,
--     Title VARCHAR(255),
--     term_sets TEXT,
--     terms TEXT,
--     term_map TEXT,
--     count_maps TEXT
-- )

-- CREATE TABLE IF NOT EXISTS anime_verb (
--     ID INT PRIMARY KEY,
--     Title VARCHAR(255),
--     term_sets TEXT,
--     terms TEXT,
--     term_map TEXT,
--     count_maps TEXT
-- )

-- CREATE TABLE IF NOT EXISTS anime_adj (
--     ID INT PRIMARY KEY,
--     Title VARCHAR(255),
--     term_sets TEXT,
--     terms TEXT,
--     term_map TEXT,
--     count_maps TEXT
-- )