from src.core.ecuestre.sedes import Sedes
from src.core.database import db

def create_sede(**kwargs):
    sede = Sedes(**kwargs)
    db.session.add(sede)
    db.session.commit()

    return sede