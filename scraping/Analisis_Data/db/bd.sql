-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS cuscotrends 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE cuscotrends;

-- Eliminar la tabla reviews y usuarios si ya existen
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS usuarios;

-- Crear la tabla usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- ID auto-incremental, clave primaria
    nombre VARCHAR(100) NOT NULL,       -- Nombre del usuario
    email VARCHAR(100) NOT NULL,        -- Email del usuario, obligatorio y único
    password VARCHAR(255) NOT NULL,     -- Contraseña, obligatoria
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  -- Fecha de actualización automática
) ENGINE=InnoDB;

-- Crear la tabla reviews sin la cláusula CHECK para evitar problemas en MariaDB
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,  -- ID auto-incremental, clave primaria
    tour_title VARCHAR(255) NOT NULL,   -- Título del tour, obligatorio
    source VARCHAR(50) NOT NULL,        -- Fuente (TripAdvisor, Trustpilot, etc.), obligatorio
    opinion_count INT DEFAULT NULL,     -- Número de opiniones totales, puede ser NULL
    rating FLOAT DEFAULT NULL,          -- Calificación, puede ser NULL
    estrellas_5 FLOAT DEFAULT NULL,     -- Porcentaje de 5 estrellas, puede ser NULL
    estrellas_4 FLOAT DEFAULT NULL,     -- Porcentaje de 4 estrellas, puede ser NULL
    estrellas_3 FLOAT DEFAULT NULL,     -- Porcentaje de 3 estrellas, puede ser NULL
    estrellas_2 FLOAT DEFAULT NULL,     -- Porcentaje de 2 estrellas, puede ser NULL
    estrellas_1 FLOAT DEFAULT NULL,     -- Porcentaje de 1 estrella, puede ser NULL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Fecha de creación
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,  -- Fecha de actualización
    usuario_id INT,  -- Relación con la tabla usuarios
    CONSTRAINT fk_usuario
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE  -- Si el usuario se elimina, se eliminan sus reviews
) ENGINE=InnoDB;
