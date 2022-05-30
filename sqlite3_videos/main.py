from fastapi import Depends, FastAPI, HTTPException, FastAPI, File, UploadFile
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, Form, UploadFile
from schemas import VideoBase
import uvicorn


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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/getvideo/{id}", response_model=schemas.VideoReturn)
def read_video(uuid: str, db: Session = Depends(get_db)):
    db_vdo = crud.get_video_by_ID(db, uuid=uuid)
    if db_vdo is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return db_vdo

@app.get("/getvideos/{videoname}", response_model=list[schemas.VideoReturn])
def read_videos(VideoName: str, db: Session = Depends(get_db)):
    print("in getvideos/{videoname}")
    videos = crud.get_videos_by_VideoName(db, VideoName=VideoName)
    if videos is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return videos

@app.get("/getvideos/{lecturename}", response_model=list[schemas.VideoReturn])
def read_videos(LectureName : str, db: Session = Depends(get_db)):
    print("in getvideos/{lecturename}")
    videos = crud.get_videos_by_LectureName(db, LectureName=LectureName)
    if videos is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return videos

@app.get("/getvideos/{lecturerID}", response_model=list[schemas.VideoReturn])
def read_videos(LecturerID: int, db: Session = Depends(get_db)):
    print("in getvideos/{lecturerID}")
    videos = crud.get_videos_by_LecturerID(db, LecturerID=LecturerID)
    if videos is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return videos

@app.get("/getvideos/{studentID}", response_model=list[schemas.VideoReturn])
def read_videos(StudentID: int, db: Session = Depends(get_db)):
    print("in getvideos/{studentID}")
    videos = crud.get_videos_by_StudentID(db, StudentID=StudentID)
    if videos is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return videos

 
@app.get("/getallvideos", response_model=list[schemas.VideoReturn])
def read_videos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    print("in getallvideos")
    videos = crud.get_all_videos(db, skip=skip, limit=limit)
    return videos
    
       
@app.post("/uploadvideo")
async def create_file(file: UploadFile, video: schemas.VideoBase = Depends(VideoBase.send_form), db: Session = Depends(get_db)):
    print("in files2, create_file")
    print("uuid: ", video.uuid)
    db_vdo = crud.get_video(db, uuid=video.uuid)
    if db_vdo:
        raise HTTPException(status_code=400, detail="Video already exists in database!")
    print("about to input into database >> filename:", file.filename)
    return crud.create_video(db=db, video=video, file=file)


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

