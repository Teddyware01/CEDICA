from flask import current_app

def avatar_url(avatar):
    client = current_app.storage.client
    config = current_app.config
    if avatar is None:
        return default_avatar_url(config)
    
    return client.presigned_get_object("grupo15", avatar) # Esto sirve para archivos sensibles como documento de jya.

def default_avatar_url(config):
    protocol = "https" if config.get("MINIO_SECURE") else "http"
    return f"{protocol}://{config.get('MINIO_SERVER')}/grupo15/public/default.png"