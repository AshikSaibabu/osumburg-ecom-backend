import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.product_color_variant import ProductColorVariant
from app.models.products import Product
from app.models.color_variant import ColorVariant
from app.extensions import db


product_color_variants = Blueprint('product_color_variants', __name__)
product_color_variants_config = Blueprint('product_color_variants_config', __name__)

""""
    APIs for product_color_variants
"""
@product_color_variants.route('/', methods=['POST'])
@jwt_required()
def add_product_color_variants():
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
        color_variant = ColorVariant.query.filter_by(id=color_variant_id).first()
        if not color_variant:
            raise ValueError('Color variant not found')
        
        product_id = payload.get('product_id')
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            raise ValueError('Product not found')
        
        is_blocked = payload.get('is_blocked')

        if ProductColorVariant.query.filter(db.and_(ProductColorVariant.color_variant==color_variant.id, ProductColorVariant.product==product.id)).first():
            raise ValueError('Product color variant already exists')
        
        variant = ProductColorVariant(
            color_variant=color_variant.id,
            product=product.id,
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
        import traceback
        print(traceback.print_exc())
        return make_response({
            'error': e.__doc__
        }, 500)


@product_color_variants.route('/<id>', methods=['GET'])
def get_product_color_variants(id):
    try:
        data = {}
        variant = ProductColorVariant.query.filter(db.and_(ProductColorVariant.id==id, ProductColorVariant.is_blocked==False)).first()
        if variant:
            data = {
                'id': variant.id,
                'color_variant': variant.color_variant,
                'product': variant.product
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

@product_color_variants.route('/', methods=['GET'])
def get_all_product_color_variants():
    try:
        data = []
        variants = ProductColorVariant.query.filter_by(is_blocked=False).all()
        for variant in variants:
            if variant:
                data.append({
                    'id': variant.id,
                    'color_variant': variant.color_variant,
                    'product': variant.product
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
