from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os

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
     "starting and ending at the hotel. Include transportation times and realistic time allocations.")
])

def generate_itinerary(city: str, budget: float, hotel: str, days: int):
    chain = itinerary_prompt | llm
    return chain.invoke({
        "city": city,
        "days": days,
        "hotel": hotel,
        "budget": budget
    }).content