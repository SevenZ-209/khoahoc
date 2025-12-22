import hashlib
from datetime import datetime
from sqlalchemy import func
import cloudinary.uploader

from eapp.models import Category, Course, User, db, Receipt, PaymentStatus, ReceiptDetail, Class, Enrollment, Score, \
    ScoreType, Attendance, Result, Level
from eapp import app

def load_categories():
    return Category.query.all()

def load_courses(cate_id=None, kw=None, page=1):
    query = Course.query
    if kw:
        query = query.filter(Course.name.contains(kw))

    if cate_id:
        query = query.filter(Course.category_id.__eq__(cate_id))

    if page:
        start = (page - 1) * app.config['PAGE_SIZE']
        query = query.slice(start, start + app.config['PAGE_SIZE'])

    return query.all()

def count_courses():
    return Course.query.count()

def get_course_by_id(course_id):
    return Course.query.get(course_id)

def get_user_by_id(id):
    return User.query.get(id)

def count_students(class_id):
    return Enrollment.query.filter(Enrollment.class_id == class_id).count()

def get_user_by_username(username):
    return User.query.filter_by(username=username.strip()).first()

def auth_user(username, password):
    password= str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username==username.strip(),
                                User.password==password).first()

def check_username(username):
    if not username:
        return False

    user = get_user_by_username(username)
    return user is not None

def check_email(email):
    if not email:
        return False
    user = User.query.filter_by(email=email.strip()).first()
    return user is not None

def add_user(name, username, password, avatar, email):
    if check_username(username):
        raise Exception('Tên đăng nhập đã tồn tại')
    if check_email(email):
        raise Exception('Địa chỉ email đã tồn tại')
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name, username=username.strip(), password=password, email=email.strip())
    if avatar:
        res = cloudinary.uploader.upload(avatar)
        u.avatar = res.get('secure_url')

    db.session.add(u)
    db.session.commit()

def add_receipt(user_id, class_id):
    my_class = Class.query.get(class_id)
    if not my_class:
        return False, "Lớp học không tồn tại!"

    if is_user_registered(user_id, class_id):
        return False, "Học viên này ĐÃ đăng ký lớp này rồi (hoặc đang chờ thanh toán)!"

    current_students = count_students(class_id)
    if current_students >= my_class.max_students:
        return False, "Lớp đã đủ sĩ số, không thể thêm!"

    try:
        course_price = my_class.course.price
        receipt = Receipt(user_id=user_id,
                          created_date=datetime.now(),
                          status=PaymentStatus.CHUA_THANH_TOAN)

        db.session.add(receipt)
        detail = ReceiptDetail(receipt=receipt,
                               class_id=class_id,
                               price=course_price)

        db.session.add(detail)
        db.session.commit()
        return True, "Tạo hóa đơn thành công!"

    except Exception as ex:
        print(f"Lỗi tạo hóa đơn: {ex}")
        db.session.rollback()
        return False, "Lỗi hệ thống: " + str(ex)

def delete_receipt_detail(detail_id):
    try:
        detail = ReceiptDetail.query.get(detail_id)
        if detail:
            if detail.receipt.status == PaymentStatus.DA_THANH_TOAN:
                return False, "Không thể hủy! Khóa học này đã đóng học phí."

            receipt = detail.receipt
            db.session.delete(detail)

            if len(receipt.details) == 0:
                db.session.delete(receipt)
            db.session.commit()
            return True, "Hủy đăng ký thành công!"

        return False, "Không tìm thấy thông tin đăng ký."
    except Exception as ex:
        print(ex)
        return False, "Lỗi hệ thống: " + str(ex)

def is_user_registered(user_id, class_id):
    return ReceiptDetail.query.join(Receipt).filter(
        Receipt.user_id == user_id,
        ReceiptDetail.class_id == class_id
    ).first() is not None

def get_enrollment(user_id, class_id):
    return Enrollment.query.filter_by(user_id=user_id, class_id=class_id).first()

def get_classes_by_teacher(teacher_id):
    return Class.query.filter(Class.teacher_id == teacher_id).all()

def get_students_in_class(class_id):
    return Enrollment.query.filter(Enrollment.class_id == class_id).all()

def add_or_update_score(enrollment_id, score_type_value, value):
    score_enum = ScoreType(int(score_type_value))
    score = Score.query.filter(
        Score.enrollment_id == enrollment_id,
        Score.score_type == score_enum
    ).first()

    if score:
        score.value = value
    else:
        score = Score(value=value,
                      score_type=score_enum,
                      enrollment_id=enrollment_id)
        db.session.add(score)

    db.session.commit()
    return True

def get_score(enrollment, score_type_enum):
    if not enrollment or not enrollment.scores:
        return ''
    for s in enrollment.scores:
        if s.score_type == score_type_enum:
            return s.value
    return ''

def get_scores_by_enrollment(enrollment_id):
    return Score.query.filter(Score.enrollment_id == enrollment_id).all()

def calculate_stats(enrollment_id):
    scores = get_scores_by_enrollment(enrollment_id)

    total = 0

    if scores:
        for s in scores:
            total += s.value

    num_columns = len(ScoreType)

    avg = 0
    if num_columns > 0:
        avg = total / num_columns

    avg = round(avg, 2)

    if avg >= 5.0:
        final_result = Result.DAT
    else:
        final_result = Result.KHONG_DAT

    return {
        'avg': avg,
        'result_enum': final_result,
        'result_text': "Đạt" if final_result == Result.DAT else "Không Đạt",
        'is_passed': final_result == Result.DAT
    }

def save_attendance(enrollment_id, date_str, is_present):
    try:
        attend_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        enrollment = Enrollment.query.get(enrollment_id)
        attendance = None

        for a in enrollment.attendances:
            if a.date.date() == attend_date:
                attendance = a
                break

        if attendance:
            attendance.present = is_present
        else:
            attendance = Attendance(enrollment_id=enrollment_id,
                                    date=attend_date,
                                    present=is_present)
            db.session.add(attendance)
        db.session.commit()
        return True, "Lưu thành công"
    except Exception as ex:
        return False, str(ex)


def get_attendance_status(enrollment, date_str):
    try:
        target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        for a in enrollment.attendances:
            if a.date.date() == target_date:
                return a.present
    except:
        pass
    return None

def get_unpaid_receipts_by_user_kw(kw):
    query = Receipt.query.join(Receipt.user).filter(Receipt.status == PaymentStatus.CHUA_THANH_TOAN)

    if kw:
        query = query.filter((User.name.contains(kw)) | (User.username.contains(kw)))

    return query.all()


def pay_receipt(receipt_id, cashier_id=None):
    receipt = Receipt.query.get(receipt_id)

    if not receipt:
        return False, "Hóa đơn không tồn tại"

    for detail in receipt.details:
        current_count = count_students(detail.class_id)
        max_students = detail.my_class.max_students

        if current_count >= max_students:
            return False, f"Thất bại! Lớp '{detail.my_class.name}' đã đủ sĩ số ({current_count}/{max_students})."

    try:
        receipt.status = PaymentStatus.DA_THANH_TOAN
        receipt.created_date = datetime.now()

        if cashier_id:
            receipt.cashier_id = cashier_id

        for detail in receipt.details:
            check = get_enrollment(receipt.user_id, detail.class_id)
            if not check:
                enrollment = Enrollment(user_id=receipt.user_id, class_id=detail.class_id)
                db.session.add(enrollment)

        db.session.commit()
        return True, "Thanh toán thành công!"

    except Exception as ex:
        return False, str(ex)

def load_active_classes():
    return Class.query.filter(Class.active == True).order_by(Class.id.desc()).all()

def update_course_price(level_name, category_id, new_price):
    try:
        level_enum = Level[level_name]

        query = Course.query.filter(
            Course.level == level_enum,
            Course.category_id == int(category_id)
        )

        row_count = query.update({Course.price: new_price})
        db.session.commit()

        return True, row_count
    except Exception as ex:
        print(f"Lỗi update giá: {ex}")
        db.session.rollback()
        return False, "Lỗi hệ thống: " + str(ex)

def update_class_max_students(class_id, new_max):
    try:
        my_class = Class.query.get(class_id)
        if my_class:
            current_count = count_students(class_id)
            if new_max < current_count:
                return False, f"Không thể giảm xuống {new_max}! Lớp đang có {current_count} học viên."
            my_class.max_students = new_max
            db.session.commit()
            return True, f"Đã cập nhật sĩ số lớp {my_class.name} thành {new_max}."

    except Exception as ex:
        print(ex)
        db.session.rollback()
    return False, "Lỗi hệ thống!"

def stats_revenue(year=None):
    if not year:
        year = datetime.now().year

    return db.session.query(func.extract('month', Receipt.created_date),
                            func.sum(ReceiptDetail.price)) \
        .join(Receipt, Receipt.id == ReceiptDetail.receipt_id) \
        .filter(func.extract('year', Receipt.created_date) == year,
                Receipt.status == PaymentStatus.DA_THANH_TOAN) \
        .group_by(func.extract('month', Receipt.created_date)) \
        .order_by(func.extract('month', Receipt.created_date)).all()

def stats_student_by_course():
    return db.session.query(Course.name, func.count(Enrollment.id))\
                     .join(Class, Class.course_id == Course.id)\
                     .join(Enrollment, Enrollment.class_id == Class.id)\
                     .group_by(Course.id, Course.name).all()

def stats_pass_fail_by_course():
    courses = Course.query.all()
    stats_data = []

    for course in courses:
        pass_count = 0
        fail_count = 0

        for my_class in course.classes:
            for enrollment in my_class.enrollments:
                result = calculate_stats(enrollment.id)
                if result['is_passed']:
                    pass_count += 1
                else:
                    fail_count += 1

        if pass_count > 0 or fail_count > 0:
            stats_data.append({
                'course_name': course.name,
                'pass': pass_count,
                'fail': fail_count
            })

    return stats_data

def count_courses_by_category():
    return db.session.query(Category.name, func.count(Course.id))\
                     .join(Course, Course.category_id == Category.id, isouter=True)\
                     .group_by(Category.id, Category.name).all()

