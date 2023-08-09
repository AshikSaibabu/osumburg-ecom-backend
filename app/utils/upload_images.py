import os
import uuid
from werkzeug.utils import secure_filename


def upload_image(file):
    path = os.environ.get('DESIGN_ASSETS_PATH')
    if not os.path.exists(path):
        os.mkdir(path)

    filename = secure_filename(file.filename)
    filename = f"{uuid.uuid4()}_.{filename.split('.')[-1]}"
    file.save(os.path.join(path, filename))
    return os.path.join(path, filename)[4:]