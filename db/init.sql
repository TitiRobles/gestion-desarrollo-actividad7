-- Base de datos Actividad 7
-- Equipo: Tiago, Joaquin, Juan Pablo y Rodrigo

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL
);

INSERT INTO usuarios (nombre, email) VALUES
('Tiago', 'tiago@ejemplo.com'),
('Joaquin', 'joaquin@ejemplo.com'),
('Juan Pablo', 'juanpablo@ejemplo.com'),
('Rodrigo', 'rodrigo@ejemplo.com');