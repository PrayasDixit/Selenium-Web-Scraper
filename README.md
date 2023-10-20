# Selenium-Web-Scraper
Steps to run Script:
1.Lab4_scripts.py
There is only 1 script in this assignment which will take the data from the Reditt API and will do the preprocessing and will save the data in MySQL Server.
Command to run the file : python3 Lab4_scripts.py
Before that we also need to create the database that we are going to use for this assignment by using below commands.
CREATE DATABASE reddit_data;
USE reddit_data;
CREATE TABLE reddit_posts (
post_id INT AUTO_INCREMENT PRIMARY KEY,
title VARCHAR(255),
body TEXT,
author VARCHAR(255),
created_utc DATETIME,
keywords TEXT,
topics TEXT
);



The main Aim of this project is to scrape the data, preprocess it and store it in on-premise My-SQL Database.
