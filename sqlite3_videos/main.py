from fastapi import Depends, FastAPI, HTTPException, FastAPI, File, UploadFile
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from schemas import VideoBase, VideoUpdate
import uvicorn
import uuid
from databases import Database
from fastapi import FastAPI
from fastapi.responses import FileResponse

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

@app.get("/getvideos_videoname/{videoname}")
def read_videos_videoname(VideoName: str, db: Session = Depends(get_db)):
    print("in getvideos/{videoname}")
    videos = crud.get_videos_by_VideoName(db, VideoName=VideoName)
    if videos is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return videos

@app.get("/getvideos_lecturename/{lecturename}")
def read_videos_lecturename(LectureName : str, db: Session = Depends(get_db)):
    print("in getvideos/{lecturename}")
    videos = crud.get_videos_by_LectureName(db, LectureName=LectureName)
    if videos is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return videos

@app.get("/getvideos_lecturerID/{lecturerID}")
def read_videos_lecturerID(LecturerID: int, db: Session = Depends(get_db)):
    print("in getvideos/{lecturerID}")
    videos = crud.get_videos_by_LecturerID(db, LecturerID=LecturerID)
    if videos is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return videos

@app.get("/getvideos_studentID/{studentID}")
def read_videos_studentID(StudentID: int, db: Session = Depends(get_db)):
    print("in getvideos/{studentID}")
    videos = crud.get_videos_by_StudentID(db, StudentID=StudentID)
    if videos is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return videos

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
    with open(f'../React_part/src/components/PlayerVideo_page/Player_part/uploadedVideos/{vuuid}.mp4', 'wb') as uploadvideo:
        content = await file.read()
        uploadvideo.write(content)
        # VideoPath = f'C:/Users/Aekky/OneDrive - Mahidol University/Desktop/VS Code work/imaginecup-2023/React_part/src/components/PlayerVideo_page/Player_part/uploadedVideos/{vuuid}.mp4'
        VideoPath = f'React_part/src/components/PlayerVideo_page/Player_part/uploadedVideos/{vuuid}.mp4' # is this type of path correct??
    crud.create_video(db=db, video=video, file=file, uuid=vuuid, path = VideoPath)
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


@app.get("/stream")
async def stream_video(uuid: str):
    vuuid = f'"{uuid}"'
    print(vuuid)
    query = "SELECT VideoPath FROM video WHERE uuid={}".format(str(vuuid))
    results = database.fetch_one(query=query)
    print(results)
    path = str( await results)
    path = path[:-3]
    path = path[2:]
    print(path)
    return FileResponse(path, media_type="video/mp4")

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

