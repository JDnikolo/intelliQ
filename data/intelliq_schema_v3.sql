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
  us_role VARCHAR(1),
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
  qtype VARCHAR (8),
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
/*
-- -----------------------------------------------------
-- Table Ans_opt. Shows the many-to-many relation
-- between Answer and Qoption
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS intelliq.Ans_opt (
  ansID VARCHAR(11) NOT NULL,
  qoptID VARCHAR(20) NOT NULL,
  INDEX ans_idx (ansID ASC) ,
  CONSTRAINT ansID
    	FOREIGN KEY (ansID)
    	REFERENCES intelliq.Answer (answerID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  INDEX qopt_idx (qoptID ASC) ,
  CONSTRAINT qoptID
    	FOREIGN KEY (qoptID)
    	REFERENCES intelliq.Qoption (optionID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  PRIMARY KEY (ansID,qoptID))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Answer_text. Expresses the generalisation of 
-- the Answer table to text answers
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS intelliq.Answer_text (
  ansID VARCHAR(11) NOT NULL,
  sessionID VARCHAR(4) NOT NULL,
  answer_text TEXT,
  INDEX ans_idx (ansID ASC) ,
  CONSTRAINT txt_ansID
    	FOREIGN KEY (ansID)
    	REFERENCES intelliq.Answer (answerID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  INDEX sess_idx (sessionID ASC) ,
  CONSTRAINT ans_txt_sessionID
    	FOREIGN KEY (sessionID)
    	REFERENCES intelliq.Answer (sessionID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  PRIMARY KEY (ansID,sessionID))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Answer_text. Expresses the generalisation of 
-- the Answer table to multiple choice answers
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS intelliq.Answer_mc (
  ansID VARCHAR(11) NOT NULL,
  sessionID VARCHAR(4) NOT NULL,
  choiceID VARCHAR(1),
  INDEX ans_idx (ansID ASC) ,
  CONSTRAINT mc_ansID
    	FOREIGN KEY (ansID)
    	REFERENCES intelliq.Answer (answerID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  INDEX sess_idx (sessionID ASC) ,
  CONSTRAINT mc_sessionID
    	FOREIGN KEY (sessionID)
    	REFERENCES intelliq.Answer (sessionID)
    	ON DELETE CASCADE
    	ON UPDATE CASCADE,
  PRIMARY KEY (ansID,sessionID))
ENGINE = InnoDB;
*/
-- -----------------------------------------------------
-- Table Has_questions. Shows the one-to-many relation
-- between Questionnaire and Question
-- ATTENTION One-to-Many relationships with total 
-- participation on the many side can be modelled 
-- by just adding the dominating entity's 
-- primary key on the dominated entity
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS intelliq.Has_questions (
--  qnrID VARCHAR(5) NOT NULL,
--  qID VARCHAR(10) NOT NULL,
--  INDEX hq_idx1 (qnrID ASC) ,
--  CONSTRAINT qnrID
--    	FOREIGN KEY (qnrID)
--    	REFERENCES intelliq.Questionnaire (questionnaireID)
--    	ON DELETE CASCADE
--    	ON UPDATE CASCADE,
--  INDEX hq_idx2 (qID ASC) ,
--  CONSTRAINT qID
--    	FOREIGN KEY (qID)
--    	REFERENCES intelliq.Question (questionID)
--    	ON DELETE CASCADE
--    	ON UPDATE CASCADE,
--  PRIMARY KEY (qnrID,qID))
-- ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table Has_options. Shows the one-to-many relation
-- between Questionnaire and Question. It is not needed
-- since one-to-one relationships can be modelled with 
-- either side acting as the many side which is 
-- equivalant with a one to many relationship with a
-- one to many relationship with partial cardinality 
-- -----------------------------------------------------
-- CREATE TABLE IF NOT EXISTS intelliq.Has_questions (
--  qnrID VARCHAR(5) NOT NULL,
--  qID VARCHAR(10) NOT NULL,
--  INDEX hq_idx1 (qnrID ASC) ,
--  CONSTRAINT qnrID
--    	FOREIGN KEY (qnrID)
--    	REFERENCES intelliq.Questionnaire (questionnaireID)
--    	ON DELETE CASCADE
--    	ON UPDATE CASCADE,
--  INDEX hq_idx2 (qID ASC) ,
--  CONSTRAINT qID
--    	FOREIGN KEY (qID)
--    	REFERENCES intelliq.Question (questionID)
--    	ON DELETE CASCADE
--    	ON UPDATE CASCADE,
--  PRIMARY KEY (qnrID,qID))
-- ENGINE = InnoDB;
