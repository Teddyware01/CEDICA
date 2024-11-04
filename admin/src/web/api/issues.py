from flask import Blueprint
from src.core import board
from src.web.schemas.issue import issues_schema

bp = Blueprint("issues_api", __name__, url_prefix="/api/consultas")


@bp.get("/")
def index():
    issues = board.list_issues()
    data = issues_schema.dump(issues)
    print(data)
    
    '''data = []
    for issue in issues:
        data.append(
            {
                "id": issue.id,
                "title": issue.title,
                "description": issue.description,
                "status": issue.status,                
                "inserted_at": issue.inserted_at,
                "updated_at": issue.updated_at,
            }
    )'''
    
    return data, 200
