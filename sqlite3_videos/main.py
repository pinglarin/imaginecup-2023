from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from schemas import VideoBase, StudentBase, LecturerBase, VideoGroupBase,StudentGroupBase
import uvicorn
import uuid
from databases import Database
from fastapi.responses import FileResponse, StreamingResponse
from pathlib import Path
from fastapi import FastAPI
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from fastapi import Header
from fastapi.templating import Jinja2Templates
import os

from speech_ocr import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
    
app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

database = Database("sqlite:///videoDatabase.db")

@app.on_event("startup")
async def database_connect():
    await database.connect()


@app.on_event("shutdown")
async def database_disconnect():
    await database.disconnect()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/getvideo/{id}")
def read_video(uuid: str, db: Session = Depends(get_db)):
    db_vdo = crud.get_video_by_ID(db, uuid=uuid)
    if db_vdo is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_vdo

@app.get("/getallvideos")
def read_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    print("in getallvideos")
    videos = crud.get_all_videos(db, skip=skip, limit=limit)
    return videos

@app.post("/uploadvideo")
async def upload_video(file: UploadFile, video: schemas.VideoBase = Depends(VideoBase.send_form), db: Session = Depends(get_db)):
    vuuid = str(uuid.uuid4())
    print("uuid: ", vuuid)
    db_vdo = crud.get_video_by_ID(db, uuid=vuuid)
    if db_vdo:
        raise HTTPException(status_code=400, detail="Video already exists in database!")
    print("about to input into database >> filename:", file.filename)
    with open(f'uploadedVideos/{vuuid}.mp4', 'wb') as uploadvideo:
        content = await file.read()
        uploadvideo.write(content)
        # VideoPath = f'C:/Users/Aekky/OneDrive - Mahidol University/Desktop/VS Code work/imaginecup-2023/React_part/src/components/PlayerVideo_page/Player_part/uploadedVideos/{vuuid}.mp4'
        VideoPath = f'uploadedVideos/{vuuid}.mp4'
    crud.create_video(db=db, video=video, file=file, uuid=vuuid, path = VideoPath)
    # not working (ignored) ???
    json_ocr_output = vidOCR(VideoPath)
    print(json_ocr_output)
    return "Success"
# To be done: if function returns success, the user is notified of it, and the opposite goes for failed attempt.

@app.post("/uploadvideo/youtube")
async def upload_video(VideoName: str, VideoPath: str, video: schemas.VideoBase = Depends(VideoBase.send_form), db: Session = Depends(get_db)):
    vuuid = str(uuid.uuid4())
    print("uuid: ", vuuid)
    db_vdo = crud.get_video_by_ID(db, uuid=vuuid)
    if db_vdo:
        raise HTTPException(status_code=400, detail="Video already exists in database!")
    crud.create_youtube_video(db=db, video=video, uuid=vuuid, path = VideoPath, VideoName=VideoName)
    # # not working (ignored) ??? --> commented temporarily
    # json_ocr_output = vidOCR(VideoPath)
    # print(json_ocr_output)
    return "Success"

@app.put("/updatevideo/{uuid}")
async def update_item(vuuid: str, video: schemas.VideoBase = Depends(VideoBase.send_form), db: Session = Depends(get_db)):
    db_vdo = db.get(models.Video, vuuid)
    if not db_vdo:
        raise HTTPException(status_code=404, detail="Video not found")
    vdo_data = video.dict()
    for key, value in vdo_data.items():
        setattr(db_vdo, key, value)
    db.add(db_vdo)
    db.commit()
    db.refresh(db_vdo)
    return db_vdo

@app.delete("/deletevideo/{id}")
async def delete_video(uuid: str, db: Session = Depends(get_db)):
    db_vdo = crud.get_video_by_ID(db, uuid=uuid)
    if db_vdo is None:
        raise HTTPException(status_code=404, detail="Video not found")
    db.delete(db_vdo)
    db.commit()
    print("Video is successfully deleted")
    return "success"

@app.get("/vid") # video streaming function
async def video_endpoint(uuid: str, range: str = Header(None)):
    CHUNK_SIZE = 1024*1024
    vuuid = f'"{uuid}"'
    print(vuuid)
    query = "SELECT VideoPath FROM video WHERE uuid={}".format(str(vuuid))
    video_path = str(await database.fetch_one(query=query))
    video_path = Path(video_path[2:-3])
    print(video_path)
    if os.path.exists(video_path):
        print("found")
    filesize = str(video_path.stat().st_size)
    start, end = range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    chunksize = (end-start) + 1
    with open(video_path, "rb") as video:
        video.seek(start)
        data = video.read(end - start)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
            'Accept-Ranges': 'bytes',
        }
    return Response(data, status_code=206, headers=headers, media_type="video/mp4")

@app.get("/youtube")
async def video_endpoint(uuid: str):
    vuuid = f'"{uuid}"'
    print(vuuid)
    query = "SELECT VideoPath FROM video WHERE uuid={}".format(str(vuuid))
    video_path = str(await database.fetch_one(query=query))
    video_path = video_path[2:-3]
    print(video_path)
    return video_path

# --- POST FUNCTIONS ---
@app.post("/signup_student")
async def signupStudent(student: schemas.StudentBase = Depends(StudentBase.send_form), db: Session = Depends(get_db)):
    # db_vdo = crud.get_video_by_ID(db, uuid=vuuid)
    # if db_vdo:
    #     raise HTTPException(status_code=400, detail="Video already exists in database!")
    crud.create_student(db=db, student=student)
    return "Success"

@app.post("/signup_lecturer")
async def signupLecturer(lecturer: schemas.LecturerBase = Depends(LecturerBase.send_form), db: Session = Depends(get_db)):
    # db_vdo = crud.get_video_by_ID(db, uuid=vuuid)
    # if db_vdo:
    #     raise HTTPException(status_code=400, detail="Video already exists in database!")
    crud.create_lecturer(db=db, lecturer=lecturer)
    return "Success"

@app.post("/group_students")
async def groupStudents(group: schemas.StudentGroupBase = Depends(StudentGroupBase.send_form), db: Session = Depends(get_db)):
    # db_vdo = crud.get_video_by_ID(db, uuid=vuuid)
    # if db_vdo:
    #     raise HTTPException(status_code=400, detail="Video already exists in database!")
    crud.assign_groups(db=db, group=group)
    return "Success"

@app.post("/video_group")
async def video_group(group: schemas.VideoGroupBase = Depends(VideoGroupBase.send_form), db: Session = Depends(get_db)):
    # db_vdo = crud.get_video_by_ID(db, uuid=vuuid)
    # if db_vdo:
    #     raise HTTPException(status_code=400, detail="Video already exists in database!")
    crud.video_group_assignment(db=db, group=group)
    return "Success"

# --- GET FUNCTIONS ---
@app.get("/get/lecturename")
async def get_lecturename(vuuid: str):
    query = "SELECT LectureName FROM video WHERE uuid = :vuuid"
    rows = await database.fetch_one(query=query, values={"vuuid": vuuid})
    return rows

@app.get("/get/coursename")
async def get_coursename(vuuid: str):
    query = "SELECT CourseName FROM video WHERE uuid = :vuuid"
    rows = await database.fetch_one(query=query, values={"vuuid": vuuid})
    return rows

@app.get("/get/lecturedetails")
async def get_lecturedetails(vuuid: str):
    query = "SELECT Details FROM video WHERE uuid = :vuuid"
    rows = await database.fetch_one(query=query, values={"vuuid": vuuid})
    return rows

@app.get("/get/lectures_of_lecturer")
async def get_lectures_of_lecturer(firstname: str):
    query = "SELECT * FROM video LEFT JOIN lecturer ON (video.LecturerID = lecturer.LecturerID) WHERE lecturer.Firstname = :Firstname"
    rows = await database.fetch_all(query=query, values={"Firstname": firstname})
    return rows

@app.get("/get/students_in_group")
async def students_in_group(GroupNumber: int):
    query = "SELECT * FROM student INNER JOIN student_group ON (student.StudentID = student_group.StudentID) WHERE student_group.GroupNumber = :GroupNumber"
    rows = await database.fetch_all(query=query, values={"GroupNumber": GroupNumber})
    return rows

# @app.get("/get/coursename")
# async def get_from_coursename(coursename: str):
#     query = "SELECT * FROM video WHERE CourseName = :CourseName"
#     rows = await database.fetch_all(query=query, values={"CourseName": coursename})
#     return rows

# @app.get("/get/lecturename")
# async def get_from_lecturename(lecturename: str):
#     query = "SELECT * FROM video WHERE LectureName = :LectureName"
#     rows = await database.fetch_all(query=query, values={"LectureName": lecturename})
#     return rows