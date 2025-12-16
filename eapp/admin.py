# eapp/admin.py

import hashlib
from datetime import datetime
from flask import redirect, request, url_for
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from eapp.models import Category, Course, UserRole, Class, User
from eapp import db, app, dao


# 1. BẢO VỆ TRANG CHỦ ADMIN (/admin)
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or current_user.user_role != UserRole.ADMIN:
            return redirect('/')  # Đá về trang chủ nếu không phải Admin
        return super(MyAdminIndexView, self).index()


# 2. CLASS CHA BẢO VỆ CÁC MODEL (Category, Course...)
class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


# 3. Kế thừa từ class đã bảo mật
class CourseView(AuthenticatedModelView):  # <-- Sửa ModelView thành AuthenticatedModelView
    column_list = ['id', 'name', 'price', 'level', 'category']
    column_searchable_list = ['name']
    column_filters = ['id', 'name', 'price']
    can_export = True
    edit_modal = True
    page_size = 30


class UserView(AuthenticatedModelView):  # <-- Sửa AdminView thành AuthenticatedModelView
    column_list = ['id', 'name', 'username', 'email', 'user_role', 'active']
    form_columns = ['name', 'username', 'password', 'email', 'user_role', 'active']

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = str(hashlib.md5(form.password.data.encode('utf-8')).hexdigest())


class ClassView(AuthenticatedModelView):  # <-- Sửa AdminView thành AuthenticatedModelView
    column_list = ['name', 'course', 'teacher', 'schedule', 'room']
    form_columns = ['name', 'course', 'teacher', 'schedule', 'room', 'start_date', 'max_students']
    column_labels = dict(name='Tên Lớp', course='Thuộc Khóa', teacher='Giáo Viên',
                         schedule='Lịch học', start_date='Khai giảng',
                         max_students='Sĩ số', room='Phòng')


class StatsView(BaseView):
    @expose('/')
    def index(self):
        # ... (Code thống kê giữ nguyên) ...
        year = request.args.get('year', datetime.now().year)
        revenue_data = dao.stats_revenue_by_month(year)
        course_data = dao.stats_courses_enrollment()
        pass_rate_data = dao.stats_pass_rate_by_course()  # <-- Dữ liệu tỷ lệ đạt

        return self.render('admin/stats.html',
                           revenue_data=revenue_data,
                           course_data=course_data,
                           pass_rate_data=pass_rate_data,
                           year=year)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/')

    def is_accessible(self):
        return current_user.is_authenticated


# 4. KHỞI TẠO ADMIN VỚI INDEX VIEW BẢO MẬT
admin = Admin(app=app,
              name="DOK's Admin",
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())  # <-- Quan trọng: Chặn ngay cửa chính

# 5. THÊM VIEW (Tất cả đều phải dùng AuthenticatedModelView)
# Category dùng trực tiếp AuthenticatedModelView thay vì ModelView gốc
admin.add_view(AuthenticatedModelView(Category, db.session, name='Danh mục'))
admin.add_view(CourseView(Course, db.session, name='Khóa học'))
admin.add_view(ClassView(Class, db.session, name='Lớp học'))
admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(StatsView(name='Thống kê báo cáo'))
admin.add_view(LogoutView(name='Đăng xuất'))