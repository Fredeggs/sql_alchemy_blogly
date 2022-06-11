-- from the terminal run:
-- psql < music.sql

DROP DATABASE IF EXISTS blogly_db;

CREATE DATABASE blogly_db;

\c blogly_db

DROP TABLE users;

CREATE TABLE users
(
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  image_url VARCHAR(255) NOT NULL DEFAULT 'https://thumbs.dreamstime.com/b/default-avatar-profile-image-vector-social-media-user-icon-potrait-182347582.jpg'
);

INSERT INTO users 
(first_name, last_name, image_url)
VALUES 
('Fred', 'Bobson', DEFAULT),
('Michelle', 'Obama', 'https://www.history.com/.image/ar_4:3%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTc5MzY2ODYwNDIzMTc3NTQ5/michelle-obama-gettyimages-1138043297.jpg');

