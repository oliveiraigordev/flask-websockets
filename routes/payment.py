from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, send_file
from models.payment import Payment
from payments.pix import Pix
from repository.database import db
from repository.socketio import socketio


payment_bp = Blueprint('payment', __name__)


@payment_bp.post('/payments/pix')
def create_payment_pix():
    data = request.get_json()

    if 'value' not in data:
        return jsonify({"message": "Invalid value"}), 400

    expiration_date = datetime.now() + timedelta(minutes=30)
    new_payment = Payment(value=data['value'], expiration_date=expiration_date)
    
    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()

    new_payment.bank_payment_id = data_payment_pix['bank_payment_id']
    new_payment.qr_code = data_payment_pix['qr_code_path']

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({"message": "The payment has been created",
                    "payment": new_payment.to_dict()}), 201


@payment_bp.get('/payments/pix/qr_code/<file_name>')
def get_image(file_name):
    return send_file(f'static/qrcode_img/{file_name}.png', mimetype='image/png')


@payment_bp.post('/payments/pix/confirmation')
def pix_confirmation():
    data = request.get_json()
    value = data.get('value')
    bank_payment_id = data.get('bank_payment_id')

    if not value or not bank_payment_id:
        return jsonify({"message": "Invalid payment data"}), 400    

    payment = Payment.query.filter_by(bank_payment_id=bank_payment_id).first()

    if not payment or payment.paid:
        return jsonify({"message": "The payment not found"}), 404

    if value != payment.value:
        return jsonify({"message": "The payment not found"}), 400

    payment.paid = True
    db.session.commit()
    socketio.emit(f'payment-confirmed-{payment.id}')

    return jsonify({"message": "The payment has been confirmed"})


@payment_bp.get('/payments/pix/<int:payment_id>')
def payment_pix_page(payment_id):
    payment = Payment.query.get(payment_id)

    if not payment:
        return render_template('404.html')
    
    payment_kw = {
        'payment_id': payment.id,
        'value': payment.value,
        'host': "http://127.0.0.1:5000",
        'qrcode': payment.qr_code
        }

    if payment.paid:
        return render_template('confirmed_payment.html', **payment_kw)
    return render_template('payment.html', **payment_kw)


@socketio.on('connect')
def handle_connect():
    pass


@socketio.on('disconnect')
def handle_disconnect():
    pass
