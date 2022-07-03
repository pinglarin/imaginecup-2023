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
    LecturerID = Column(Integer, ForeignKey("lecturer.LecturerID"), nullable=False)
    Details = Column(String, nullable=False)

    video_lecturer = relationship("Lecturer", foreign_keys=[LecturerID])

class VideoGroup(Base):
    __tablename__ = "video_group"
    uuid = Column(String, ForeignKey("video.uuid"), nullable=False ,primary_key=True)
    GroupNumber = Column(Integer, ForeignKey("student_group.GroupNumber"), nullable=False, primary_key=True)

    video_group_uuid = relationship("Video", foreign_keys=[uuid])
    video_group = relationship("StudentGroup", foreign_keys=[GroupNumber])

class StudentGroup(Base):
    __tablename__ = "student_group"

    GroupNumber = Column(Integer, nullable=False, primary_key=True)
    StudentID = Column(Integer, ForeignKey("student.StudentID"), nullable=False, primary_key=True)

    student = relationship("Student", foreign_keys=[StudentID])

class Student(Base):
    __tablename__ = "student"

    StudentID = Column(Integer, primary_key=True)
    Firstname = Column(String, nullable=False)
    Lastname = Column(String, nullable=False)

class Lecturer(Base):
    __tablename__ = "lecturer"

    LecturerID = Column(Integer, primary_key=True)
    Firstname = Column(String, nullable=False)
    Lastname = Column(String, nullable=False)
    Details = Column(String, nullable=False)

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
