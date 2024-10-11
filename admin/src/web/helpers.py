from flask import current_app

def avatar_url(avatar):
    client = current_app.storage.client
    
    if avatar is None:
        return ""
    
    return client.presigned_get_object("grupo15", avatar)