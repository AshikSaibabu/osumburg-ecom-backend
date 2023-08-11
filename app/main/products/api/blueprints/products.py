import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.products import Product
from app.models.category import Category
from app.models.type import Type
from app.models.design import Design
from app.extensions import db


product = Blueprint('product', __name__)
product_config = Blueprint('product_config', __name__)

""""
    APIs for product
"""
@product.route('/', methods=['POST'])
@jwt_required()
def add_product():
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

        design_id = payload.get('design_id')
        design = Design.query.filter_by(id=design_id).first()
        if not design:
            raise ValueError('Design does not exists')
    
        type_id = payload.get('type_id')
        type = Type.query.filter_by(id=type_id).first()
        if not type:
            raise ValueError('Type does not exists')
        
        category_id = payload.get('category_id')
        category = Type.query.filter_by(id=category_id).first()
        if not category:
            raise ValueError('Category does not exists')

        name = payload.get('name')
        short_description = payload.get('short_description')
        long_description = payload.get('long_description')
        is_blocked = payload.get('is_blocked')

        if not name:
            raise ValueError('Inappropirate data')
        
        if Product.query.filter_by(name=name).first():
            raise ValueError('Product name exists')

        product = Product(
            name=name,
            design_id=design.id,
            short_description=short_description,
            long_description=long_description,
            type=type.id,
            category=category.id,
            is_blocked=is_blocked,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            created_by=current_user,
            updated_by=current_user
        )
        db.session.add(product)
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


@product.route('/<id>', methods=['GET'])
def get_product(id):
    try:
        data = {}
        product = Product.query.filter(db.and_(Product.id==id, Product.is_blocked==False)).first()
        if product:
            data = {
                'id': product.id,
                'name': product.name,
                'design_id': product.design_id,
                'short_description': product.short_description,
                'long_description': product.long_description,
                'type': product.type,
                'category': product.category,
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

@product.route('/', methods=['GET'])
def get_all_product():
    try:
        data = []
        products = Product.query.filter_by(is_blocked=False).all()
        for product in products:
            if product:
                data.append({
                'id': product.id,
                'name': product.name,
                'design_id': product.design_id,
                'short_description': product.short_description,
                'long_description': product.long_description,
                'type': product.type,
                'category': product.category,
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
        import traceback
        print(traceback.print_exc())
        return make_response({
            'error': e.__doc__
        }, 500)
