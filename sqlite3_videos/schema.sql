DROP TABLE IF EXISTS video;

CREATE TABLE video (
    uuid STR PRIMARY KEY,
    VideoName STR NOT NULL,
    LectureName STR NOT NULL,
    LecturerID INT,
    StudentID INT
);

-- created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

-- student ID
-- lecturer name
-- Lecture name



-- update schema of database
-- test the new functions
