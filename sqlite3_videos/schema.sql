DROP TABLE IF EXISTS video;

CREATE TABLE video (
    uuid TEXT PRIMARY KEY,
    VideoName TEXT NOT NULL,
    VideoPath TEXT NOT NULL,
    LectureName TEXT NOT NULL,
    CourseName TEXT NOT NULL,
    LecturerID INT,
    StudentID INT,

    FOREIGN KEY (StudentID)
        REFERENCES student (StudentID),

    FOREIGN KEY (LecturerID)
        REFERENCES lecturer (LecturerID)
);

DROP TABLE IF EXISTS OCR;

CREATE TABLE OCR (
    uuid TEXT PRIMARY KEY,
    info TEXT NOT NULL,
    numFrames INT,

    FOREIGN KEY (uuid)
        REFERENCES video (uuid)
);

DROP TABLE IF EXISTS frame;

CREATE TABLE frame ( -- should there be metadata?
    frameID TEXT PRIMARY KEY,
    uuid TEXT NOT NULL,
    sentences TEXT,
    -- path to JSON
    
    FOREIGN KEY (uuid)
        REFERENCES OCR (uuid)
);

-- DROP TABLE IF EXISTS student_group;

-- CREATE TABLE student_group (
--     GroupNumber INT PRIMARY KEY,
--     StudentID INT NOT NULL,

--     FOREIGN KEY (GroupNumber)
--         REFERENCES video (GroupNumber),

--     FOREIGN KEY (StudentID)
--         REFERENCES student (StudentID)
-- );

DROP TABLE IF EXISTS student;

CREATE TABLE student (
    StudentID INT PRIMARY KEY,
    Firstname TEXT NOT NULL,
    Lastname TEXT NOT NULL
);

DROP TABLE IF EXISTS lecturer;

CREATE TABLE lecturer (
    LecturerID INT PRIMARY KEY,
    Firstname TEXT NOT NULL,
    Lastname TEXT NOT NULL    
);



-- table speech recog << to be done

-- to be researched: keeping JSON results in DB


















-- DROP TABLE IF EXISTS video;

-- CREATE TABLE video (
--     uuid TEXT PRIMARY KEY,
--     VideoName TEXT NOT NULL,
--     VideoPath TEXT NOT NULL,
--     LectureName TEXT NOT NULL,
--     CourseName TEXT NOT NULL,
--     LecturerID INT,
--     StudentID INT
-- );

-- DROP TABLE IF EXISTS OCR;

-- CREATE TABLE OCR (
--     uuid TEXT PRIMARY KEY,
--     info TEXT NOT NULL,
--     numFrames INT,

--     FOREIGN KEY (uuid)
--         REFERENCES video (uuid)
-- );

-- DROP TABLE IF EXISTS frame;

-- CREATE TABLE frame ( -- should there be metadata?
--     frameID TEXT PRIMARY KEY,
--     uuid TEXT NOT NULL,
--     sentences TEXT,
--     -- path to JSON
    
--     FOREIGN KEY (uuid)
--         REFERENCES OCR (uuid)
-- );

-- DROP TABLE IF EXISTS student;

-- CREATE TABLE student (
--     StudentID INT PRIMARY KEY,
--     Firstname TEXT NOT NULL,
--     Lastname TEXT NOT NULL,
    
--     FOREIGN KEY (StudentID)
--         REFERENCES video (StudentID)
-- );

-- DROP TABLE IF EXISTS lecturer;

-- CREATE TABLE lecturer (
--     LecturerID INT PRIMARY KEY,
--     Firstname TEXT NOT NULL,
--     Lastname TEXT NOT NULL,
    
--     FOREIGN KEY (LecturerID)
--         REFERENCES video (LecturerID)
-- );
-- -- table speech recog << to be done

-- -- to be researched: keeping JSON results in DB
