from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_mail import Mail, Message
from datetime import timedelta
import os
from dotenv import load_dotenv
from flask_cors import CORS  
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-super-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

app.config['MAIL_SERVER'] = 'smtp.ionos.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'support@f1automobile.com'
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'support@f1automobile.com'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

def send_welcome_email(user_email, user_name):
    """Send welcome email to new user using IONOS SMTP"""
    try:
        msg = Message(
            subject="Welcome to F1 Automobile!",
            recipients=[user_email],
            html=f"""
            <h1>Welcome, {user_name}!</h1>
            <p>Thank you for registering with F1 Automobile.</p>
            <p>We're excited to have you on board!</p>
            <p>If you have any questions, please contact us at support@f1automobile.com</p>
            <p><strong>F1 Automobile Team</strong></p>
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")
        return False
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'All fields are required'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    
    email_sent = send_welcome_email(email, name)
    
    response = {
        'message': 'User registered successfully',
        'email_sent': email_sent
    }
    return jsonify(response), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email
    })

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    users_list = [{
        'id': user.id,
        'name': user.name,
        'email': user.email
    } for user in users]

    return jsonify(users_list), 200

@app.route('/delete', methods=['POST'])
def delete_all_users():
    try:
        num_deleted = db.session.query(User).delete()
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": f"Deleted all {num_deleted} users"
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)