DROP DATABASE IF EXISTS WikipediaDataMining;
CREATE DATABASE WikipediaDataMining;
USE WikipediaDataMining;

CREATE TABLE person (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    day_of_birth DATE,
    day_of_death DATE,
    age INT(10)
);

DELIMITER //
CREATE TRIGGER calc_age BEFORE INSERT ON person
FOR EACH ROW
BEGIN
SET NEW.age = YEAR(NEW.day_of_death) - YEAR(NEW.day_of_birth);
END; //
DELIMITER ;
