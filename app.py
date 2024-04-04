from flask import Flask, request, jsonify


app = Flask(__name__)

app.register_blueprint(payment_bp)


if __name__ == '__main__':
    app.run(debug=True)