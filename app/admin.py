from markupsafe import Markup

from app import app, db
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from app.models import Doctor, Patient, User, UserRoleEnum, Medicine
from flask_login import logout_user, current_user
from flask import redirect
from flask_admin.form.upload import ImageUploadField

admin = Admin(app=app, name='Quản Lý Phòng Khám', template_mode='bootstrap4')


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class DoctorView(AuthenticatedAdmin):
    with app.app_context():
        user_id = User.query.all()
    column_list = ['id', 'image', 'name', 'specialization', 'phone', 'email', 'join_date', 'active', 'user_id']
    column_hide_backrefs = False
    can_export = True
    edit_modal = True
    create_modal = True
    details_modal = True
    can_view_details = True
    column_searchable_list = ['name']
    column_labels = {
        'image': 'Ảnh',
        'name': 'Họ tên',
        'specialization': 'Chuyên môn',
        'phone': 'SĐT',
        'email': 'Email',
        'join_date': 'Ngày gia nhập',
        'active': 'Hiện trạng'
    }

    def display_image(view, context, model, name):
        if not model.image:
            return ''

        return Markup(f'<img src="{model.image}" width="30" height="30"> ')

    column_formatters = {
        'image': display_image
    }

    form_excluded_columns = 'appoint'


class PatientView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'gender', 'address', 'phone', 'birth_day', 'injury']
    can_export = True
    edit_modal = True
    create_modal = True
    details_modal = True
    can_view_details = True
    column_filters = ['birth_day']
    column_searchable_list = ['name']
    column_labels = {
        'name': 'Họ tên',
        'gender': 'Giới tính',
        'address': 'Địa chỉ',
        'phone': 'SĐT',
        'birth_day': 'Ngày sinh',
        'injury': 'Triệu chứng',
    }


class UserView(AuthenticatedAdmin):
    column_list = ['id', 'username', 'password', 'user_role']
    can_export = True
    edit_modal = True
    create_modal = True
    details_modal = True
    can_view_details = True
    column_searchable_list = ['username']


class MedicineView(AuthenticatedAdmin):
    column_list = ['id', 'name', 'unit', 'quantity', 'price', 'usage']
    can_export = True
    create_modal = True
    can_view_details = True
    edit_modal = True
    column_searchable_list = ['name']


class LogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect("/admin")


admin.add_view(DoctorView(Doctor, db.session, name='Bác sĩ'))
admin.add_view(PatientView(Patient, db.session, name='Bệnh nhân'))
admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(MedicineView(Medicine, db.session, name='Thuốc'))
admin.add_view(LogoutView(name='Đăng xuất'))
