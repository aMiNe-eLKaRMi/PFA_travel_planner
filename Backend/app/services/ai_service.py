# app/services/ai_service.py
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from app.models.travel_plan import TravelPlan

llm = ChatGroq(
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192"
)

itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a detailed travel assistant. Generate a {days}-day itinerary for {city}, "
     "tailored to the user's preferences. The user is staying at {hotel}, "
     "with a total budget of {budget} dollars. Create a hour-by-hour schedule for each day, "
     "starting and ending at the hotel. Include transportation times and realistic time allocations. "
     "Official hotel website: {hotel_website}")
])

def generate_itinerary(plan_id: str, hotel: str):
    plan = TravelPlan.find_by_id(plan_id)
    if not plan:
        return "Plan not found"
    
    hotel_website = next(
        (h["website"] for h in plan["hotels"] if h["name"] == hotel),
        "No website available"
    )
    
    chain = itinerary_prompt | llm
    return chain.invoke({
        "city": plan["city"],
        "days": plan["days"],
        "hotel": hotel,
        "budget": plan["budget"],
        "hotel_website": hotel_website
    }).content