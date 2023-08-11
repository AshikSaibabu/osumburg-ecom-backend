import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.type import Type
from app.extensions import db


type = Blueprint('type', __name__)
type_config = Blueprint('type_config', __name__)

""""
    APIs for type
"""
@type.route('/', methods=['POST'])
@jwt_required()
def add_type():
    current_user = get_jwt_identity()
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            payload = request.json
        else:
            return make_response({
                'status': 'BAD REQUEST',
                'message': 'Content-Type is not supported.'
            })

        name = payload.get('name')
        description = payload.get('description')
        img_url = payload.get('img_url')
        is_blocked = payload.get('is_blocked')
        if not name or not img_url:
            raise ValueError('Inappropirate data')
        
        if Type.query.filter_by(name=name).first():
            raise ValueError('Type already exists')

        variant = Type(
            name=name,
            description=description,
            img_url=img_url,
            is_blocked=is_blocked,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            created_by=current_user,
            updated_by=current_user
        )
        db.session.add(variant)
        db.session.commit()

        return make_response({
            'status': 'OK',
            'message': 'Success',
        }, 200)
    
    except ValueError as e:
        return make_response({
            'error': e.__str__()
        }, 400)

    except Exception as e:
        return make_response({
            'error': e.__doc__
        }, 500)


@type.route('/<id>', methods=['GET'])
def get_type(id):
    try:
        data = {}
        variant = Type.query.filter(db.and_(Type.id==id, Type.is_blocked==False)).first()
        if variant:
            data = {
                'id': variant.id,
                'name': variant.name,
                'description': variant.description,
                'img_url': variant.img_url,
            }
        
        return make_response({
            'status': 'OK',
            'message': 'Success',
            'data': data
        }, 200)
    
    except ValueError as e:
        return make_response({
            'error': e.__str__()
        }, 400)

    except Exception as e:
        return make_response({
            'error': e.__doc__
        }, 500)

@type.route('/', methods=['GET'])
def get_all_type():
    try:
        data = []
        variants = Type.query.filter_by(is_blocked=False).all()
        for variant in variants:
            if variant:
                data.append({
                    'id': variant.id,
                    'name': variant.name,
                    'description': variant.description,
                    'img_url': variant.img_url,
                })
        
        return make_response({
            'status': 'OK',
            'message': 'Success',
            'data': data
        }, 200)
    
    except ValueError as e:
        return make_response({
            'error': e.__str__()
        }, 400)

    except Exception as e:
        return make_response({
            'error': e.__doc__
        }, 500)
