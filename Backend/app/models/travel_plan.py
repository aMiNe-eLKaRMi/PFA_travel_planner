from datetime import datetime
from bson import ObjectId
from app import mongo

class TravelPlan:
    @staticmethod
    def create(user_id, city, budget, hotels):
        return mongo.db.plans.insert_one({
            "user_id": ObjectId(user_id),
            "city": city,
            "budget": budget,
            "hotels": hotels,
            "selected_hotel": None,
            "days": None,
            "itinerary": None,
            "created_at": datetime.utcnow()
        })

    @staticmethod
    def find_by_id(plan_id):
        return mongo.db.plans.find_one({"_id": ObjectId(plan_id)})

    @staticmethod
    def update(plan_id, update_data):
        return mongo.db.plans.update_one(
            {"_id": ObjectId(plan_id)},
            {"$set": update_data}
        )