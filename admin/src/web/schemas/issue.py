from marshmallow import Schema, fields


class IssueSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    status = fields.Str()
    user_id = fields.Int(required=True)
    inserted_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
# Hacer este mapeo sirve para reducir campos y poder tener otras validaciones. 
class SimpleIssueSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    title = fields.Str(required=True)
    

class CreateIssueSchema(Schema):
    email = fields.Email(required=True)
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    user_id = fields.Int(required=True)
        
    
issue_schema = IssueSchema()
issues_schema = IssueSchema(many=True)
create_issue_schema = CreateIssueSchema()