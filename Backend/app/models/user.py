from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from app import mongo

class User:
    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def create(email, password):
        hashed_pw = generate_password_hash(password)
        return mongo.db.users.insert_one({
            "email": email,
            "password": hashed_pw
        })