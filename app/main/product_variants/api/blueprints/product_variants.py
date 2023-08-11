import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.product_variant import ProductVariants
from app.models.product_color_variant import ProductColorVariant
from app.models.size_varaint import SizeVariant
from app.models.sleeve_length_variant import SleeveLengthVariant
from app.extensions import db


product_variant = Blueprint('product_variant', __name__)
product_variant_config = Blueprint('product_variant_config', __name__)

""""
    APIs for product_variant
"""
@product_variant.route('/', methods=['POST'])
@jwt_required()
def add_product_variant():
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

        color_variant_id = payload.get('color_variant_id')
        print('>>>>', color_variant_id, type(color_variant_id))
        color_variant = ProductColorVariant.query.filter_by(id=color_variant_id).first()
        if not color_variant:
            raise ValueError('Product color varaint is not found')
        
        size_variant_id = payload.get('size_variant_id')
        size_variant = SizeVariant.query.filter_by(id=size_variant_id).first()
        if not size_variant:
            raise ValueError('Product size varaint is not found')
        
        sleeve_variant_id = payload.get('sleeve_variant_id')
        sleeve_variant = SleeveLengthVariant.query.filter_by(id=sleeve_variant_id).first()
        if not sleeve_variant:
            raise ValueError('Product sleeve length varaint is not found')
        
        is_blocked = payload.get('is_blocked')

        product_variant = ProductVariants.query.filter(db.and_(ProductVariants.color_variant==color_variant.id, ProductVariants.size_variant==size_variant.id, ProductVariants.sleeve_variant==sleeve_variant.id)).first()
        if product_variant:
            raise ValueError('Product variant already exists')
        
        variant = ProductVariants(
            color_variant=color_variant.id,
            size_variant=size_variant.id,
            sleeve_variant=sleeve_variant.id,
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


@product_variant.route('/<id>', methods=['GET'])
def get_product_variant(id):
    try:
        data = {
            'product_id': id,
            'variants': []
        }
        color_variants = ProductColorVariant.query.filter(db.and_(ProductColorVariant.product==id, ProductColorVariant.is_blocked==False)).all()

        if color_variants:
            for color_variant in color_variants:
                product_variants = ProductVariants.query.filter(db.and_(ProductVariants.color_variant==color_variant.id, ProductVariants.is_blocked==False)).all()
                for variant in product_variants:
                    data['variants'].append({
                        'color_variant_id': variant.color_variant,
                        'size_variant_id': variant.size_variant,
                        'sleeve_variant_id': variant.sleeve_variant
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
