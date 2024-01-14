import hashlib

from app.models import User, Doctor, Appointment, Patient, Medicine, Receipt


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf8')).hexdigest())

    return User.query.filter(User.username.__eq__(username),
                             User.password.__eq__(password)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_user():
    return User.query.all()


def get_doctors():
    return Doctor.query.all()


def get_appointments_by_doc_id(doctor_id, kw):
    appoints = Appointment.query.filter_by(doctor_id=doctor_id)
    if kw:
        appoints = appoints.join(Patient).filter(Patient.name.contains(kw))
    return appoints.all()


def get_patient_by_doc_id(doc_id, kw):
    patients = Patient.query.filter_by(doc_id=doc_id)

    if kw:
        patients = patients.filter(Patient.name.contains(kw))

    return patients.all()


def get_med():
    return Medicine.query.all()


def get_med_by_name(med_name):
    return Medicine.query.filter_by(name=med_name).first()


def get_pat_by_name(pat_name):
    return Patient.query.filter_by(name=pat_name).first()


def get_receipt():
    return Receipt.query.all()
