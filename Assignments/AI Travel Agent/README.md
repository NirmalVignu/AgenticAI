
# AI Travel Agent 🌍✈️

A comprehensive, AI-powered travel agent that helps you plan every aspect of your trip. Just provide your destination, duration, and interests, and the agent will generate a detailed itinerary, including attractions, restaurants, weather forecasts, budget breakdowns, and more.

## Features

- **Dynamic Itinerary Generation:** Creates detailed day-by-day plans based on your interests.
- **Real-time Information:** Fetches current weather and multi-day forecasts.
- **Comprehensive Search:** Finds top attractions, restaurants, activities, and transportation options.
- **Accommodation Suggestions:** Recommends hotels based on your budget (budget, mid-range, luxury).
- **Budgeting Tools:** Calculates hotel costs, daily budgets, and total trip costs.
- **Currency Conversion:** Provides real-time exchange rates and currency conversions.
- **PDF Export:** Saves your complete travel plan as a downloadable PDF.

## How It Works

This application is built with a sophisticated agentic architecture using the following technologies:

- **LangChain & LangGraph:** The core framework for building the AI agent and defining the workflow. The agent uses a set of tools to gather information and construct the travel plan.
- **Groq:** Powers the language model (LLaMA3) for fast and intelligent responses.
- **Tavily Search:** The primary search engine for finding information about attractions, hotels, and more.
- **OpenWeatherMap:** Provides real-time weather data.
- **Streamlit:** Creates the interactive web user interface.

The agent takes a user's query, breaks it down into steps, and uses the available tools to find the necessary information. The entire process, including the agent's "thoughts," is streamed to the user interface, providing transparency into how the plan is being created.

## Setup and Installation

To run this project locally, follow these steps:

**1. Clone the Repository**

```bash
git clone [https://github.com/your-username/AI-Travel-Agent.git](https://github.com/your-username/AI-Travel-Agent.git)
cd AI-Travel-Agent
````

**2. Create a `.env` File**

Create a file named `.env` in the root of the project directory and add your API keys:

```
OPENWEATHER_API_KEY="your_openweathermap_api_key"
GROQ_API_KEY="your_groq_api_key"
TAVILY_API_KEY="your_tavily_api_key"
```

**3. Install Dependencies**

Install all the required Python libraries using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

To start the application, run the following command in your terminal:

```bash
streamlit run app.py
```

Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

## Example Output

Here is a sample travel plan generated for a 7-day trip to Manali, India. The application can generate a similar PDF for your custom query.

*(Image of the first page of Trip\_Plan\_Manali.pdf)*

The plan includes:

  - A trip overview
  - Weather information and packing advice
  - A detailed daily itinerary
  - Accommodation options
  - Top attractions and activities
  - Dining recommendations
  - A transportation guide
  - A comprehensive budget breakdown
  - Essential travel tips

## Tools Used

  - **Programming Language:** Python
  - **Web Framework:** Streamlit
  - **AI/LLM Framework:** LangChain, LangGraph
  - **Language Model:** Groq (LLaMA3)
  - **Search:** Tavily Search API
  - **Weather:** OpenWeatherMap API
  - **PDF Generation:** xhtml2pdf

<!-- end list -->

```
```