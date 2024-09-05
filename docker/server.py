from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask_cors import CORS
#import logging # Maha : Use only for debugging

app = Flask(__name__)
# To DO : Maha - Read all these variables from enviornment 
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['PORT'] = 5000 # Adding default port as 5000 can be changed via environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['DEFAULT_ADMIN_USERNAME'] = 'admin'
app.config['DEFAULT_ADMIN_PASSWORD'] = 'password'
db = SQLAlchemy(app)

# Maha : Use only for debugging
#app.logger.setLevel(logging.ERROR)

# Initialize CORS
CORS(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(200))

# Create default admin user
@app.before_first_request
def create_admin():
    if not User.query.filter_by(username=app.config['DEFAULT_ADMIN_USERNAME']).first():
        hashed_password = generate_password_hash(app.config['DEFAULT_ADMIN_PASSWORD'], method='pbkdf2:sha256')
        admin_user = User(username=app.config['DEFAULT_ADMIN_USERNAME'], password=hashed_password, role='admin')
        db.session.add(admin_user)
        db.session.commit()

# Serve index.html for testing functionality from web page
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# JWT token generation 
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = jwt.encode({
            'user_id': user.id,
            'role': user.role,  
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

# Usage        : User creation with password hashed and stored in DB
# Allowed Role : Admin 
# Method       : POST
@app.route('/user', methods=['POST'])
def create_user():
    token = request.headers.get('x-access-token')
    error_message, status_code = check_role(token, ['admin'])
    if error_message:
        return jsonify({'message': error_message}), status_code

    data = request.get_json()
    # Check if the username already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'User already exists!'}), 400
    
    new_user = User(
        username=data['username'],
        password=generate_password_hash(data['password'], method='pbkdf2:sha256'),
        role=data['role']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created'})

# Usage        : Utility function to get role and token verification
# Param        : token and required_roles as list 
def check_role(token, required_roles):
    if not token:
        return 'Token is missing!', 401

    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"]) 
        user_role = decoded_token.get('role')
        if user_role in required_roles:
            return None,None  # No error
        return 'You are unauthrized to perform this action!', 403
    except Exception as e: 
        print(e)
        return 'Token is invalid!', 401

# ProductService Endpoints
@app.route('/products', methods=['GET'])
def get_products():
    token = request.headers.get('x-access-token')
    error_message, status_code = check_role(token, ['admin', 'privileged'])
    if error_message:
        return jsonify({'message': error_message}), status_code

    products = Product.query.all()
    if products:
        return jsonify([{'id': p.id, 'name': p.name, 'description': p.description} for p in products])
    return jsonify({'message': 'No products found!'}), 404 #Maha: This could be 200 as well in case there is no data in table

# AddProduct
@app.route('/product', methods=['POST'])
def add_product():
    
    token = request.headers.get('x-access-token')
    error_message, status_code = check_role(token, ['admin'])
    if error_message:
        return jsonify({'message': error_message}), status_code

    data = request.get_json()
    if not data.get('name'): # If product name is not provided return error 
        return jsonify({'message': 'Bad request: Product name required'}), 400

    if Product.query.filter_by(name=data['name']).first():
        return jsonify({'message': 'Product name must be unique!'}), 400

    new_product = Product(name=data['name'], description=data.get('description', ''))
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully!'})

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    token = request.headers.get('x-access-token')
    error_message, status_code = check_role(token, ['admin', 'privileged'])
    if error_message:
        return jsonify({'message': error_message}), status_code

    product = Product.query.get(product_id)
    if product:
        return jsonify({'id': product.id, 'name': product.name, 'description': product.description})
    return jsonify({'message': 'Product not found!'}), 404


# Fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    token = request.headers.get('x-access-token')
    error_message, status_code = check_role(token, ['admin'])
    if error_message:
        return jsonify({'message': error_message}), status_code

    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'role': u.role} for u in users])

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=app.config['PORT'])
