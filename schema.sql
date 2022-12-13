
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS RatingUser;
DROP TABLE IF EXISTS BidsHistory;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS CreditCard;
DROP TABLE IF EXISTS ItemFilePicture;
DROP TABLE IF EXISTS Report;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS Warning;
DROP TABLE IF EXISTS Complaint;





-- CREATE TABLE AllUser (
--     ID INTEGER PRIMARY KEY,
--     email TEXT UNIQUE NOT NULL,
--     firstName TEXT NOT NULL,
--     lastName TEXT NOT NULL,
--     password TEXT NOT NULL,
--     address TEXT,
--     phoneNumber INTEGER,
--     userType INTEGER DEFAULT 0
-- );

-- CREATE TABLE SuperUser (
--     ID INTEGER PRIMARY KEY,
--     FOREIGN KEY (ID) REFERENCES AllUser (ID)
-- );

-- CREATE TABLE OrdinaryUser (
--     ID INTEGER PRIMARY KEY,
--     superUserID INTEGER UNIQUE,
--     banHammer BOOLEAN DEFAULT 0,
--     balance REAL NOT NULL,
--     rating REAL,
--     FOREIGN KEY (ID) REFERENCES AllUser (ID),
--     FOREIGN KEY (superUserID) REFERENCES SuperUser (ID)
-- );

-- CREATE TABLE GuestUser (
--     ID INTEGER PRIMARY KEY,
--     superUserID INTEGER UNIQUE,
--     ApplicationStatus INTEGER
-- );

CREATE TABLE RatingUser (
    ReferenceID INTEGER PRIMARY KEY,
    EvaluatorID INTEGER UNIQUE,
    EvalueeID INTEGER UNIQUE,
    Description TEXT NOT NULL,
    Rating REAL NOT NULL,
    FOREIGN KEY (EvaluatorID) REFERENCES OrdinaryUser (ID),
    FOREIGN KEY (EvalueeID) REFERENCES OrdinaryUser (ID)
);

CREATE TABLE Item (
    ItemID INTEGER PRIMARY KEY,
    OwnerID INTEGER,
    Title TEXT NOT NULL,
    Status INTEGER,
    StartTime DATETIME,
    EndTime DATETIME,
    StartPrice REAL NOT NULL,
    FileName TEXT,
    WinningBid REAL,
    SUID INTEGER UNIQUE,
    FOREIGN KEY (OwnerID) REFERENCES OrdinaryUser (ID),
    FOREIGN KEY (SUID) REFERENCES SuperUser (ID)
);

CREATE TABLE BidsHistory (
    ItemID INTEGER PRIMARY KEY,
    OwnerID INTEGER UNIQUE,
    Title TEXT NOT NULL,
    EndTime DATETIME,
    BidderID INTEGER UNIQUE,
    FOREIGN KEY (BidderID) REFERENCES OrdinaryUser (ID),
    FOREIGN KEY (ItemID) REFERENCES Item (ID)
);

CREATE TABLE Transactions (
    TransactionID INTEGER PRIMARY KEY,
    ItemID INTEGER UNIQUE,
    BuyerID INTEGER UNIQUE,
    SellerID INTEGER UNIQUE,
    Title TEXT NOT NULL,
    Amount REAL,
    Balance REAl,
    FOREIGN KEY (BuyerID) REFERENCES OrdinaryUser (ID),
    FOREIGN KEY (SellerID) REFERENCES OrdinaryUser (ID),
    FOREIGN KEY (ItemID) REFERENCES Item (ID)
);

CREATE TABLE Tags (
    TagID INTEGER PRIMARY KEY,
    ItemID INTEGER UNIQUE,
    FOREIGN KEY (ItemID) REFERENCES Item (ID)
);

CREATE TABLE ItemFilePicture (
    FileID INTEGER PRIMARY KEY,
    UploadName TEXT,
    FileName TEXT,
    ItemID INTEGER UNIQUE,
    FOREIGN KEY (ItemID) REFERENCES Item (ID)
);

CREATE TABLE CreditCard (
    UserID INTEGER PRIMARY KEY,
    ItemID INTEGER UNIQUE,
    Name TEXT,
    FOREIGN KEY (UserID) REFERENCES OrdinaryUser (ID)
);  


CREATE TABLE Warning (
    ReferenceID INTEGER PRIMARY KEY,
    SUID INTEGER UNIQUE,
    ItemID INTEGER UNIQUE,
    REASON TEXT NOT NULL,
    FOREIGN KEY (SUID) REFERENCES SuperUser (ID),
    FOREIGN KEY (ItemID) REFERENCES Item (ID)
);

CREATE TABLE Report (
    ReferenceID INTEGER PRIMARY KEY,
    SUID INTEGER UNIQUE,
    UserID INTEGER UNIQUE,
    ItemID INTEGER,
    REASON TEXT NOT NULL,
    Status INTEGER,
    FOREIGN KEY (SUID) REFERENCES SuperUser (ID),
    FOREIGN KEY (UserID) REFERENCES OrdinaryUser (ID)
);

CREATE TABLE Complaint (
    ReferenceID INTEGER PRIMARY KEY,
    ComplainerID INTEGER UNIQUE,
    ItemID INTEGER,
    REASON TEXT NOT NULL,
    Status INTEGER,
    FOREIGN KEY (ComplainerID) REFERENCES OrdinaryUser (ID)
);

