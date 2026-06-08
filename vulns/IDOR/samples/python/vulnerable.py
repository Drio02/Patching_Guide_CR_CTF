# Versión vulnrable en una aplicacion Flask

from flask import Flask, jsonify, session
from models import User

app = Flask(__name__)

@app.route('api/user/<int:user_id>', methods=['GET'])
def getUserProfile(user_id):
    # IDOR: se confia en el ID que viene en la URL sin verificar
    # si el usuario tiene permitido verese recurso
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error' : 'user not found'}), 404
    
    return jsonify({
        'id': user.id,
        'email': user.email,
        'address': user.address
    })


# No existe verificacion entre la identidad del solicitante y el recurso solicitado