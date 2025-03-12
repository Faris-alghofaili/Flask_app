-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8mb3 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`user` (
  `User_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `Username` VARCHAR(50) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `password_hash` TINYTEXT NOT NULL,
  `is_admin` TINYINT NOT NULL,
  `created_at` DATE NOT NULL,
  PRIMARY KEY (`User_id`),
  UNIQUE INDEX `User_id_UNIQUE` (`User_id` ASC) VISIBLE,
  UNIQUE INDEX `Username_UNIQUE` (`Username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`voices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`voices` (
  `voice_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `description` TINYTEXT NULL DEFAULT NULL,
  `file_path` TINYTEXT NOT NULL,
  `created_at` DATE NOT NULL,
  PRIMARY KEY (`voice_id`),
  UNIQUE INDEX `voice_id_UNIQUE` (`voice_id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`quranversions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`quranversions` (
  `Version_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `language` VARCHAR(50) NOT NULL,
  `description` TINYTEXT NULL DEFAULT NULL,
  `created_at` DATE NOT NULL,
  PRIMARY KEY (`Version_id`),
  UNIQUE INDEX `Version_id_UNIQUE` (`Version_id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Projects`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Projects` (
  `Project_id` INT NOT NULL AUTO_INCREMENT,
  `User_id` INT NOT NULL,
  `name` VARCHAR(50) NOT NULL,
  `voice_id` INT NOT NULL,
  `quranversions_Version_id` INT NOT NULL,
  PRIMARY KEY (`Project_id`, `User_id`),
  UNIQUE INDEX `Project_id_UNIQUE` (`Project_id` ASC) VISIBLE,
  INDEX `fk_Projects_user1_idx` (`User_id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE,
  INDEX `fk_Projects_voices1_idx` (`voice_id` ASC) VISIBLE,
  INDEX `fk_Projects_quranversions1_idx` (`quranversions_Version_id` ASC) VISIBLE,
  CONSTRAINT `fk_Projects_user1`
    FOREIGN KEY (`User_id`)
    REFERENCES `mydb`.`user` (`User_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Projects_voices1`
    FOREIGN KEY (`voice_id`)
    REFERENCES `mydb`.`voices` (`voice_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Projects_quranversions1`
    FOREIGN KEY (`quranversions_Version_id`)
    REFERENCES `mydb`.`quranversions` (`Version_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`audiorequests`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`audiorequests` (
  `request_id` INT NOT NULL AUTO_INCREMENT,
  `status` VARCHAR(20) NOT NULL,
  `audio_file_path` TINYTEXT NOT NULL,
  `requested_at` DATETIME NOT NULL,
  `completed_at` DATETIME NULL DEFAULT NULL,
  `start_verse` INT NOT NULL,
  `end_verse` INT NOT NULL,
  `inculde_tags` TINYINT NOT NULL,
  `Projects_id` INT NOT NULL,
  `Projects_user_User_id` INT NOT NULL,
  PRIMARY KEY (`request_id`, `Projects_id`, `Projects_user_User_id`),
  UNIQUE INDEX `request_id_UNIQUE` (`request_id` ASC) VISIBLE,
  INDEX `fk_audiorequests_Projects1_idx` (`Projects_id` ASC, `Projects_user_User_id` ASC) VISIBLE,
  CONSTRAINT `fk_audiorequests_Projects1`
    FOREIGN KEY (`Projects_id` , `Projects_user_User_id`)
    REFERENCES `mydb`.`Projects` (`Project_id` , `User_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`surahs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`surahs` (
  `sutrah_id` INT NOT NULL AUTO_INCREMENT,
  `surah_number` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `arabic_name` VARCHAR(255) NOT NULL,
  `number_of_ayahs` INT NOT NULL,
  `QuranVersions_Version_id` INT NOT NULL,
  PRIMARY KEY (`sutrah_id`, `QuranVersions_Version_id`),
  UNIQUE INDEX `sutrah_id_UNIQUE` (`sutrah_id` ASC) VISIBLE,
  INDEX `fk_Surahs_QuranVersions1_idx` (`QuranVersions_Version_id` ASC) VISIBLE,
  CONSTRAINT `fk_Surahs_QuranVersions1`
    FOREIGN KEY (`QuranVersions_Version_id`)
    REFERENCES `mydb`.`quranversions` (`Version_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`tag`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tag` (
  `tag_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` TINYTEXT NULL DEFAULT NULL,
  PRIMARY KEY (`tag_id`),
  UNIQUE INDEX `sutrah_id_UNIQUE` (`tag_id` ASC) VISIBLE,
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`verses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`verses` (
  `verse_id` INT NOT NULL AUTO_INCREMENT,
  `verse_number` INT NOT NULL,
  `text` MEDIUMTEXT NOT NULL,
  `Surahs_sutrah_id` INT NOT NULL,
  PRIMARY KEY (`verse_id`, `Surahs_sutrah_id`),
  UNIQUE INDEX `verse_id_UNIQUE` (`verse_id` ASC) VISIBLE,
  INDEX `fk_verses_Surahs1_idx` (`Surahs_sutrah_id` ASC) VISIBLE,
  CONSTRAINT `fk_verses_Surahs1`
    FOREIGN KEY (`Surahs_sutrah_id`)
    REFERENCES `mydb`.`surahs` (`sutrah_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`versetags`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`versetags` (
  `verse_tag_id` INT NOT NULL AUTO_INCREMENT,
  `start_word_index` INT NOT NULL,
  `end_word_index` INT NOT NULL,
  `created_at` DATE NOT NULL,
  `verses_verse_id` INT NOT NULL,
  `tag_tag_id` INT NOT NULL,
  `Projects_Project_id` INT NOT NULL,
  `Projects_User_id` INT NOT NULL,
  PRIMARY KEY (`verse_tag_id`, `verses_verse_id`, `tag_tag_id`),
  UNIQUE INDEX `sutrah_id_UNIQUE` (`verse_tag_id` ASC) VISIBLE,
  INDEX `fk_verseTags_verses1_idx` (`verses_verse_id` ASC) VISIBLE,
  INDEX `fk_versetags_tag1_idx` (`tag_tag_id` ASC) VISIBLE,
  INDEX `fk_versetags_Projects1_idx` (`Projects_Project_id` ASC, `Projects_User_id` ASC) VISIBLE,
  CONSTRAINT `fk_verseTags_verses1`
    FOREIGN KEY (`verses_verse_id`)
    REFERENCES `mydb`.`verses` (`verse_id`),
  CONSTRAINT `fk_versetags_tag1`
    FOREIGN KEY (`tag_tag_id`)
    REFERENCES `mydb`.`tag` (`tag_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_versetags_Projects1`
    FOREIGN KEY (`Projects_Project_id` , `Projects_User_id`)
    REFERENCES `mydb`.`Projects` (`Project_id` , `User_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
