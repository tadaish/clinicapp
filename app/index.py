from datetime import date

from flask import render_template, request, redirect, session
from app import app, login, data, db
import data
from flask_login import login_user, logout_user, current_user
from app.models import UserRoleEnum, Patient, Appointment, Receipt, ReceiptDetail


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/appoint_booking", methods=['get', 'post'])
def appoint_booking():
    doc = data.get_doctors()
    message = None
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        address = request.form.get('address')
        b_day = request.form.get('birth_day')
        injury = request.form.get('injury')
        doc_id = request.form.get('doctor')
        app_date = request.form.get('appoint_date')

        pat = Patient(name=name, phone=phone, gender=gender, address=address, birth_day=b_day, injury=injury,
                      doc_id=doc_id)
        db.session.add(pat)
        db.session.flush()
        appoint = Appointment(patient_id=pat.id, doctor_id=doc_id, appoint_date=app_date, status=True)
        db.session.add(appoint)

        db.session.commit()

        message = "Đặt lịch thành công!"

    return render_template('appoint_booking.html', doctors=doc, message=message)


@app.route('/admin/login', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = data.auth_user(username=username, password=password)
    if user.user_role == UserRoleEnum.ADMIN:
        login_user(user)
    else:
        return redirect('/clinic')
    return redirect('/admin')


@app.route('/clinic/login', methods=['get', 'post'])
def staff_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = data.auth_user(username=username, password=password)

        if user.user_role != UserRoleEnum.ADMIN:
            login_user(user)
            return redirect('/clinic')

    return render_template('/clinic/login.html')


@app.route('/clinic')
def clinic_index():
    if current_user.is_authenticated:
        return render_template('/clinic/index.html')
    return redirect('/clinic/login')


@app.route('/clinic/appointments')
def appointments():
    kw = request.args.get('kw')
    appoint_list = data.get_appointments_by_doc_id(current_user.doctor.id, kw)

    return render_template('/clinic/appointments.html', appoint_list=appoint_list)


@app.route('/clinic/patients')
def patients():
    kw = request.args.get('kw')
    patients = data.get_patient_by_doc_id(current_user.doctor.id, kw)
    return render_template('/clinic/patients.html', patients=patients)


@app.route('/clinic/checkup', methods=['get', 'post'])
def checkup():
    today = date.today()
    kw = ''

    patients = data.get_patient_by_doc_id(current_user.doctor.id, kw)
    meds = data.get_med()

    if request.method.__eq__('POST'):
        pat_name = request.form.get('pat_name')

        pat = data.get_pat_by_name(pat_name=pat_name)

        if pat is not None:
            pat_id = pat.id

        r = Receipt(patient_id=pat_id)

        rd = ReceiptDetail(receipt=r)

        db.session.add(r)
        db.session.add(rd)

        db.session.commit()

    return render_template('/clinic/checkup.html', today=today, patients=patients, medicine=meds)


@app.route('/clinic/receipt')
def receipt():
    r = data.get_receipt()
    return render_template('/clinic/receipt.html', receipt=r)


@app.route('/clinic/logout')
def logout():
    logout_user()
    return redirect('/clinic/login')


@login.user_loader
def load_user(user_id):
    return data.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
