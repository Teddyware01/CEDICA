from flask import Blueprint, request, jsonify
from src.core import board
from src.web.schemas.issue import issues_schema, create_issue_schema, issue_schema


bp = Blueprint("issues_api", __name__, url_prefix="/api/consultas")


@bp.get("/")
def index():
    issues = board.list_issues()
    data = issues_schema.dump(issues)
    
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
    print("TODOS:")
    print(jsonify(data))

    print(jsonify(data))
    return jsonify(data), 200


@bp.post("/")
def create():
    attrs = request.get_json() #obtengo los parametros
    #new_issue = create_issue_schema.load(data)
    errors = create_issue_schema.validate(attrs)
        
    if errors:
        return jsonify(errors), 400
    else:
        kwars = create_issue_schema.load(attrs)
        new_issue = board.create_issue(**kwars)
        data = issue_schema.dump(new_issue)
        return jsonify(data), 201 