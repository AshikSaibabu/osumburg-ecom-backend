import json
import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, jwt_required
from app.models.users import User
from app.models.design import Design
from app.models.design_images import DesignAssets
from app.utils.upload_images import upload_image
from app.extensions import db


assets = Blueprint('assets', __name__)
assets_config = Blueprint('assets_config', __name__)

""""
    APIs for assets
"""
@assets.route('/upload', methods=['POST'])
@jwt_required()
def add_assets():
    try:
        content_type = request.headers.get('Content-Type')
        if (content_type.startswith('multipart/form-data')):
            payload = request.files
        else:
            return make_response({
                'status': 'BAD REQUEST',
                'message': 'Content-Type is not supported.'
            })
        
        file = payload.get('file')
        if file:
            url = upload_image(file)
            return make_response({
                'status': 'OK',
                'message': 'Success',
                'data': {
                    'url': url
                }
            }, 200)
        else:
            raise ValueError('File not found')
    
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
