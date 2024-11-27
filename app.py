from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default="Pending")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Invalid input!'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        return jsonify({'message': 'User already exists or other error occurred!', 'error': str(e)}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Invalid input!'}), 400

    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials!'}), 401

    token = jwt.encode(
        {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
        app.config['SECRET_KEY'],
        algorithm="HS256"
    )
    
    return jsonify({'token': token, 'user_id': user.id})

@app.route('/payment', methods=['POST'])
@token_required
def make_payment(current_user):
    data = request.get_json()

    if not data or not data.get('amount') or not data.get('currency'):
        return jsonify({'message': 'Invalid input!'}), 400

    new_payment = Payment(
        amount=data['amount'],
        currency=data['currency'],
        status="Pending",
        user_id=current_user.id
    )

    db.session.add(new_payment)
    db.session.commit()

    return jsonify({'message': 'Payment initiated successfully!', 'payment_id': new_payment.id}), 201

@app.route('/payment/<int:payment_id>', methods=['GET'])
@token_required
def get_payment_status(current_user, payment_id):
    payment = Payment.query.filter_by(id=payment_id, user_id=current_user.id).first()

    if not payment:
        return jsonify({'message': 'Payment not found!'}), 404

    return jsonify({
        'payment_id': payment.id,
        'amount': payment.amount,
        'currency': payment.currency,
        'status': payment.status,
        'created_at': payment.created_at,
        'updated_at': payment.updated_at
    })

@app.route('/payments', methods=['GET'])
@token_required
def get_all_payments(current_user):
    payments = Payment.query.filter_by(user_id=current_user.id).all()

    result = [
        {
            'payment_id': payment.id,
            'amount': payment.amount,
            'currency': payment.currency,
            'status': payment.status,
            'created_at': payment.created_at,
            'updated_at': payment.updated_at
        } for payment in payments
    ]

    return jsonify(result)

@app.route('/payment/<int:payment_id>', methods=['PUT'])
@token_required
def update_payment_status(current_user, payment_id):
    data = request.get_json()
    payment = Payment.query.filter_by(id=payment_id, user_id=current_user.id).first()

    if not payment:
        return jsonify({'message': 'Payment not found!'}), 404

    if not data or not data.get('status'):
        return jsonify({'message': 'Invalid input!'}), 400

    payment.status = data['status']
    db.session.commit()

    return jsonify({'message': 'Payment status updated successfully!', 'payment': {
        'payment_id': payment.id,
        'amount': payment.amount,
        'currency': payment.currency,
        'status': payment.status,
        'created_at': payment.created_at,
        'updated_at': payment.updated_at
    }})

@app.route('/credits', methods=['GET'])
def credits():
    return jsonify({
        'author': 'Amrit Acharya',
        'github': 'https://github.com/amritacharya022',
        'message': 'Made with ❤️ by Amrit Acharya. Secure Payment API for developers.'
    })

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
