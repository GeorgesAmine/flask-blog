import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flaskblog import mailjet
from flaskblog.config import Config

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    
    # Resizing image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    #Returns picture filename
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    data = {
        'Messages': [
            {
               "From":{
                "Email": Config.SENDER_EMAIL,
                "Name": "PasswordService"
               },
               "To":[
                 {
                   "Email": user.email,
                   "Name": user.username
                 }
               ],
               "Subject": "Password reset",
               "TextPart": f'''To reset your password click on the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not request this please ignore this email 
'''
            }
        ]
    }

    mailjet.send.create(data=data)