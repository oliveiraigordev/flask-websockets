from flask import Flask, request, jsonify
from repository.database import db
from routes.payments import payment_bp
from models.payment import Payment


app = Flask(__name__)
app.config.from_pyfile('settings.py')
app.register_blueprint(payment_bp)

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)