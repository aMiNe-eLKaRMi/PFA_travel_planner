from flask_jwt_extended import current_user
from bson import ObjectId
from app.models.user import User

def configure_jwt(jwt):
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = ObjectId(jwt_data["sub"])
        return User.find_by_id(identity)