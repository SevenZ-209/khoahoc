from eapp import app, db
from eapp.models import *
import hashlib
from datetime import datetime

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        u = User(name='Admin', username='admin', email='admin@gmail.com',
                 password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.ADMIN)
        ql = User(name='QuanLy', username='quanly', email='quanly@gmail.com',
                  password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.Quan_Ly)
        hv = User(name='Khoa', username='lekhoa', email='123@gmail.com',
                  password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.Hoc_Vien)

        hv1 = User(name='Khang', username='dangkhang', email='khang123@gmail.com',
                   password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.Hoc_Vien)

        hv2 = User(name='Long', username='danglong', email='long123@gmail.com',
                   password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.Hoc_Vien)

        cashier1 = User(name='Long Thu Ngân', username='thungan', email='thungan@gmail.com',
                        password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.Thu_Ngan)

        teacher1 = User(name='Thầy Nguyễn Văn A', username='gv1', email='gv1@gmail.com',
                        password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.Giao_Vien)

        teacher2 = User(name='Cô Lê Thị B', username='gv2', email='gv2@gmail.com',
                        password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.Giao_Vien)

        teacher3 = User(name='Thầy Trần Văn C', username='gv3', email='gv3@gmail.com',
                        password=str(hashlib.md5('123'.encode('utf-8')).hexdigest()), user_role=UserRole.Giao_Vien)

        db.session.add_all([u, ql, hv, hv1, hv2, cashier1, teacher1, teacher2, teacher3])

        c1 = Category(name='English')
        c2 = Category(name='China')
        c3 = Category(name='Korea')
        c4 = Category(name='Japan')
        db.session.add_all([c1, c2, c3, c4])

        db.session.commit()

        courses = [{
            'name': 'Khóa tiếng anh mất gốc',
            'description': 'Lấy lại căn bản',
            'price': 500000,
            'image': 'http://res.cloudinary.com/dgpiotsmt/image/upload/v1764772124/txrww1mxs31fzd7up7ft.png',
            'level': Level.BEGINNER,
            'category_id': 1,
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


        course_ta_mg = Course.query.filter_by(name='Khóa tiếng anh mất gốc').first()
        course_trung_cb = Course.query.filter_by(name='Khóa tiếng trung cơ bản').first()
        course_han_mg = Course.query.filter_by(name='Khóa tiếng hàn mất gốc').first()
        course_nhat_nc = Course.query.filter_by(name='Khóa tiếng nhật nâng cao').first()

        classes_to_add = []

        if course_ta_mg:
            c1 = Class(name='TA-MG-01 Sáng 2-4-6',
                       schedule='08:00 - 10:00 Thứ 2,4,6',
                       start_date=datetime(2025, 12, 15),
                       room='P.101',
                       teacher_id=teacher1.id,
                       course_id=course_ta_mg.id)

            c2 = Class(name='TA-MG-02 Tối 3-5-7',
                       schedule='18:00 - 20:00 Thứ 3,5,7',
                       start_date=datetime(2025, 12, 20),
                       room='P.102',
                       max_students=15,
                       teacher_id=teacher1.id,
                       course_id=course_ta_mg.id)
            classes_to_add.extend([c1, c2])

        if course_trung_cb:
            c3 = Class(name='CN-CB-01 Chiều 3-5-7',
                       schedule='14:00 - 16:00 Thứ 3,5,7',
                       start_date=datetime(2025, 12, 16),
                       room='P.201',
                       teacher_id=teacher2.id,
                       course_id=course_trung_cb.id)
            classes_to_add.append(c3)

        if course_han_mg:
            c4 = Class(name='KR-MG-01 Sáng T7-CN',
                       schedule='08:00 - 11:00 T7, CN',
                       start_date=datetime(2025, 12, 21),
                       room='LAB-01',
                       teacher_id=teacher2.id,
                       course_id=course_han_mg.id)
            classes_to_add.append(c4)

        if course_nhat_nc:
            c5 = Class(name='JP-NC-01 Tối 2-4-6',
                       schedule='19:00 - 21:00 Thứ 2,4,6',
                       start_date=datetime(2025, 12, 22),
                       room='LAB-02',
                       max_students=10,
                       teacher_id=teacher3.id,
                       course_id=course_nhat_nc.id)
            classes_to_add.append(c5)

        if classes_to_add:
            db.session.add_all(classes_to_add)
            db.session.commit()

