CREATE TABLE users(
    email varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    name    varchar(255) NOT NULL,
    phone varchar(225) NOT NULL,
    privilege   varchar(15) NOT NULL 
        CHECK (type in ('admin', 'user')),
    PRIMARY KEY(email)
);

