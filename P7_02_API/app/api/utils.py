import os
from functools import wraps
from flask import current_app, request, abort
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException


##############################
#    ##### SECURITY #####    #

# for swagger documentation
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}


# decorator to secure the endpoints
def apikey_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if 'X-API-KEY' in request.headers:
            if request.headers.get('X-API-KEY') == current_app.config['API_KEY']:
                return f(*args, **kwargs)
            else:
                abort(401, 'Token is invalid')
        else:
            abort(401, 'A valid API key is missing')
    return decorator


#################################
#    ##### FILE UPLOAD #####    #

def check_local_upload_dir():
    """Create an upload directory on the server filesystem if it not exist"""
    if not os.path.isdir(current_app.config['UPLOAD_DIR']):
        os.mkdir(current_app.config['UPLOAD_DIR'])


def file_upload(file, save=True):
    """Verify and save or return an uploaded file
    args:
        file: file - the received file
        save: bool, default=True - If true save the file in the filesystem, else return the file
    """
    if not file:
        # if user does not select file, browser also submit an empty part without filename
        raise HTTPException.BadRequest('No file selected')
    if file.mimetype.split('/', 1)[1] in current_app.config['ALLOWED_EXT']:
        filename = secure_filename(file.filename)
        if save:
            filepath = os.path.join(current_app.config['UPLOAD_DIR'], filename)
            check_local_upload_dir()
            file.save(filepath)
            return filename
        else:
            return file
    else:
        raise HTTPException.BadRequest('This file extension is not allowed')
