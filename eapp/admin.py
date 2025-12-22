import hashlib
from datetime import datetime
from flask import redirect, request, url_for
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from eapp.models import Category, Course, UserRole, Class, User
from eapp import db, app, dao

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or current_user.user_role != UserRole.ADMIN:
            return redirect('/')

        return self.render('admin/index.html', stats = dao.count_courses_by_category())



class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class CourseView(AuthenticatedModelView):
    column_list = ['id', 'name', 'price', 'level', 'category']
    column_searchable_list = ['name']
    column_filters = ['id', 'name', 'price']
    can_export = True
    edit_modal = True
    page_size = 30

class UserView(AuthenticatedModelView):
    column_list = ['id', 'name', 'username', 'email', 'user_role', 'active']
    form_columns = ['name', 'username', 'password', 'email', 'user_role', 'active']

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = str(hashlib.md5(form.password.data.encode('utf-8')).hexdigest())

class ClassView(AuthenticatedModelView):
    column_list = ['name', 'course', 'teacher', 'schedule', 'room', 'active']
    form_columns = ['name', 'course', 'teacher', 'schedule', 'room', 'start_date', 'max_students', 'active']
    column_labels = dict(name='Tên Lớp', course='Thuộc Khóa', teacher='Giáo Viên',
                         schedule='Lịch học', start_date='Khai giảng',
                         max_students='Sĩ số', room='Phòng')

class StatsView(BaseView):
    @expose('/')
    def index(self):
        year = datetime.now().year

        revenue_data = dao.stats_revenue(year)
        student_data = dao.stats_student_by_course()
        pass_fail_data = dao.stats_pass_fail_by_course()

        return self.render('admin/stats.html',
                           revenue_data=revenue_data,
                           student_data=student_data,
                           pass_fail_data=pass_fail_data,
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

admin = Admin(app=app,
              name="DOK's Admin",
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())

admin.add_view(AuthenticatedModelView(Category, db.session, name='Danh mục'))
admin.add_view(CourseView(Course, db.session, name='Khóa học'))
admin.add_view(ClassView(Class, db.session, name='Lớp học'))
admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(StatsView(name='Thống kê & Báo cáo', endpoint='stats'))
admin.add_view(LogoutView(name='Đăng xuất'))