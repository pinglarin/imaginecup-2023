from typing import Optional, Type
from typing_extensions import Self
import inspect
from database import SessionLocal, engine

from pydantic import BaseModel
from pydantic.fields import ModelField
from fastapi import FastAPI, Form

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#base class for creating and reading data (reduce code redundancy)
class VideoBase(BaseModel):
    # uuid: str
    # VideoName: str
    LectureName: str
    CourseName: str
    LecturerID: int
    Details: str
    class Config:
        orm_mode = True

    @classmethod
    def send_form(
        cls,
        LectureName: str = Form(...),
        CourseName: str = Form(...),
        LecturerID: int = Form(...),
        Details: str = Form(...),
    ) -> Self:
        return cls(LectureName=LectureName, CourseName=CourseName, LecturerID=LecturerID, Details=Details)

class VideoReturn(VideoBase):
    uuid: str
    VideoName: str

class VideoGroupBase(BaseModel):
    uuid: str
    GroupNumber: int
    class Config:
        orm_mode = True

    @classmethod # maybe change input format later
    def send_form(
        cls,
        uuid: str = Form(...),
        GroupNumber: int = Form(...),
    ) -> Self:
        return cls(uuid=uuid, GroupNumber=GroupNumber)

class StudentGroupBase(BaseModel):
    GroupNumber: int
    StudentID: int
    class Config:
        orm_mode = True

    @classmethod # maybe change input format later
    def send_form(
        cls,
        GroupNumber: int = Form(...),
        StudentID: int = Form(...),
    ) -> Self:
        return cls(GroupNumber=GroupNumber, StudentID=StudentID)


class StudentBase(BaseModel):
    StudentID: int
    Firstname: str
    Lastname: str
    class Config:
        orm_mode = True

    @classmethod
    def send_form(
        cls,
        StudentID: int = Form(...),
        Firstname: str = Form(...),
        Lastname: str = Form(...),
    ) -> Self:
        return cls(StudentID=StudentID, Firstname=Firstname, Lastname=Lastname)

class LecturerBase(BaseModel):
    LecturerID: int
    Firstname: str
    Lastname: str
    Details: str
    class Config:
        orm_mode = True

    @classmethod
    def send_form(
        cls,
        LecturerID: int = Form(...),
        Firstname: str = Form(...),
        Lastname: str = Form(...),
        Details: str = Form(...),
    ) -> Self:
        return cls(LecturerID=LecturerID, Firstname=Firstname, Lastname=Lastname, Details=Details)


    # @classmethod
    # def return_VideoName():
    #     return VideoReturn.VideoName

# class VideoUpdate(VideoReturn):
#     #vid = crud.get_video_by_ID(get_db(), uuid)
#     @classmethod
#     def as_form(
#         cls,
#         VideoName: Optional[str] = Form("VideoReturn.return_VideoName"), #VideoName: Optional[str] = Form(VideoReturn.return_VideoName),
#         LectureName: Optional[str] = Form("smth"),
#         LecturerID: Optional[int] = Form(1),
#         StudentID: Optional[int] = Form(1)
#     ) :
#         # new_parameters = []

#         # for field_name, model_field in cls.__fields__.items():
#         #     model_field: ModelField  # type: ignore

#         #     new_parameters.append(
#         #         inspect.Parameter(
#         #             model_field.alias,
#         #             inspect.Parameter.POSITIONAL_ONLY,
#         #             default=Form(...) if not model_field.required else Form(model_field.default),
#         #             annotation=model_field.outer_type_,
#         #         )
#         #     )

#         # async def as_form_func(**data):
#         #     return cls(**data)

#         # sig = inspect.signature(as_form_func)
#         # sig = sig.replace(parameters=new_parameters)
#         # as_form_func.__signature__ = sig  # type: ignore
#         # setattr(cls, 'as_form', as_form_func)
#         return cls(VideoName=VideoName, LectureName=LectureName, LecturerID=LecturerID, StudentID=StudentID)
    
    
    
    
    #  send_form(
    #     cls,
    #     VideoName: str = Form(...),
    #     LectureName: str = Form(...),
    #     LecturerID: int = Form(1),
    #     StudentID: int = Form(1)
    # ) -> Self:
    #     return cls(VideoName=VideoName, LectureName=LectureName, LecturerID=LecturerID, StudentID=StudentID)


#https://fastapi.tiangolo.com/tutorial/sql-databases/ << check out this
