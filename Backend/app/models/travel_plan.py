# app/models/travel_plan.py
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
            "hotels": [{
                "name": h["name"],
                "address": h["address"],
                "website": h.get("website", "")
            } for h in hotels],
            "selected_hotel": None,
            "days": None,
            "itinerary": None,
            "created_at": datetime.utcnow()
        })

    # Les autres méthodes restent inchangées
    @staticmethod
    def find_by_id(plan_id):
        return mongo.db.plans.find_one({"_id": ObjectId(plan_id)})

    @staticmethod
    def update(plan_id, update_data):
        return mongo.db.plans.update_one(
            {"_id": ObjectId(plan_id)},
            {"$set": update_data}
        )
    
    @staticmethod
    def delete(plan_id):
        return mongo.db.plans.delete_one({"_id": ObjectId(plan_id)})

    @staticmethod
    def find_by_user_id(user_id):
        return list(mongo.db.plans.find({"user_id": ObjectId(user_id)}))