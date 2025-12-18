import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, Enum, ForeignKey, DateTime
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
    courses = relationship('Course', backref='category', lazy=True)

    def __str__(self):
        return self.name

class Course(BaseModel):
    name = Column(String(50),nullable=False, unique=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(255), default='default.jpg')

    level = Column(Enum(Level), default=Level.BEGINNER)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)


    def __str__(self):
        return self.name

class Class(BaseModel):
    name = Column(String(50), nullable=False)
    start_date = Column(DateTime)
    schedule = Column(String(100))
    room = Column(String(50))
    max_students = Column(Integer, default=25)

    teacher_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    teacher = relationship('User', backref='teaching_classes', lazy=True)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    course = relationship('Course', backref='classes', lazy=True)

    def __str__(self):
        return self.name

class Enrollment(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('class.id'), nullable=False)
    enrolled_date = Column(DateTime, default=datetime.now)

    scores = relationship('Score', backref='enrollment', lazy=True)
    user = relationship('User', backref='enrollments', lazy=True)
    my_class = relationship('Class', backref='enrollments', lazy=True)


class Score(BaseModel):
    value = Column(Float, nullable=False)
    score_type = Column(Enum(ScoreType), nullable=False)
    enrollment_id = Column(Integer, ForeignKey('enrollment.id'), nullable=False)

    def __str__(self):
        return f"{self.score_type.name}: {self.value}"

class Receipt(BaseModel):
    total_amount = Column(Float, default=0)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.CHUA_THANH_TOAN)
    created_date = Column(DateTime, default=datetime.now)

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    cashier_id = Column(Integer, ForeignKey('user.id'), nullable=True)

    user = relationship('User', foreign_keys=[user_id], backref='receipts', lazy=True)
    cashier = relationship('User', foreign_keys=[cashier_id], backref='cashier_receipts', lazy=True)

    def __str__(self):
        return f"HĐ: {self.code} - {self.total_amount}"


class Attendance(BaseModel):
    date = Column(DateTime, default=datetime.now)
    present = Column(Boolean, default=True)

    enrollment_id = Column(Integer, ForeignKey('enrollment.id'), nullable=False)
    enrollment = relationship('Enrollment', backref='attendances', lazy=True)

    def __str__(self):
        return f"{self.date.strftime('%d/%m')}: {'Có' if self.present else 'Vắng'}"

class ReceiptDetail(BaseModel):
    receipt_id = Column(Integer, ForeignKey('receipt.id'), nullable=False)
    class_id = Column(Integer, ForeignKey('class.id'), nullable=False)
    price = Column(Float, default=0)

    receipt = relationship('Receipt', backref='details', lazy=True)
    my_class = relationship('Class', backref='receipt_details', lazy=True)

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
        import hashlib
        u=User(name='Admin', username='admin', email='admin@gmail.com' , password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
               user_role =UserRole.ADMIN)
        db.session.add(u)
        db.session.commit()

        ql=User(name='QuanLy', username='quanly', email='quanly@gmail.com', password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.Quan_Ly)
        db.session.add(ql)
        db.session.commit()

        hv=User(name='Khoa', username='lekhoa', email='123@gmail.com', password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),user_role=UserRole.Hoc_Vien)
        db.session.add(hv)
        db.session.commit()

        hv1 = User(name='Khang', username='dangkhang', email='khang123@gmail.com',
                  password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.Hoc_Vien)
        db.session.add(hv1)
        db.session.commit()

        hv2 = User(name='Long', username='danglong', email='long123@gmail.com',
                   password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.Hoc_Vien)
        db.session.add(hv2)
        db.session.commit()

        cashier1 = User(name='Long',
                       username='thungan',
                       email='thungan@gmail.com',
                       password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
                       user_role=UserRole.Thu_Ngan)

        db.session.add(cashier1)
        db.session.commit()

        teacher1 = User(name='Thầy Nguyễn Văn A',
                       username='gv1',
                       email='gv1@gmail.com',
                       password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()),
                       user_role=UserRole.Giao_Vien)

        db.session.add(teacher1)
        db.session.commit()

        c1 = Category(name ='English')
        c2 = Category(name='China')
        c3 = Category(name='Korea')
        c4 = Category(name='Japan')
        db.session.add_all([c1, c2, c3, c4])
        db.session.commit()

        courses =[{
            'name': 'Khóa tiếng anh mất gốc',
            'description' : 'Lấy lại căn bản',
            'price': 500000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764772124/txrww1mxs31fzd7up7ft.png',
            'level' : Level.BEGINNER,
            'category_id' : 1,
        },
        {
            'name': 'Khóa tiếng anh cơ bản',
            'description': 'Phản xạ nghe nói',
            'price': 700000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764772253/yff8ib2gmix2osk3lozh.png',
            'level': Level.INTERMEDIATE,
            'category_id': 1,
        },
        {
            'name': 'Khóa tiếng anh nâng cao',
            'description': 'Luyen thi',
            'price': 999000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764772353/lgddrgwvpw9lvdnvef4p.png',
            'level': Level.ADVANCED,
            'category_id': 1,
        },
        {
            'name': 'Khóa tiếng trung mất gốc',
            'description': 'Lấy lại căn bản',
            'price': 500000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764772494/srtj8a9ihgh50tr64uum.png',
            'level': Level.BEGINNER,
            'category_id': 2,
        },
        {
            'name': 'Khóa tiếng trung cơ bản',
            'description': 'Phản xạ nghe nói',
            'price': 700000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764772564/iwzyqzxowintmx9xxvav.png',
            'level': Level.INTERMEDIATE,
            'category_id': 2,
        },
        {
            'name': 'Khóa tiếng trung nâng cao',
            'description': 'Phản xạ nghe nói',
            'price': 999000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764772644/atvvypvjw3qqpxhy3yxe.png',
            'level': Level.ADVANCED,
            'category_id': 2,
        },
        {
            'name': 'Khóa tiếng hàn mất gốc',
            'description': 'Lấy lại căn bản',
            'price': 500000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764772815/tpx8s1izvj3izps2fmdk.png',
            'level': Level.BEGINNER,
            'category_id': 3,
        },
        {
            'name': 'Khóa tiếng hàn cơ bản',
            'description': 'Phản xạ nghe nói',
            'price': 700000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764772838/mhoroyhbg2igl4c78hab.png',
            'level': Level.INTERMEDIATE,
            'category_id': 3,
        },
        {
            'name': 'Khóa tiếng hàn nâng cao',
            'description': 'Luyen thi',
            'price': 999000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764772858/w3gnwyxaojvaz7oyd2k7.png',
            'level': Level.ADVANCED,
            'category_id': 3,
        },
        {
            'name': 'Khóa tiếng nhật mất gốc',
            'description': 'Lấy lại căn bản',
            'price': 500000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764773130/piwizcslfgwenldq6fav.png',
            'level': Level.BEGINNER,
            'category_id': 4,
        },
        {
            'name': 'Khóa tiếng nhật cơ bản',
            'description': 'Phản xạ nghe nói',
            'price': 700000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764773154/n9s83bcgjzcagrlvevcy.png',
            'level': Level.INTERMEDIATE,
            'category_id': 4,
            },
            {
            'name': 'Khóa tiếng nhật nâng cao',
            'description': 'Luyen thi',
            'price': 999000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764773183/nicdxqaw4kseg8bkmzfv.png',
            'level': Level.ADVANCED,
            'category_id': 4,
            }

        ]
        for c in courses:
            cro = Course(**c)
            db.session.add(cro)
        db.session.commit()

        course_ta = Course.query.filter_by(name='Khóa tiếng anh mất gốc').first()

        if course_ta:
            class1 = Class(name='TA-01 Sáng 2-4-6',
                           schedule='08:00 - 10:00 Thứ 2,4,6',
                           start_date=datetime(2025, 12, 15),
                           course_id=course_ta.id)

            class2 = Class(name='TA-02 Tối 3-5-7',
                           schedule='18:00 - 20:00 Thứ 3,5,7',
                           start_date=datetime(2025, 12, 20),
                           course_id=course_ta.id,
                           teacher_id=teacher1.id,
                           max_students=2
                          )

            db.session.add_all([class1, class2])
            db.session.commit()
            if class2 and hv:
                enrollment = Enrollment(user_id=hv.id, class_id=class2.id)

                db.session.add(enrollment)
                db.session.commit()
            if class1 and hv1:
                enrollment = Enrollment(user_id=hv1.id, class_id=class2.id)
                db.session.add(enrollment)
                db.session.commit()






