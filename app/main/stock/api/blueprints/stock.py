import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.product_variant import ProductVariants
from app.models.stock import Stock
from app.extensions import db


stock = Blueprint('stock', __name__)
stock_config = Blueprint('stock_config', __name__)

""""
    APIs for stock
"""
@stock.route('/', methods=['POST'])
@jwt_required()
def add_stock():
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

        product_variant_id = payload.get('product_variant_id')
        qty = payload.get('qty')
        is_pod = payload.get('is_pod')
        is_blocked = payload.get('is_blocked')
        product_variant = ProductVariants.query.filter_by(id=product_variant_id).first()
        if not product_variant:
            raise ValueError('Product varaint is not found')

        variant = Stock(
            product_variant=product_variant.id,
            qty=qty,
            is_pod=is_pod,
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


@stock.route('/<id>', methods=['GET'])
def get_stock(id):
    try:
        data = {}
        stock = Stock.query.filter(db.and_(Stock.product_variant==id, Stock.is_blocked==False)).first()
        if stock:
            data = {
                'product_variant_id': stock.product_variant_id,
                'qty': stock.qty,
                'is_pod': stock.is_pod
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

@stock.route('/', methods=['GET'])
def get_all_stock():
    try:
        data = []
        color_variants = Stock.query.filter_by(is_blocked=False).all()
        for variant in color_variants:
            if variant:
                data.append({
                    'product_variant_id': stock.product_variant_id,
                    'qty': stock.qty,
                    'is_pod': stock.is_pod
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
