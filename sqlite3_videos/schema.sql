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
<<<<<<< HEAD
    uuid TEXT
    sentences TEXT
    -- path to JSON
=======
    uuid TEXT PRIMARY KEY
    sentences TEXT
>>>>>>> 9e6889e8b646be5045103991a6f68b83f7d7bd45
    
    CONTEXTAINT fk_OCR_uuid
        FOREIGN KEY (uuid)
        REFERENCES OCR (uuid)
);


<<<<<<< HEAD
-- table speech recog << to be done

-- to be researched: keeping JSON results in DB
=======
-- table speech recog << to be done
>>>>>>> 9e6889e8b646be5045103991a6f68b83f7d7bd45
