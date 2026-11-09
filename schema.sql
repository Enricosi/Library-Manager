-- Library Manager schema (MySQL 8.0.13+)
-- Usage:
--   mysql -u <user> -p -e "CREATE DATABASE library_manager"
--   mysql -u <user> -p library_manager < schema.sql

CREATE TABLE book (
  book_id        INT NOT NULL AUTO_INCREMENT,
  title          VARCHAR(150) NOT NULL,
  author         VARCHAR(100) NOT NULL,
  genre          VARCHAR(50) NOT NULL,
  published_year INT DEFAULT NULL,
  isbn           VARCHAR(20) DEFAULT NULL,
  created_at     DATE NOT NULL DEFAULT (CURDATE()),
  PRIMARY KEY (book_id),
  UNIQUE KEY isbn (isbn)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE copy (
  copy_id        INT NOT NULL AUTO_INCREMENT,
  book_id        INT NOT NULL,
  status         VARCHAR(20) NOT NULL DEFAULT 'available',
  shelf_location VARCHAR(20) DEFAULT NULL,
  created_at     DATETIME NOT NULL DEFAULT (CURDATE()),
  PRIMARY KEY (copy_id),
  KEY book_id (book_id),
  CONSTRAINT copy_ibfk_1 FOREIGN KEY (book_id) REFERENCES book (book_id),
  CONSTRAINT copy_chk_status CHECK (status IN ('available', 'loaned', 'damaged', 'lost'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE library_user (
  user_id    INT NOT NULL AUTO_INCREMENT,
  username   VARCHAR(50) NOT NULL,
  first_name VARCHAR(20) NOT NULL,
  last_name  VARCHAR(20) NOT NULL,
  is_active  TINYINT(1) NOT NULL DEFAULT '1',
  created_at DATE NOT NULL DEFAULT (CURDATE()),
  PRIMARY KEY (user_id),
  UNIQUE KEY username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE loan (
  loan_id     INT NOT NULL AUTO_INCREMENT,
  copy_id     INT NOT NULL,
  user_id     INT NOT NULL,
  loan_date   DATE NOT NULL DEFAULT (CURDATE()),
  due_date    DATE NOT NULL,
  return_date DATE DEFAULT NULL,
  PRIMARY KEY (loan_id),
  KEY copy_id (copy_id),
  KEY user_id (user_id),
  CONSTRAINT loan_ibfk_1 FOREIGN KEY (copy_id) REFERENCES copy (copy_id),
  CONSTRAINT loan_ibfk_2 FOREIGN KEY (user_id) REFERENCES library_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
