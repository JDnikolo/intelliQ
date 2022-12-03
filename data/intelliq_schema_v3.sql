SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

DROP DATABASE IF EXISTS `intelliq` ;
CREATE SCHEMA IF NOT EXISTS `intelliq` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci ;

USE `intelliq` ;

-- -----------------------------------------------------
-- Table Users. Renamed because User is the built-in
-- mySQL table for accounts login previleges etc.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS intelliq.Users (
  username VARCHAR(10) NOT NULL,
  us_password VARCHAR(20) NOT NULL,
  us_role ENUM('Admin','Viewer'),
  access_token VARCHAR(30),
  CHECK (us_role = 'A' OR us_role = 'V'),
  PRIMARY KEY (username))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Questionnaire.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS intelliq.Questionnaire (
  questionnaireID VARCHAR(5) NOT NULL,
  title TINYTEXT NULL,
  created_by VARCHAR(10),
  INDEX quest_idx (created_by ASC) ,
  CONSTRAINT created_by
    	FOREIGN KEY (created_by)
    	REFERENCES intelliq.Users (username)
    	ON DELETE NO ACTION
    	ON UPDATE CASCADE,
  PRIMARY KEY (questionnaireID))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Keywords.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS intelliq.Keywords (
  questionnaireID VARCHAR(5) NOT NULL,
  word VARCHAR(30) NOT NULL,
  INDEX quest_idx (questionnaireID ASC) ,
  CONSTRAINT questionnaireID
    	FOREIGN KEY (questionnaireID)
    	REFERENCES intelliq.Questionnaire (questionnaireID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  PRIMARY KEY (word, questionnaireID))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Question. Increased the question available text
-- from 256 to 65.535 characters.
-- qtext can be null if required is true?
-- changed type field to qtype, since type is a reserved
-- word in mysql
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS intelliq.Question (
  questionID VARCHAR(20) NOT NULL,
  qtext TEXT,
  required BOOLEAN NOT NULL,
  qtype ENUM('question','profile'),
  qnrID VARCHAR(5) NOT NULL,
  INDEX qn_idx (qnrID ASC) ,
  CONSTRAINT qnrID
    	FOREIGN KEY (qnrID)
    	REFERENCES intelliq.Questionnaire (questionnaireID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  PRIMARY KEY (questionID))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Qoption. Renamed since Option is a reserved
-- word
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS intelliq.Qoption (
  optionID VARCHAR(20) NOT NULL,
  optionTXT TINYTEXT NOT NULL,
  nextQ  VARCHAR(20),
  questionID VARCHAR(20),
  INDEX opt_idx1 (questionID ASC) ,
  CONSTRAINT questionID
    	FOREIGN KEY (questionID)
    	REFERENCES intelliq.Question (questionID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  INDEX opt_idx2 (nextQ ASC) ,
  CONSTRAINT nextQ
    	FOREIGN KEY (nextQ)
    	REFERENCES intelliq.Question (questionID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  PRIMARY KEY (optionID))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Answer. Increased the question available text
-- from 256 to 65.535 characters.
-- qtext can be null if required is true?
-- changed type field to qtype, since type is a reserved
-- word in mysql
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS intelliq.Answer (
  answerID VARCHAR(11) NOT NULL,
  sessionID VARCHAR(4) NOT NULL,
  ans_optionID VARCHAR(20) NOT NULL,
  qnrID VARCHAR(5) NOT NULL,
  answertxt TINYTEXT NULL,
  INDEX sess_idx (sessionID ASC) ,
  INDEX opt_idx (ans_optionID ASC) ,
  CONSTRAINT ans_optionID
    	FOREIGN KEY (ans_optionID)
    	REFERENCES intelliq.Qoption (optionID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  INDEX qnr_idx (qnrID ASC) ,
  CONSTRAINT ans_qnrID
    	FOREIGN KEY (qnrID)
    	REFERENCES intelliq.Questionnaire (questionnaireID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  PRIMARY KEY (answerID,sessionID))
ENGINE = InnoDB;
