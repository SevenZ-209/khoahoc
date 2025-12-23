import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, Enum, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin
from eapp import db, app

class UserRole(enum.Enum):
    ADMIN = 1
    Hoc_Vien=2
    Giao_Vien=3
    Thu_Ngan=4
    Quan_Ly=5

class Level(enum.Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3

class PaymentStatus(enum.Enum):
    CHUA_THANH_TOAN = 1
    DA_THANH_TOAN = 2

class ScoreType(enum.Enum):
    GIUA_KY = 1
    CUOI_KY = 2
    CHUYEN_CAN = 3
    # KIEM_TRA_MIENG = 4

class Result(enum.Enum):
    DAT = 1
    KHONG_DAT = 2

class BaseModel(db.Model):
    __abstract__ = True
    id= Column(Integer, primary_key=True, autoincrement=True)
    active= Column(Boolean, default=True)


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    user_role = Column(Enum(UserRole), default=UserRole.Hoc_Vien)
    avatar = Column(String(255), default='http://res.cloudinary.com/dgpiotsmt/image/upload/v1764773563/j3nstjmidk7m0ynjxqkn.jpg')

    def __str__(self):
        return self.name

class Category(BaseModel):
    name = Column(String(50), unique=True)


    def __str__(self):
        return self.name

class Course(BaseModel):
    name = Column(String(50),nullable=False, unique=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(255), default='default.jpg')

    level = Column(Enum(Level), default=Level.BEGINNER)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', backref='courses', lazy=True)


    def __str__(self):
        return self.name

class Class(BaseModel):
    name = Column(String(50), nullable=False)
    start_date = Column(DateTime)
    schedule = Column(String(100))
    room = Column(String(50))
    max_students = Column(Integer, default=25)

    teacher_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    teacher = relationship('User', backref='teaching_classes', lazy=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    course = relationship('Course', backref='classes', lazy=True)

    def __str__(self):
        return self.name

class Enrollment(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('class.id'), nullable=False)
    enrolled_date = Column(DateTime, default=datetime.now)

    user = relationship('User', backref='enrollments', lazy=True)
    my_class = relationship('Class', backref='enrollments', lazy=True)


class Score(BaseModel):
    value = Column(Float, nullable=False)
    score_type = Column(Enum(ScoreType), nullable=False)

    enrollment_id = Column(Integer, ForeignKey('enrollment.id'), nullable=False)
    enrollment = relationship('Enrollment', backref='scores', lazy=True)

    def __str__(self):
        return f"{self.score_type.name}: {self.value}"

class Receipt(BaseModel):
    status = Column(Enum(PaymentStatus), default=PaymentStatus.CHUA_THANH_TOAN)
    created_date = Column(DateTime, default=datetime.now)
    payment_date = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', foreign_keys=[user_id], backref='receipts', lazy=True)

    cashier_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    cashier = relationship('User', foreign_keys=[cashier_id], backref='cashier_receipts', lazy=True)

    def __str__(self):
        return f"HĐ: {self.id}"

class ReceiptDetail(BaseModel):
    receipt_id = Column(Integer, ForeignKey('receipt.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('class.id'), nullable=False)
    price = Column(Float, default=0)

    receipt = relationship('Receipt', backref='details', lazy=True)
    my_class = relationship('Class', backref='receipt_details', lazy=True)

class Attendance(BaseModel):
    date = Column(Date, default=datetime.now)
    present = Column(Boolean, default=True)

    enrollment_id = Column(Integer, ForeignKey('enrollment.id'), nullable=False)
    enrollment = relationship('Enrollment', backref='attendances', lazy=True)

    def __str__(self):
        return f"{self.date.strftime('%d/%m')}: {'Có' if self.present else 'Vắng'}"








