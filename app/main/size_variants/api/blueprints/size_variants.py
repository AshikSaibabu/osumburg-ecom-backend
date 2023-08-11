import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.size_varaint import SizeVariant
from app.extensions import db


size_variants = Blueprint('size_variants', __name__)
size_variants_config = Blueprint('size_variants_config', __name__)

""""
    APIs for size_variants
"""
@size_variants.route('/', methods=['POST'])
@jwt_required()
def add_size_variants():
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
        code = payload.get('code')
        is_blocked = payload.get('is_blocked')
        if not name or not code:
            raise ValueError('Inappropirate data')
        
        if SizeVariant.query.filter_by(code=code).first():
            raise ValueError('Size variant already exists')

        variant = SizeVariant(
            name=name,
            code=code,
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


@size_variants.route('/<id>', methods=['GET'])
def get_size_variants(id):
    try:
        data = {}
        variant = SizeVariant.query.filter(db.and_(SizeVariant.id==id, SizeVariant.is_blocked==False)).first()
        if variant:
            data = {
                'id': variant.id,
                'name': variant.name,
                'code': variant.code,
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

@size_variants.route('/', methods=['GET'])
def get_all_size_variants():
    try:
        data = []
        variants = SizeVariant.query.filter_by(is_blocked=False).all()
        for variant in variants:
            if variant:
                data.append({
                    'id': variant.id,
                    'name': variant.name,
                    'code': variant.code,
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
