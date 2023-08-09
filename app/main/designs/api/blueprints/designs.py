import json
import datetime
from flask import Blueprint, make_response, request
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token, jwt_required
from app.models.users import User
from app.models.design import Design
from app.models.design_images import DesignAssets
from app.extensions import db


designs = Blueprint('designs', __name__)
designs_config = Blueprint('designs_config', __name__)

""""
    APIs for designs
"""
@designs.route('/', methods=['POST'])
@jwt_required()
def add_designs():
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
        asset_urls = payload.get('asset_urls')
        if not name or not asset_urls:
            raise ValueError('Inappropirate data')

        design = Design(
            name=name,
            description=description,
            is_blocked=is_blocked,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            created_by=current_user,
            updated_by=current_user
        )
        db.session.add(design)
        db.session.commit()

        for url in asset_urls:
            design_asset = DesignAssets(
                design_id = design.id,
                url = url,
                updated_by = current_user,
                created_by = current_user
            )
            db.session.add(design_asset)

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


@designs.route('/<id>', methods=['GET'])
def get_designs(id):
    try:
        data = {}
        design = Design.query.filter(db.and_(Design.id==id, Design.is_blocked==False)).first()
        if design:
            design_assets = DesignAssets.query.filter_by(design_id=design.id).all()
            data = {
                'name': design.name,
                'description': design.description,
                'assets': [asset.url for asset in design_assets]
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

@designs.route('/', methods=['GET'])
def get_all_designs():
    try:
        data = []
        designs = Design.query.filter_by(is_blocked=False).all()
        for design in designs:
            if design:
                design_assets = DesignAssets.query.filter_by(design_id=design.id).all()
                data.append({
                    'name': design.name,
                    'description': design.description,
                    'assets': [asset.url for asset in design_assets]
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
