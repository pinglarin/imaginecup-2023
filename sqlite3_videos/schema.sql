DROP TABLE IF EXISTS video;

CREATE TABLE video (
    uuid STR PRIMARY KEY,
    VideoName STR NOT NULL,
    LectureName STR NOT NULL,
    LecturerID INT,
    StudentID INT
);

DROP TABLE IF EXISTS videoInfo;

CREATE TABLE videoInfo (
    uuid STR PRIMARY KEY,
    info STR NOT NULL,

    CONSTRAINT fk_uuid
        FOREIGN KEY (uuid)
        REFERENCES video (uuid)
);