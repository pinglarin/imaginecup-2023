from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base
import uuid


class Video(Base):
    __tablename__ = "video"

    uuid = Column(String, name="uuid", primary_key=True, default=str(uuid.uuid4()))
    VideoName = Column(String, nullable=False) #file.filename
    VideoPath = Column(String, nullable=False)
    LectureName = Column(String, nullable=False)
    CourseName = Column(String, nullable=False)
    LecturerID = Column(Integer, ForeignKey("Lecturer.lecturer"))
    StudentID = Column(Integer, ForeignKey("Student.stu"))

    vid_lecturer = relationship("Lecturer", back_populates="lecturer")
    vid_stu = relationship("Student", back_populates="stu")
   
    
class Student(Base):
    __tablename__ = "student"

    StudentID = Column(Integer, primary_key=True)
    Firstname = Column(String, nullable=False)
    Lastname = Column(String, nullable=False)

    stu = relationship("Video", back_populates="vid_stu")

class Lecturer(Base):
    __tablename__ = "lecturer"

    LecturerID = Column(Integer, primary_key=True)
    Firstname = Column(String, nullable=False)
    Lastname = Column(String, nullable=False)

    lecturer = relationship("Video", back_populates="vid_lecturer")

    #from https://www.codegrepper.com/code-examples/sql/uuid+sqlalcomany

    #uuid = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    #created = Column(DateTime, nullable=False, default=True)
#-------------------------------------------------------------------------------------------------------------------------------------------

#OLD CODE
# from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
# from sqlalchemy.orm import relationship

# from database import Base


# class Video(Base):
#     __tablename__ = "video"

#     id = Column(Integer, primary_key=True)
#     created = Column(DateTime, nullable=False, default=True)
#     video_name = Column(String, nullable=False)
#     file_path_name = Column(String, nullable=False)
#     file_blob = Column(String, nullable=False)




# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)
#     is_active = Column(Boolean, default=True)

#     items = relationship("Item", back_populates="owner")

# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")
