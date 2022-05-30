from typing_extensions import Self
from sqlalchemy.dialects.postgresql import UUID

from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, FastAPI, File, UploadFile
from fastapi import FastAPI, File, Form, UploadFile


#base class for creating and reading data (reduce code redundancy)
class VideoBase(BaseModel):
    LectureName: str
    LecturerID: int
    StudentID: int
    class Config:
        orm_mode = True

    @classmethod
    def send_form(
        cls,
        LectureName: str = Form(...),
        LecturerID: int = Form(1),
        StudentID: int = Form(1)
    ) -> Self:
        return cls(LectureName=LectureName, LecturerID=LecturerID, StudentID=StudentID)


class VideoReturn(VideoBase):
    uuid: str
    VideoName: str

#https://fastapi.tiangolo.com/tutorial/sql-databases/ << check out this
