import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.color_variant import ColorVariant
from app.extensions import db


color_variant = Blueprint('color_variant', __name__)
color_variant_config = Blueprint('color_variant_config', __name__)

""""
    APIs for color_variant
"""
@color_variant.route('/', methods=['POST'])
@jwt_required()
def add_color_variant():
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
        hex_code = payload.get('hex_code')
        is_blocked = payload.get('is_blocked')
        if not name:
            raise ValueError('Inappropirate data')
        
        if ColorVariant.query.filter_by(hex_code=hex_code).first():
            raise ValueError('Color already exists')

        variant = ColorVariant(
            name=name,
            hex_code=hex_code,
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


@color_variant.route('/<id>', methods=['GET'])
def get_color_variant(id):
    try:
        data = {}
        variant = ColorVariant.query.filter(db.and_(ColorVariant.id==id, ColorVariant.is_blocked==False)).first()
        if variant:
            data = {
                'id': variant.id,
                'name': variant.name,
                'hex_code': variant.hex_code,
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

@color_variant.route('/', methods=['GET'])
def get_all_color_variant():
    try:
        data = []
        color_variants = ColorVariant.query.filter_by(is_blocked=False).all()
        for variant in color_variants:
            if variant:
                data.append({
                    'id': variant.id,
                    'name': variant.name,
                    'hex_code': variant.hex_code,
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
