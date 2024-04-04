from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, jsonify, send_file
from models.payment import Payment
from payments.pix import Pix
from repository.database import db


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
    return jsonify({"message": "The payment has been confirmed"})


@payment_bp.get('/payments/pix/<int:payment_id>')
def payment_pix_page(payment_id):
    payment = Payment.query.get(payment_id)

    return render_template('payment.html',
                           payment_id=payment.id,
                           value=payment.value,
                           host="http://127.0.0.1:5000",
                           qrcode=payment.qr_code
                           )
