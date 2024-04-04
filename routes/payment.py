from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from models.payment import Payment
from repository.database import db


payment_bp = Blueprint('payment', __name__)


@payment_bp.post('/payments/pix')
def create_payment_pix():
    data = request.get_json()

    if 'value' not in data:
        return jsonify({"message": "Invalid value"}), 400

    expiration_date = datetime.now() + timedelta(minutes=30)
    new_payment = Payment(value=data['value'], expiration_date=expiration_date)
    
    db.session.add(new_payment)
    db.session.commit()
    
    return jsonify({"message": "The payment has been created",
                    "payment": new_payment.to_dict()}), 201


@payment_bp.post('/payments/pix/confirmation')
def pix_confirmation():
    return jsonify({"message": "The payment has been confirmed"})


@payment_bp.get('/payments/pix/<int:payment_id>')
def payment_pix_page(payment_id):
    return 'pagamento pix'
