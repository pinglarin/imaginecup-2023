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

# @app.get("/getvideos_videoname/{videoname}")
# def read_videos_videoname(VideoName: str, db: Session = Depends(get_db)):
#     print("in getvideos/{videoname}")
#     videos = crud.get_videos_by_VideoName(db, VideoName=VideoName)
#     if videos is None:
#         raise HTTPException(status_code=404, detail="Video not found")
#     return videos

# @app.get("/getvideos_lecturename/{lecturename}")
# def read_videos_lecturename(LectureName : str, db: Session = Depends(get_db)):
#     print("in getvideos/{lecturename}")
#     videos = crud.get_videos_by_LectureName(db, LectureName=LectureName)
#     if videos is None:
#         raise HTTPException(status_code=404, detail="Video not found")
#     return videos

# @app.get("/getvideos_lecturerID/{lecturerID}")
# def read_videos_lecturerID(LecturerID: int, db: Session = Depends(get_db)):
#     print("in getvideos/{lecturerID}")
#     videos = crud.get_videos_by_LecturerID(db, LecturerID=LecturerID)
#     if videos is None:
#         raise HTTPException(status_code=404, detail="Video not found")
#     return videos

# @app.get("/getvideos_studentID/{studentID}")
# def read_videos_studentID(StudentID: int, db: Session = Depends(get_db)):
#     print("in getvideos/{studentID}")
#     videos = crud.get_videos_by_StudentID(db, StudentID=StudentID)
#     if videos is None:
#         raise HTTPException(status_code=404, detail="Video not found")
#     return videos

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

@app.get("/vid")
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
    if(range):
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
    else:
        with open(video_path, "rb") as video:
            video.seek(0)
            data = video.read(CHUNK_SIZE)
            headers = {
                'Content-Length': str(CHUNK_SIZE),
            }
    return Response(data, status_code=206, headers=headers, media_type="video/mp4")

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

@app.get("/get/coursename")
async def get_from_coursename(coursename: str):
    query = "SELECT * FROM video WHERE CourseName = :CourseName"
    rows = await database.fetch_all(query=query, values={"CourseName": coursename})
    return rows

@app.get("/get/lecturename")
async def get_from_lecturename(lecturename: str):
    query = "SELECT * FROM video WHERE LectureName = :LectureName"
    rows = await database.fetch_all(query=query, values={"LectureName": lecturename})
    return rows

@app.get("/get/lectures_of_lecturer")
async def get_lectures_of_lecturer(firstname: str):
    query = "SELECT * FROM video LEFT JOIN lecturer ON (video.LecturerID = lecturer.LecturerID) WHERE lecturer.Firstname = :Firstname"
    rows = await database.fetch_all(query=query, values={"Firstname": firstname})
    return rows

# @app.get("/teststream") # http://127.0.0.1:8000/teststream
# async def test_stream():
#     return FileResponse('uploadedVideos/1ce89b45-1ab6-478c-b85f-91233176514e.mp4', media_type="video/mp4")

# @app.get("/stream")
# async def stream_video(uuid: str):
#     vuuid = f'"{uuid}"'
#     print(vuuid)
#     query = "SELECT VideoPath FROM video WHERE uuid={}".format(str(vuuid))
#     path = str(await database.fetch_one(query=query))
#     path = path[2:-3]
#     print(path)
#     return FileResponse(path, media_type="video/mp4")


# @app.get("/stream2")
# async def main(uuid: str):
#     vuuid = f'"{uuid}"'
#     print(vuuid)
#     query = "SELECT VideoPath FROM video WHERE uuid={}".format(str(vuuid))
#     path = str(await database.fetch_one(query=query))
#     path = path[2:-3]
#     print(path)
#     def iterfile():  # 
#         with open(path, mode="rb") as file_like:  # 
#             yield from file_like  # 

#     return StreamingResponse(iterfile(), media_type="video/mp4")


# @app.post("/test")
# async def fetch_data(id: int):
#     query = "SELECT LectureName FROM video WHERE ID={}".format(str(id))
#     results = await database.fetch_all(query=query)
#     return  results

# from pathlib import Path
# from fastapi import FastAPI
# from fastapi import Request, Response
# from fastapi import Header
# from fastapi.templating import Jinja2Templates

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")
# CHUNK_SIZE = 1024*1024
# video_path = Path("uploadedVideos/74f7e89d-0caf-4b0d-b32d-591d4c3bcf74.mp4")

# @app.get("/video")
# async def video_endpoint():
#     # print(range)
#     # print(type(range))
#     # start, end = str(range).replace("bytes=", "").split("-")
#     # start = int(start)
#     # print(start)
#     # end = int(end) if end else start + CHUNK_SIZE
#     # print(end)
#     start = 1024000
#     end = 2048000
#     with open(video_path, "rb") as video:
#         video.seek(start)
#         data = video.read(end - start)
#         filesize = str(video_path.stat().st_size)
#         headers = {
#             'Content-Range': f'bytes {str(start)}-{str(end)}/{filesize}',
#             'Accept-Ranges': 'bytes'
#         }
#         return Response(data, status_code=206, headers=headers, media_type="video/mp4")

# @app.get("/get/viewed_videos")
# async def get_viewed_videos(firstname: str):
#     query = "SELECT * FROM video LEFT JOIN student ON (video.StudentID = student.StudentID) WHERE student.Firstname = :Firstname"
#     rows = await database.fetch_all(query=query, values={"Firstname": firstname})
#     return rows

@app.post("/group_students")
async def groupStudents(group: schemas.StudentGroupBase = Depends(StudentGroupBase.send_form), db: Session = Depends(get_db)):
    # db_vdo = crud.get_video_by_ID(db, uuid=vuuid)
    # if db_vdo:
    #     raise HTTPException(status_code=400, detail="Video already exists in database!")
    crud.assign_groups(db=db, group=group)
    return "Success"

@app.get("/get/students_in_group")
async def students_in_group(GroupNumber: int):
    query = "SELECT * FROM student INNER JOIN student_group ON (student.StudentID = student_group.StudentID) WHERE student_group.GroupNumber = :GroupNumber"
    rows = await database.fetch_all(query=query, values={"GroupNumber": GroupNumber})
    return rows

@app.post("/video_group")
async def video_group(group: schemas.VideoGroupBase = Depends(VideoGroupBase.send_form), db: Session = Depends(get_db)):
    # db_vdo = crud.get_video_by_ID(db, uuid=vuuid)
    # if db_vdo:
    #     raise HTTPException(status_code=400, detail="Video already exists in database!")
    crud.video_group_assignment(db=db, group=group)
    return "Success"


# @app.get("/get/video_permission/students")
# async def students_in_group(GroupNumber: int):
#     query = "SELECT * FROM student INNER JOIN student_group ON (student.StudentID = student_group.StudentID) WHERE student_group.GroupNumber = :GroupNumber"
#     rows = await database.fetch_all(query=query, values={"GroupNumber": GroupNumber})
#     return rows   
#------------------------------------------------------------------------------------------------------------------------------------------
#OLD UNUSED CODE
# @app.post("/video/post", response_model=schemas.Video)
# def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
#     print("in create_video")
#     print("uuid: ", video.uuid)
#     db_vdo = crud.get_video(db, uuid=video.uuid)
#     if db_vdo:
#         raise HTTPException(status_code=400, detail="Video already exists in database!")
#     print("crud.create_video")
#     return crud.create_video(db=db, video=video)


#original function
# @app.post("/uploadfile")
# async def create_upload_file(file: UploadFile):
#     print(file.filename)
#     return {"filename": file.filename}


# @app.post("/uploadfile2")
# async def create_upload_file(file: UploadFile, video: schemas.VideoBase, db: Session = Depends(get_db)): #schemas.VideoCreate
#     print("in create_upload_file")
#     print("uuid: ", video.uuid)
#     #uncomment when doing the get_video function
#     # db_vdo = crud.get_video(db, uuid=video.uuid)
#     # if db_vdo:
#     #     raise HTTPException(status_code=400, detail="Video already exists in database!")
#     print("crud.create_video")
#     print("filename:", file.filename)
#     return crud.create_video(db=db, video=video, file=file)
#     #return {"filename": file.filename}


# @app.post("/files/")
# async def create_file( file: UploadFile, video: schemas.VideoBase = Depends(VideoBase.send_form)):
#     return {
#         "file_name": file.filename,
#         "video": video
#     }

