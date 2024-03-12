-- Creacion de la base de datos si no existe
CREATE DATABASE IF NOT EXISTS pbd1;
USE pbd1;

-- Creación de la tabla de anuncios (ads)

CREATE TABLE ads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    external_id VARCHAR(255) NOT NULL,
    post_date DATE,
    make VARCHAR(50),
    model VARCHAR(50),
    trimlevel VARCHAR(50),
    car_year INT,
    fueltype VARCHAR(50),
    transmission VARCHAR(50),
    km INT,
    bodytype VARCHAR(50),
    horse_power VARCHAR(50),
    cyl_capacity VARCHAR(50),
    traction VARCHAR(50),
    price INT,
    warranty VARCHAR(50),
    plate_type VARCHAR(50),
    ad_type VARCHAR(50),
    video_call_visible VARCHAR(50),
    status VARCHAR(50),
    dealer_name VARCHAR(255),
    car_location VARCHAR(255),
    trade_in_flag BOOLEAN,
    region VARCHAR(50),
    car_name VARCHAR(255),
    url VARCHAR(255),
    seller_gallery_url VARCHAR(255),
    seller_phone_number VARCHAR(50),
    damages TINYINT,
    color VARCHAR(50),
    misc TINYINT,
    UNIQUE (external_id)
);

-- Creación de la tabla de vendedores (sellers)
CREATE TABLE sellers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dealer_name VARCHAR(255) NOT NULL,
    seller_gallery_url VARCHAR(255),
    contact_phone VARCHAR(50),
    UNIQUE (dealer_name)
);