import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.product_color_variant import ProductColorVariant
from app.models.product_color_variant_images import ProductColorVariantImages
from app.extensions import db


product_color_variant_images = Blueprint('product_color_variant_images', __name__)
product_color_variant_images_config = Blueprint('product_color_variant_images_config', __name__)

""""
    APIs for product_color_variant_images
"""
@product_color_variant_images.route('/', methods=['POST'])
@jwt_required()
def add_product_color_variant_images():
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

        product_color_variant_id = payload.get('product_color_variant_id')
        product_color_variant = ProductColorVariant.query.filter_by(id=product_color_variant_id).first()
        if not product_color_variant:
            raise ValueError('Product color variant not found')

        asset_urls = payload.get('asset_urls')
        is_blocked = payload.get('is_blocked')

        for url in asset_urls:
            variant = ProductColorVariantImages(
                color_variant=product_color_variant.id,
                url=url,
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


@product_color_variant_images.route('/<id>', methods=['GET'])
def get_product_color_variant_images(id):
    try:
        data = {'assets': []}
        assets = ProductColorVariantImages.query.filter(db.and_(ProductColorVariantImages.color_variant==id, ProductColorVariantImages.is_blocked==False)).all()
        for asset in assets:
            data['product_color_variant_id'] = asset.color_variant
            data['assets'].append(asset.url)
        
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
