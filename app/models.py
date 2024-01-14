import enum

from app import db, app
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum, Date, DateTime
from datetime import date, datetime
from sqlalchemy.orm import relationship


class UserRoleEnum(enum.Enum):
    ADMIN = 1
    DOCTOR = 2
    NURSE = 3
    OTHER = 4


class GenderEnum(enum.Enum):
    Male = 'Nam'
    Female = 'Nữ'


class DrugUnitEnum(enum.Enum):
    Tablet = 'Viên'
    Bottle = 'Chai'
    Vial = 'Vĩ'


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(200),
                    default="https://res.cloudinary.com/dbkmrrnge/image/upload/v1704561026/images_i0udr0.png")
    user_role = Column(Enum(UserRoleEnum))
    doctor = relationship('Doctor', backref='user', uselist=False)

    def __str__(self):
        return self.username


class Doctor(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    specialization = Column(String(50))
    phone = Column(String(20), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    image = Column(String(200))
    join_date = Column(Date, default=date.today())
    active = Column(Boolean, default=True)
    user_id = Column(Integer, ForeignKey(User.id))
    appoint = relationship('Appointment', backref='doctor', lazy=True)
    patient = relationship('Patient', backref='doctor', lazy=True)

    def __str__(self):
        return self.name


class Patient(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    gender = Column(Enum(GenderEnum))
    address = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    birth_day = Column(Date)
    injury = Column(String(100), nullable=False)
    appoint = relationship('Appointment', backref='patient', lazy=True)
    doc_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)
    medical_record = relationship('MedicalRecord', backref='medi_rec', lazy=True)
    receipts = relationship('Receipt', backref='patient', lazy=True)

    def __str__(self):
        return self.name


class Appointment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)
    appoint_date = Column(Date)
    status = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class Medicine(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    unit = Column(Enum(DrugUnitEnum))
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    usage = Column(String(100))

    def __str__(self):
        return self.name


class MedicalRecord(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    symptoms = Column(String(100), nullable=False)
    diagnosis = Column(String(100), nullable=False)
    created_date = Column(Date, default=date.today())

    def __str__(self):
        return self.name


class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)
    receipt_details = relationship('ReceiptDetail', backref='receipt', lazy=True)


class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_fee = Column(Float, default=100000)
    medicine_fee = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()

        # import hashlib

        # u = User(username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #         user_role=UserRoleEnum.ADMIN)

        # doc1 = Doctor(name='Nguyễn Văn An', specialization='Nội Khoa', phone='094144153', email='annguyen@gmail.com')
        # doc2 = Doctor(name='Nguyễn Thị Mai Anh', specialization='Nhi Khoa', phone='07531359',
        #             email='maianh123@gmail.com')
        # doc3 = Doctor(name='Võ Quốc Pháp', specialization='Ngoại Khoa', phone='035416418', email='drquocphap@gmail.com')

        # u1 = User(username='doctor1',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.DOCTOR)
        # u2 = User(username='doctor2',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.DOCTOR)
        # u3 = User(username='doctor3',
        #          password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
        #          user_role=UserRoleEnum.DOCTOR)

        # db.session.add(u2)
        # db.session.add(doc1)
        # db.session.add(doc2)
        # db.session.add(doc3)

        # db.session.add(u)
        # db.session.add(u1)
        # db.session.add(u2)
        # db.session.add(u3)
        db.session.commit()
