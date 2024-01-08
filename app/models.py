import enum

from app import db, app
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, Enum, DateTime, Time
from datetime import datetime
from sqlalchemy.orm import relationship


class UserRoleEnum(enum.Enum):
    ADMIN = 1
    DOCTOR = 2
    NURSE = 3
    OTHER = 4


class GenderEnum(enum.Enum):
    Male = 0
    Female = 1


class DrugUnitEnum(enum.Enum):
    Tablet = 1
    Bottle = 2
    Vial = 3


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(200),
                    default="https://res.cloudinary.com/dbkmrrnge/image/upload/v1704561026/images_i0udr0.png")
    user_role = Column(Enum(UserRoleEnum))

    def __str__(self):
        return self.name


class Doctor(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    specialization = Column(String(50))
    phone = Column(String(20), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    image = Column(String(200))
    join_date = Column(DateTime, default=datetime.now())
    active = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class Patient(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    gender = Column(Enum(GenderEnum))
    address = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False, unique=True)
    email = Column(String(50), unique=True)
    birth_day = Column(DateTime)

    def __str__(self):
        return self.name


class Appointment(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    doctor_id = Column(Integer, ForeignKey(Doctor.id), nullable=False)
    appoint_date = Column(DateTime, default=datetime.now())
    appoint_time = Column(Time)
    status = Column(Boolean, default=False)

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


class MedicalBill(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey(Patient.id), nullable=False)
    med_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    symptoms = Column(String(100), nullable=False)
    diagnosis = Column(String(100), nullable=False)
    created_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib

        u = User(name='Admin', username='admin', password=str(hashlib.md5('123456'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)

        doc1 = Doctor(name='Nguyễn Văn An', specialization='Nội Khoa', phone='094144153', email='annguyen@gmail.com')
        doc2 = Doctor(name='Nguyễn Thị Mai Anh', specialization='Nhi Khoa', phone='07531359',
                      email='maianh123@gmail.com')
        doc3 = Doctor(name='Võ Quốc Pháp', specialization='Ngoại Khoa', phone='035416418', email='drquocphap@gmail.com')

        db.session.add(u)
        db.session.add(doc1)
        db.session.add(doc2)
        db.session.add(doc3)
        db.session.commit()
