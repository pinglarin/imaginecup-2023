from sqlalchemy.orm import Session

import models, schemas
from fastapi import FastAPI, File, UploadFile


def get_video_by_ID(db: Session, uuid: str):
    print("in get_video_by_ID")
    print("uuid in get_video: ", uuid)
    return db.query(models.Video).filter(models.Video.uuid == uuid).first()

# def get_videos_by_VideoName(db: Session, VideoName: str):
#     return db.query(models.Video).filter(models.Video.VideoName == VideoName).all()

# def get_videos_by_LectureName(db: Session, LectureName: str):
#     print("in function")
#     return db.query(models.Video).filter(models.Video.LectureName == LectureName).all()

# def get_videos_by_LecturerID(db: Session, LecturerID: int):
#     return db.query(models.Video).filter(models.Video.LecturerID == LecturerID).all()

# def get_videos_by_StudentID(db: Session, StudentID: int):
#     return db.query(models.Video).filter(models.Video.StudentID == StudentID).all()

def get_all_videos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Video).offset(skip).limit(limit).all()

def create_video(db: Session, video: schemas.VideoBase, file: UploadFile, uuid: str, path:str):
    print("in create_video")
    vdo = models.Video(uuid=uuid, VideoName=file.filename, VideoPath = path, LectureName=video.LectureName, CourseName = video.CourseName, LecturerID=video.LecturerID, Details=video.Details)
    db.add(vdo)
    db.commit()
    db.refresh(vdo)
    print("file is inside database ", file.filename)
    print("Video is successfully uploaded")
    return vdo

def create_youtube_video(db: Session, video: schemas.VideoBase, uuid: str, path: str, VideoName: str):
    print("in create_youtube_video")
    vdo = models.Video(uuid=uuid, VideoName=VideoName, VideoPath = path, LectureName=video.LectureName, CourseName = video.CourseName, LecturerID=video.LecturerID, Details=video.Details)
    db.add(vdo)
    db.commit()
    db.refresh(vdo)
    print("Video is successfully uploaded")
    return vdo

def create_student(db: Session, student: schemas.StudentBase):
    print("in create_student")
    stu = models.Student(StudentID=student.StudentID, Firstname=student.Firstname, Lastname=student.Lastname)
    db.add(stu)
    db.commit()
    db.refresh(stu)
    print("student is successfully created")
    return stu

def create_lecturer(db: Session, lecturer: schemas.LecturerBase):
    print("in create_lecturer")
    lec = models.Lecturer(LecturerID=lecturer.LecturerID, Firstname=lecturer.Firstname, Lastname=lecturer.Lastname, Details=lecturer.Details)
    db.add(lec)
    db.commit()
    db.refresh(lec)
    print("lecturer is successfully created")
    return lec

def assign_groups(db: Session, group: schemas.StudentGroupBase):
    gr = models.StudentGroup(GroupNumber=group.GroupNumber, StudentID = group.StudentID)
    db.add(gr)
    db.commit()
    db.refresh(gr)
    print("student is successfully assigned to group")
    return gr


def video_group_assignment(db: Session, group: schemas.VideoGroupBase):
    gr = models.VideoGroup(uuid=group.uuid, GroupNumber=group.GroupNumber)
    db.add(gr)
    db.commit()
    db.refresh(gr)
    print("video has been added groups")
    return gr
# def get_videos(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Video).offset(skip).limit(limit).all()


# def create_video(db: Session, video: schemas.VideoCreate):
#     #vdo = models.Video(video_name=video.video_name, file_path_name=(video.file_path_name).replace('\\', '\\\\')) #file_blob = video.file_blob
#     #vdo = models.Video(video_name=video.video_name, file_path_name=json.loads(video.file_path_name)) #file_blob = video.file_blob
#     #vdo = models.Video(video_name=Datavideo.acceptedFileItems[0].key, file_path_name=Datavideo.acceptedFileItems[0]._source.fileName) #file_blob = video.file_blob

#     vdo = models.Video(video_name=video.video_name, file_path_name=video.file_path_name)
#     db.add(vdo)
#     db.commit()
#     db.refresh(vdo)
#     return vdo
