import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.category import Category
from app.extensions import db


categories = Blueprint('categories', __name__)
categories_config = Blueprint('categories_config', __name__)

""""
    APIs for decategoriessigns
"""
@categories.route('/', methods=['POST'])
@jwt_required()
def add_categories():
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
        is_blocked = payload.get('is_blocked')
        img_url = payload.get('img_url')
        if not name:
            raise ValueError('Inappropirate data')
        
        if Category.query.filter_by(name=name).first():
            raise ValueError('Category already exists')

        design = Category(
            name=name,
            description=description,
            img_url=img_url,
            is_blocked=is_blocked,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            created_by=current_user,
            updated_by=current_user
        )
        db.session.add(design)
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


@categories.route('/<id>', methods=['GET'])
def get_categories(id):
    try:
        data = {}
        category = Category.query.filter(db.and_(Category.id==id, Category.is_blocked==False)).first()
        if category:
            data = {
                'id': category.id,
                'name': category.name,
                'description': category.description,
                'img_url': category.img_url
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

@categories.route('/', methods=['GET'])
def get_all_categories():
    try:
        data = []
        categories = Category.query.filter_by(is_blocked=False).all()
        for category in categories:
            if category:
                data.append({
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    'img_url': category.img_url
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
