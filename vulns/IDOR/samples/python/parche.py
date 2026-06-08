from flask import Flask, jsonify, session, abort
from functools import wraps
from models import User

app = Flask(__name__)

def loginRequired(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            abort(401)
        return f(*args, **kwargs)
    return wrapper

# Version A
@app.route('/api/user/<int:user_id>', methods=['GET'])
@loginRequired
def getUserProfile(user_id):
    current_user_id = session['user_id']

    # Se verifica que el usuario sea el unico que pueda ver su informacion
    # o el administrador del sistema
    current_user = User.query.get(current_user_id)
    if current_user_id != user_id and not current_user.is_admin:
        abort(403)  # Forbidden

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'id': user.id,
        'email': user.email,
        'address': user.address
    })

# Version B

@app.route('/api/me', methods=['GET'])
@logiRequired
def getMyProfile():
    # El ID se obtiene directamente de la sesion, entonces no hay posible IDOR
    user = User.query.get(session['user_id'])
    return jsonify({
        'id': user.id,
        'email': user.email,
        'phone': user.phone,
        'address': user.address
    })