from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.services.foursquare import get_hotels
from app.services.ai_service import generate_itinerary
from app.models.travel_plan import TravelPlan
from bson import ObjectId

plan_bp = Blueprint('plan', __name__)

@plan_bp.route('/init', methods=['POST'])
@jwt_required()
def init_plan():
    data = request.get_json()
    hotels = get_hotels(data['city'])
    
    plan_id = TravelPlan.create(
        user_id=current_user['_id'],
        city=data['city'],
        budget=data['budget'],
        hotels=hotels
    ).inserted_id
    
    return jsonify({
        "plan_id": str(plan_id),
        "hotels": hotels
    }), 201

@plan_bp.route('/finalize', methods=['POST'])
@jwt_required()
def finalize_plan():
    data = request.get_json()
    plan = TravelPlan.find_by_id(data['plan_id'])
    
    if not plan or plan['user_id'] != current_user['_id']:
        return jsonify({"msg": "Plan not found"}), 404
    
    itinerary = generate_itinerary(
        city=plan['city'],
        budget=plan['budget'],
        hotel=data['selected_hotel'],
        days=data['days']
    )
    
    TravelPlan.update(data['plan_id'], {
        "selected_hotel": data['selected_hotel'],
        "days": data['days'],
        "itinerary": itinerary
    })
    
    return jsonify({"itinerary": itinerary}), 200