-- Persons table
CREATE TABLE Persons (
    id VARCHAR(255) PRIMARY KEY,
    publicId VARCHAR(255),
    trackingId VARCHAR(255),
    profileId VARCHAR(255),
    occupation VARCHAR(255),
    firstName VARCHAR(100),
    lastName VARCHAR(100),
    picture VARCHAR(512)
);

CREATE INDEX idx_persons_publicid ON Persons(publicId);
CREATE INDEX idx_persons_profileid ON Persons(profileId);

-- Companies table
CREATE TABLE Companies (
    id VARCHAR(255) PRIMARY KEY,
    url VARCHAR(512),
    fullName VARCHAR(255),
    image VARCHAR(512),
    followers INT
);

CREATE INDEX idx_companies_fullname ON Companies(fullName);

-- Person2Company table
CREATE TABLE Person2Company (
    personId VARCHAR(255),
    companyId VARCHAR(255),
    PRIMARY KEY (personId, companyId),
    FOREIGN KEY (personId) REFERENCES Persons(id),
    FOREIGN KEY (companyId) REFERENCES Companies(id)
);

CREATE INDEX idx_person2company_companyid ON Person2Company(companyId);

-- Posts table
CREATE TABLE Posts (
    id VARCHAR(255) PRIMARY KEY,
    text TEXT,
    url VARCHAR(512),
    postedAtTimestamp BIGINT,
    postedAtISO TIMESTAMP
);

CREATE INDEX idx_posts_postedattimestamp ON Posts(postedAtTimestamp);

-- Author2Post table
CREATE TABLE Author2Post (
    authorId VARCHAR(255),
    postId VARCHAR(255),
    PRIMARY KEY (authorId, postId),
    FOREIGN KEY (postId) REFERENCES Posts(id)
);

CREATE INDEX idx_author2post_postid ON Author2Post(postId);

-- Attributes (Mentions) table
CREATE TABLE Attributes (
    id VARCHAR(255) PRIMARY KEY,
    postId VARCHAR(255),
    start INT,
    length INT,
    reference VARCHAR(255),
    FOREIGN KEY (postId) REFERENCES Posts(id)
);

CREATE INDEX idx_attributes_postid ON Attributes(postId);
CREATE INDEX idx_attributes_reference ON Attributes(reference);

