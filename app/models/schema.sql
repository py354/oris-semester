create table if not exists users (
    ID SERIAL PRIMARY KEY,
    Login TEXT NOT NULL,
    Password TEXT NOT NULL,
    Cart INTEGER[] DEFAULT '{}',
    Email TEXT,
    IsAdmin BOOLEAN DEFAULT FALSE,
    PhotoFilename TEXT
);
create index if not exists login_index on users (login);

create table if not exists items (
    ID SERIAL PRIMARY KEY,
    Name TEXT NOT NULL,
    Description TEXT NOT NULL,
    Server TEXT NOT NULL,
    PenniesPrice INT NOT NULL,

    CountLeft INT DEFAULT -1,
    PhotoFilename TEXT,
    IsDeleted BOOLEAN DEFAULT FALSE
);

create table if not exists orders (
    ID SERIAL PRIMARY KEY ,
    UID INTEGER NOT NULL ,
    Items INTEGER[] NOT NULL ,
    PenniesSum INT NOT NULL ,
    Timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
