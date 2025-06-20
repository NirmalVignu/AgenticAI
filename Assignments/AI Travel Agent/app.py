import os
import re
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool

from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.runnables import RunnableConfig
from save_pdf import create_pdf
from tools import (
    search_tool, search_attractions, search_restaurants, search_activities,
    search_transportation, Google_Hotels, get_current_weather,
    get_multiday_weather_forecast, calculate_hotel_cost, calculate_daily_budget,
    calculate_total_trip_cost, get_exchange_rate, convert_currency,
    create_day_plan, create_full_itinerary
    )



# --- 1. Load Environment Variables ---

load_dotenv()

# In Streamlit Cloud, you would set these in the secrets management.
os.environ["OPENWEATHER_API_KEY"] = os.getenv("OPENWEATHER_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")


# --- 2. Initialize Tools ---
tools = [
    search_tool, search_attractions, search_restaurants, search_activities,
    search_transportation, Google_Hotels, get_current_weather,
    get_multiday_weather_forecast, calculate_hotel_cost, calculate_daily_budget,
    calculate_total_trip_cost, get_exchange_rate, convert_currency,
    create_day_plan, create_full_itinerary
]


# --- 3. Define the Agent's State ---
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# --- 4. Define the Agent's Nodes ---
class TravelAgent:
    def __init__(self, model, tools):
        self.model = model.bind_tools(tools)

    def run_agent(self, state: AgentState, config: RunnableConfig):
        return {"messages": [self.model.invoke(state['messages'], config)]}




# Use a robust model
model = ChatGroq(model="llama3-70b-8192", temperature=0)

travel_agent = TravelAgent(model, tools)

# --- 5. Define the Workflow ---
workflow = StateGraph(AgentState)
workflow.add_node("agent", travel_agent.run_agent)
workflow.add_node("tools", ToolNode(tools))
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", tools_condition)
workflow.add_edge("tools", "agent")

app = workflow.compile()





# --- 6. Streamlit Web App Interface ---

st.set_page_config(page_title="🌍 AI Travel Agent", page_icon="✈️", layout="wide")

st.title("🌍 Comprehensive AI Travel Agent 🧳")
st.markdown("I can help you plan every aspect of your trip. Just tell me your destination, duration, and interests!")

# Initialize session state to hold the plan
if 'travel_plan' not in st.session_state:
    st.session_state.travel_plan = ""

# User input form
with st.form("travel_form"):
    user_query = st.text_area(
        "✈️ What travel plans can I help you with?",
        "Plan a 5-day trip to Tokyo for a solo traveler interested in anime and food."
    )
    submitted = st.form_submit_button("Plan My Trip")

if submitted and user_query:
    if not all([os.getenv("OPENWEATHER_API_KEY"), os.getenv("GROQ_API_KEY"), os.getenv("TAVILY_API_KEY")]):
        st.error("API keys are not configured. Please add them to your .env file or Streamlit secrets.")
    else:
        st.session_state.travel_plan = "" # Reset previous plan
        inputs = {"messages": [HumanMessage(content=user_query)]}

        with st.spinner("⏳ Let me think... Crafting the perfect trip for you..."):
            
            # --- Agent Execution Logic (Adapted for Streamlit) ---
            conversation_history = [f"User: {user_query}"]
            
            # Use an expander to show the agent's thought process
            with st.expander("🤖 View Agent's Thought Process..."):
                try:
                    # Stream the agent's execution steps
                    for output in app.stream(inputs, {"recursion_limit": 15}):
                        for key, value in output.items():
                            if 'messages' in value:
                                for msg in value['messages']:
                                    if isinstance(msg, AIMessage):
                                        if msg.tool_calls:
                                            st.write(f"**Tool Calls:**")
                                            for tool_call in msg.tool_calls:
                                                st.info(f"Calling `{tool_call['name']}` with args: `{tool_call['args']}`")
                                                conversation_history.append(f"Tool Call: {tool_call['name']}({tool_call['args']})")
                                        if msg.content:
                                            st.write(f"**AI:** {msg.content}")
                                            conversation_history.append(f"AI: {msg.content}")
                                    elif isinstance(msg, HumanMessage):
                                        st.write(f"**User:** {msg.content}")
                                    else: # ToolMessage
                                        st.success(f"**Tool Output [{msg.name}]:**\n\n{msg.content}")
                                        conversation_history.append(f"Tool Result [{msg.name}]: {msg.content}")
                except Exception as e:
                     st.error(f"An error occurred during agent execution: {e}")


            st.info("Generating the final comprehensive travel plan...")
            
            # --- Final Summary Generation ---
            conversation_text = "\n".join(conversation_history)
            summary_prompt = f"""You are an expert travel planner. Create a comprehensive, detailed travel plan based on the user's request: "{user_query}"

            Please provide a complete travel guide. Use the conversation context to fill in the details.

            # 🌍 TRIP OVERVIEW
            - Destination, duration, and highlights.

            # ☀️ WEATHER & CLIMATE
            - Current and forecasted weather. Packing advice.

            # 🗓️ DETAILED DAILY ITINERARY
            - A day-by-day plan with morning, afternoon, and evening activities.

            # 🏨 ACCOMMODATION
            - Hotel recommendations (budget, mid-range, luxury).

            # 🎯 TOP ATTRACTIONS & ACTIVITIES
            - Must-see landmarks and experiences.

            # 🍽️ DINING RECOMMENDATIONS
            - Local cuisine, restaurant suggestions.

            # 🚗 TRANSPORTATION GUIDE
            - How to get around the city.

            # 💰 COMPREHENSIVE BUDGET BREAKDOWN
            - Detailed cost estimates for accommodation, food, transport, and activities.
            - Currency conversions if applicable.

            # 💡 TRAVEL TIPS & ESSENTIALS
            - Local customs, safety tips, language basics.

            Based on the conversation context:
            ---
            {conversation_text}
            ---

            Make this a practical, actionable travel guide. Use Markdown for formatting.
            """
            
            try:
                summary_response = model.invoke(summary_prompt)
                final_summary = summary_response.content if hasattr(summary_response, 'content') else str(summary_response)
                st.session_state.travel_plan = final_summary
            except Exception as e:
                st.error(f"Failed to generate the final summary: {e}")
                st.session_state.travel_plan = "Sorry, I couldn't generate the final plan due to an error."

# Display the final plan if it exists
if st.session_state.travel_plan:
    st.markdown("---")
    st.subheader("🎉 Your Custom Travel Itinerary")
    st.markdown(st.session_state.travel_plan)
    
    # --- NEW: PDF Download Button ---
    try:
        pdf_data = create_pdf(st.session_state.travel_plan)
        # Extract a clean filename from the user query
        clean_destination = re.sub(r'[^\w\s-]', '', user_query.split("to ")[-1].split(" ")[0]).strip()
        file_name = f"Trip_Plan_{clean_destination}.pdf"
        
        st.download_button(
            label="⬇️ Download Plan as PDF",
            data=pdf_data,
            file_name=file_name,
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Sorry, couldn't generate the PDF. Error: {e}")