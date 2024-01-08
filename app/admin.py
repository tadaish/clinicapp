from app import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import Doctor

admin = Admin(app=app, name='Quản Lý Phòng Khám', template_mode='bootstrap4')


class DoctorView(ModelView):
    column_list = ['id', 'image', 'name', 'specialization', 'phone', 'email', 'join_date', 'active']
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
    can_set_page_size = True


admin.add_view(DoctorView(Doctor, db.session, name='Bác sĩ'))
