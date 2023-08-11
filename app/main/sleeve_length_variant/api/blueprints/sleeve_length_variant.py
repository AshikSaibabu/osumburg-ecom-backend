import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.sleeve_length_variant import SleeveLengthVariant
from app.extensions import db


sleeve_length_variants = Blueprint('sleeve_length_variants', __name__)
sleeve_length_variants_config = Blueprint('sleeve_length_variants_config', __name__)

""""
    APIs for sleeve_length_variants
"""
@sleeve_length_variants.route('/', methods=['POST'])
@jwt_required()
def add_sleeve_length_variants():
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
        is_blocked = payload.get('is_blocked')
        if not name:
            raise ValueError('Inappropirate data')
        
        if SleeveLengthVariant.query.filter_by(name=name).first():
            raise ValueError('Size variant already exists')

        variant = SleeveLengthVariant(
            name=name,
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


@sleeve_length_variants.route('/<id>', methods=['GET'])
def get_sleeve_length_variants(id):
    try:
        data = {}
        variant = SleeveLengthVariant.query.filter(db.and_(SleeveLengthVariant.id==id, SleeveLengthVariant.is_blocked==False)).first()
        if variant:
            data = {
                'id': variant.id,
                'name': variant.name,
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

@sleeve_length_variants.route('/', methods=['GET'])
def get_all_sleeve_length_variants():
    try:
        data = []
        variants = SleeveLengthVariant.query.filter_by(is_blocked=False).all()
        for variant in variants:
            if variant:
                data.append({
                    'id': variant.id,
                    'name': variant.name,
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
