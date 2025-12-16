from datetime import datetime

from flask import render_template, request, jsonify, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from eapp import app, dao, login
from eapp.dao import add_user
from eapp.models import UserRole, User, Class, ScoreType
import math

@app.route('/')
def index():

    courses = dao.load_courses(cate_id=request.args.get('category_id'),
                               kw=request.args.get('kw'),
                               page=int(request.args.get('page',1)))


    return render_template('index.html', courses=courses,
                           pages=math.ceil(dao.count_courses()/app.config['PAGE_SIZE']))

@app.route('/login')
def login_view():
    return render_template('login.html')

@app.route('/register')
def register_view():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_process():
    data = request.form

    password = data.get('password')
    confirm = data.get('confirm')
    if password != confirm:
        err_msg = 'Mật khẩu không khớp'
        return render_template('register.html', err_msg=err_msg)

    try:
        add_user(name=data.get('name'),
                 username=data.get('username'),
                 password=password,
                 avatar=request.files.get('avatar'),
                 email=data.get('email'))
        return redirect('/login')
    except Exception as ex:
        return render_template('register.html', err_msg=str(ex))


@app.context_processor
def common_response():
    return {
        'categories':dao.load_categories(),
        'count_students': dao.count_students,
        'is_user_registered': dao.is_user_registered,
        'get_score': dao.get_score,
        'ScoreType': ScoreType,
        'get_attendance': dao.get_attendance_status,
        'calc_stats': dao.calculate_stats
    }

@app.route('/login', methods=['POST'])
def login_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user= dao.auth_user(username=username, password=password)
    if user:
        login_user(user)

    next = request.args.get('next')
    return redirect(next if next else '/')

@login.user_loader
def load_user(id):
    return dao.get_user_by_id(id)

@app.route('/logout')
def logout_process():
    logout_user()
    return redirect('/login')


@app.route('/register-course', methods=['post'])
@login_required
def register_course():
    data = request.form
    class_id = data.get('class_id')

    if dao.add_receipt(user_id=current_user.id, class_id=class_id):
        print("DEBUG: Đăng ký THÀNH CÔNG!")
        flash('Đăng ký thành công! Vui lòng thanh toán.', 'success')
    else:
        print("DEBUG: Đăng ký THẤT BẠI (Có thể do Lớp đầy hoặc Lỗi DB)")
        flash('Đăng ký thất bại!', 'danger')

    return redirect('/')

@app.route('/courses/<int:course_id>')
def course_detail_process(course_id):
    c = dao.get_course_by_id(course_id)

    return render_template('details.html', course=c)


@app.route('/cashier')
@login_required
def cashier_view():
    if current_user.user_role != UserRole.Thu_Ngan and current_user.user_role != UserRole.ADMIN:
        return redirect('/')

    kw = request.args.get('kw')
    receipts = []
    if kw:
        receipts = dao.get_unpaid_receipts_by_user_kw(kw)

    return render_template('cashier.html', receipts=receipts)

@app.route('/api/pay/<int:receipt_id>', methods=['POST'])
@login_required
def pay_process(receipt_id):
    if current_user.user_role != UserRole.Thu_Ngan:
        return jsonify({'status': 'failed', 'msg': 'Không có quyền thực hiện'})

    result, message = dao.pay_receipt(receipt_id, cashier_id=current_user.id)

    if result:
        return jsonify({'status': 'success', 'msg': message})
    else:
        return jsonify({'status': 'failed', 'msg': message})

@app.route('/teacher')
@login_required
def teacher_view():
    if current_user.user_role != UserRole.Giao_Vien:
        return redirect('/')

    my_classes = dao.get_classes_by_teacher(current_user.id)
    return render_template('teacher/index.html', classes=my_classes)

@app.route('/teacher/class/<int:class_id>')
@login_required
def teacher_class_detail(class_id):
    students = dao.get_students_in_class(class_id)
    my_class = Class.query.get(class_id)

    return render_template('teacher/gradebook.html',
                           students=students,
                           my_class=my_class)


# 4. API Xử lý lưu điểm (Nhận JSON từ JavaScript)
@app.route('/api/update-score', methods=['POST'])
@login_required
def update_score_process():
    data = request.json

    if dao.add_or_update_score(data.get('enrollment_id'),
                               data.get('score_type'),
                               data.get('value')):
        return jsonify({'status': 'success'})

    return jsonify({'status': 'failed'})


@app.route('/teacher/class/<int:class_id>/attendance')
@login_required
def teacher_attendance(class_id):
    students = dao.get_students_in_class(class_id)
    my_class = Class.query.get(class_id)

    today = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

    return render_template('teacher/attendance.html',
                           students=students,
                           my_class=my_class,
                           today=today)


# 3. API Lưu điểm danh (AJAX gọi vào đây)
@app.route('/api/attendance', methods=['POST'])
@login_required
def save_attendance_process():
    data = request.json
    # data gồm: enrollment_id, date, present (true/false)
    if dao.save_attendance(data.get('enrollment_id'),
                           data.get('date'),
                           data.get('present')):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failed'})

# --- eapp/index.py ---

@app.route('/my-courses')
@login_required
def my_courses():
    return render_template('student/my_courses.html')


@app.route('/api/cancel-reg/<int:detail_id>', methods=['DELETE'])
@login_required
def cancel_registration_api(detail_id):
    if dao.delete_receipt_detail(detail_id):
        return jsonify({'status': 'success'})

    return jsonify({'status': 'failed', 'msg': 'Lỗi khi xóa dữ liệu'})


@app.route('/manager', methods=['GET', 'POST'])
@login_required
def manager_view():
    if current_user.user_role != UserRole.Quan_Ly and current_user.user_role != UserRole.ADMIN:
        return redirect('/')

    if request.method == 'POST':
        action = request.form.get('action')

        # --- Cập nhật Học phí (Code cũ - Giữ nguyên) ---
        if action == 'update_price':
            level = request.form.get('level')
            category_id = request.form.get('category_id')
            price = request.form.get('price')
            try:
                success, count = dao.update_course_price(level, category_id, float(price))
                if success:
                    flash(f'Đã cập nhật giá cho {count} khóa học!', 'success')
                else:
                    flash('Lỗi cập nhật!', 'danger')
            except:
                flash('Dữ liệu không hợp lệ', 'danger')

        # --- CẬP NHẬT SĨ SỐ (CODE MỚI) ---
        elif action == 'update_size':
            class_id = request.form.get('class_id')  # Lấy ID lớp
            size = request.form.get('max_students')

            try:
                success, class_name = dao.update_class_max_students(class_id, int(size))
                if success:
                    flash(f'Đã thay đổi sĩ số lớp "{class_name}" thành {size} học viên!', 'success')
                else:
                    flash('Lỗi khi cập nhật sĩ số!', 'danger')
            except ValueError:
                flash('Vui lòng nhập số nguyên!', 'danger')

        return redirect('/manager')

    # --- GET: Gửi thêm danh sách lớp (classes) sang HTML ---
    categories = dao.load_categories()
    classes = dao.load_active_classes()  # <--- MỚI

    return render_template('manager.html',
                           categories=categories,
                           classes=classes)

if __name__ == '__main__':
    from eapp import admin
    app.run(debug=True)


