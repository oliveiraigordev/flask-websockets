from flask import Blueprint


payment_bp = Blueprint('payment', __name__)


@payment_bp.post('/payments/pix')
def create_payment_pix():
    return jsonify({"message": "The payment has been created"})


@payment_bp.get('/payments/pix/<int:payment_id>')
def paument_pix_page(payment_id):
    return 'pagamento pix'