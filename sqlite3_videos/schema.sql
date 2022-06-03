DROP TABLE IF EXISTS video;

CREATE TABLE video (
    uuid TEXT PRIMARY KEY,
    VideoName TEXT NOT NULL,
    LectureName TEXT NOT NULL,
    LecturerID INT,
    StudentID INT
);

DROP TABLE IF EXISTS videoInfo; --delete later

DROP TABLE IF EXISTS OCR;

CREATE TABLE OCR (
    uuid TEXT PRIMARY KEY,
    info TEXT NOT NULL,
    numFrames INT

    CONTEXTAINT fk_video_uuid
        FOREIGN KEY (uuid)
        REFERENCES video (uuid)
);

DROP TABLE IF EXISTS frame;

CREATE TABLE frame ( -- should there be metadata?
    frameID TEXT PRIMARY KEY,
    uuid TEXT PRIMARY KEY
    sentences TEXT
    
    CONTEXTAINT fk_OCR_uuid
        FOREIGN KEY (uuid)
        REFERENCES OCR (uuid)
);


-- table speech recog << to be done