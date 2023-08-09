import json
import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, jwt_required
from app.models.users import User
from app.extensions import db


auth = Blueprint('auth', __name__)
auth_config = Blueprint('auth_config', __name__)

""""
    APIs for authenticaton
"""

@auth.route('/register', methods=['POST'])
def register_new():
    if request.method == 'POST':
        try:
            content_type = request.headers.get('Content-Type')
            if (content_type == 'application/json'):
                payload = request.json
            else:
                return make_response({
                    'status': 'BAD REQUEST',
                    'message': 'Content-Type is not supported.'
                })

            first_name = payload.get('first_name')
            last_name = payload.get('last_name')
            email = payload.get('email')
            phone = payload.get('phone')
            password = payload.get('password')

            existing_phone = User.query.filter_by(phone=phone).count()
            existing_email = User.query.filter_by(email=email).count()
            if existing_phone:
                return make_response({
                    'error': 'Phone number already in use'
                }, 400)
            
            if existing_email:
                return make_response({
                    'error': 'Email already in use'
                }, 400)
            
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()

            return make_response({
                    'status': 'OK',
                    'message': 'Success',
                    'data': {
                        "uid": user.id
                    }
                }, 200)
            
        except ValueError as e:
            return make_response({
                'error': e.__doc__
            }, 400)

        except Exception as e:
            return make_response({
                'error': e.__doc__
            }, 500)


@auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            content_type = request.headers.get('Content-Type')
            if (content_type == 'application/json'):
                payload = request.json
            else:
                return make_response({
                    'status': 'BAD REQUEST',
                    'message': 'Content-Type is not supported.'
                })

            username = payload.get('username')
            password = payload.get('password')
            if not username or not password:
                raise ValueError('Inappropirate data')

            user = User.query.filter(db.or_(User.phone==username, User.email==username)).first()

            if not user:
                raise ValueError('User does not exists')
            if not user.check_password(password):
                raise ValueError('Credentials are wrong')

            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return make_response({
                'status': 'OK',
                'message': 'Success',
                'data': {
                    "access": access_token,
                    "refresh": refresh_token
                }
            }, 200)
        
        except ValueError as e:
            return make_response({
                'error': e.__str__()
            }, 400)

        except Exception as e:
            return make_response({
                'error': e.__doc__
            }, 500)


@auth.route('/refresh_token', methods=['GET'])
@jwt_required(refresh=True)
def refresh_expiring_jwts():
    current_user = get_jwt_identity()
    try:
        access_token = create_access_token(identity=current_user)
        return make_response({
            'status': 'OK',
            'message': 'Success',
            'data': {
                'access': access_token
            }
        }, 200)
    except Exception as e:
        import traceback
        print(traceback.print_exc())
        return make_response({
            'error': e.__doc__
        }, 500)

