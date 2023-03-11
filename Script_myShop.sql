-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema MyTienda
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `MyTienda` ;

-- -----------------------------------------------------
-- Schema MyTienda
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `MyTienda` DEFAULT CHARACTER SET utf8 ;
USE `MyTienda` ;

-- -----------------------------------------------------
-- Table `MyTienda`.`Shops`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MyTienda`.`Shops` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  `email_shop` VARCHAR(200) NULL,
  `password` VARCHAR(250) NULL,
  `category` VARCHAR(45) NULL,
  `description_shop` VARCHAR(250) NULL,
  `color` VARCHAR(45) NULL,
  `logo_img` VARCHAR(50) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MyTienda`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MyTienda`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(100) NULL,
  `last_name` VARCHAR(100) NULL,
  `email` VARCHAR(250) NULL,
  `password` VARCHAR(250) NULL,
  `direction` VARCHAR(150) NULL,
  `profile_img` VARCHAR(50) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MyTienda`.`Products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MyTienda`.`Products` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NULL,
  `description_pro` VARCHAR(250) NULL,
  `price` INT NULL,
  `status` TINYINT(1) NULL,
  `img` TEXT(3000) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `shop_id` INT NOT NULL,
  PRIMARY KEY (`id`, `shop_id`),
  INDEX `fk_Products_Shops1_idx` (`shop_id` ASC) VISIBLE,
  CONSTRAINT `fk_Products_Shops1`
    FOREIGN KEY (`shop_id`)
    REFERENCES `MyTienda`.`Shops` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MyTienda`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MyTienda`.`orders` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `valor_total` INT NULL,
  `direction2` VARCHAR(60) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_orders_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_orders_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `MyTienda`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MyTienda`.`Orders_Products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MyTienda`.`Orders_Products` (
  `order_id` INT NOT NULL,
  `Product_id` INT NOT NULL,
  `cantidad` INT NULL,
  PRIMARY KEY (`order_id`, `Product_id`),
  INDEX `fk_Products_has_orders_orders1_idx` (`order_id` ASC) VISIBLE,
  INDEX `fk_Products_has_orders_Products1_idx` (`Product_id` ASC) VISIBLE,
  CONSTRAINT `fk_Products_has_orders_Products1`
    FOREIGN KEY (`Product_id`)
    REFERENCES `MyTienda`.`Products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Products_has_orders_orders1`
    FOREIGN KEY (`order_id`)
    REFERENCES `MyTienda`.`orders` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MyTienda`.`favs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MyTienda`.`favs` (
  `user_id` INT NOT NULL,
  `Product_id` INT NOT NULL,
  `on_off` TINYINT(1) NULL,
  PRIMARY KEY (`user_id`, `Product_id`),
  INDEX `fk_users_has_Products_Products1_idx` (`Product_id` ASC) VISIBLE,
  INDEX `fk_users_has_Products_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_Products_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `MyTienda`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_Products_Products1`
    FOREIGN KEY (`Product_id`)
    REFERENCES `MyTienda`.`Products` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MyTienda`.`proposal`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MyTienda`.`proposal` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NULL,
  `description_pro` VARCHAR(250) NULL,
  `img` TEXT(3000) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `shop_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_propuesta_Shops1_idx` (`shop_id` ASC) VISIBLE,
  INDEX `fk_propuesta_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_propuesta_Shops1`
    FOREIGN KEY (`shop_id`)
    REFERENCES `MyTienda`.`Shops` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_propuesta_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `MyTienda`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `MyTienda`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `MyTienda`.`votes` (
  `propuesta_id` INT NOT NULL,
  `user_vote_id` INT NOT NULL,
  PRIMARY KEY (`propuesta_id`, `user_vote_id`),
  INDEX `fk_propuesta_has_users_users1_idx` (`user_vote_id` ASC) VISIBLE,
  INDEX `fk_propuesta_has_users_propuesta1_idx` (`propuesta_id` ASC) VISIBLE,
  CONSTRAINT `fk_propuesta_has_users_propuesta1`
    FOREIGN KEY (`propuesta_id`)
    REFERENCES `MyTienda`.`proposal` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_propuesta_has_users_users1`
    FOREIGN KEY (`user_vote_id`)
    REFERENCES `MyTienda`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
