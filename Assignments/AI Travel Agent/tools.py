import os
from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
import requests
from forex_python.converter import CurrencyRates, RatesNotAvailableError


# Search tool for attractions, hotels, restaurants, etc.
search_tool = TavilySearchResults(max_results=5, description="A search engine optimized for comprehensive, accurate, and trusted results.")

@tool
def search_attractions(city: str, num_results: int = 5) -> str:
    """
    Search for top attractions and tourist spots in a city.
    
    Args:
        city: The city to search attractions for
        num_results: Number of attractions to return (default 5)
        
    Returns:
        str: List of top attractions with descriptions
    """
    search = TavilySearchResults(max_results=num_results)
    query = f"top attractions tourist spots things to do in {city}"
    try:
        results = search.invoke(query)
        attractions = [f"{i}. {result.get('title', 'Attraction')}: {result.get('content', 'No description available')}" for i, result in enumerate(results, 1)]
        return f"Top attractions in {city}:\n" + "\n".join(attractions)
    except Exception as e:
        return f"Error searching attractions: {str(e)}"

@tool
def search_restaurants(city: str, cuisine_type: str = "local", num_results: int = 5) -> str:
    """
    Search for restaurants and dining options in a city.
    
    Args:
        city: The city to search restaurants for
        cuisine_type: Type of cuisine (local, italian, asian, etc.)
        num_results: Number of restaurants to return
        
    Returns:
        str: List of recommended restaurants
    """
    search = TavilySearchResults(max_results=num_results)
    query = f"best {cuisine_type} restaurants dining in {city}"
    try:
        results = search.invoke(query)
        restaurants = [f"{i}. {result.get('title', 'Restaurant')}: {result.get('content', 'No description available')}" for i, result in enumerate(results, 1)]
        return f"Top {cuisine_type} restaurants in {city}:\n" + "\n".join(restaurants)
    except Exception as e:
        return f"Error searching restaurants: {str(e)}"

@tool
def search_activities(city: str, activity_type: str = "outdoor", num_results: int = 5) -> str:
    """
    Search for activities and experiences in a city.
    
    Args:
        city: The city to search activities for
        activity_type: Type of activities (outdoor, cultural, adventure, nightlife, etc.)
        num_results: Number of activities to return
        
    Returns:
        str: List of recommended activities
    """
    search = TavilySearchResults(max_results=num_results)
    query = f"{activity_type} activities experiences things to do in {city}"
    try:
        results = search.invoke(query)
        activities = [f"{i}. {result.get('title', 'Activity')}: {result.get('content', 'No description available')}" for i, result in enumerate(results, 1)]
        return f"Top {activity_type} activities in {city}:\n" + "\n".join(activities)
    except Exception as e:
        return f"Error searching activities: {str(e)}"

@tool
def search_transportation(city: str) -> str:
    """
    Search for transportation options in a city.
    
    Args:
        city: The city to search transportation for
        
    Returns:
        str: Transportation options and recommendations
    """
    search = TavilySearchResults(max_results=3)
    query = f"transportation options public transport getting around in {city}"
    try:
        results = search.invoke(query)
        transport_info = [f"{i}. {result.get('title', 'Transport Option')}: {result.get('content', 'No description available')}" for i, result in enumerate(results, 1)]
        return f"Transportation options in {city}:\n" + "\n".join(transport_info)
    except Exception as e:
        return f"Error searching transportation: {str(e)}"

@tool
def Google_Hotels(city: str, budget_range: str = "mid-range", num_results: int = 5) -> str:
    """
    Search for hotels in a city within a specific budget range.
    
    Args:
        city: The city to search hotels for
        budget_range: Budget category (budget, mid-range, luxury)
        num_results: Number of hotels to return
        
    Returns:
        str: List of recommended hotels with price information
    """
    search = TavilySearchResults(max_results=num_results)
    query = f"{budget_range} hotels accommodation booking in {city}"
    try:
        results = search.invoke(query)
        hotels = [f"{i}. {result.get('title', 'Hotel')}: {result.get('content', 'No description available')}" for i, result in enumerate(results, 1)]
        return f"Recommended {budget_range} hotels in {city}:\n" + "\n".join(hotels)
    except Exception as e:
        return f"Error searching hotels: {str(e)}"

@tool
def get_current_weather(city: str) -> str:
    """
    Fetches the current weather for a given city using the OpenWeatherMap API.

    Args:
        city (str): The name of the city for which to get the weather.

    Returns:
        str: A string describing the current weather conditions.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeatherMap API key is not set."
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        
        return (f"Current weather in {city}: {weather_description.title()}, "
                f"Temperature: {temperature}°C (feels like {feels_like}°C), "
                f"Humidity: {humidity}%")
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"
    except KeyError:
        return f"Error: Could not retrieve weather data for {city}. Please check the city name."

@tool
def get_multiday_weather_forecast(city: str, days: int) -> str:
    """
    Fetches the weather forecast for a given city for a specified number of days.
    
    Args:
        city (str): The name of the city.
        days (int): The number of days to forecast (up to 5).
        
    Returns:
        str: A string summarizing the weather forecast for each day.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeatherMap API key is not set."
    
    days = min(days, 5)
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": api_key, "units": "metric", "cnt": days * 8}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        forecast_summary = f"Weather forecast for {city} for the next {days} days:\n"
        daily_forecasts = {}

        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            if date not in daily_forecasts:
                daily_forecasts[date] = {'temps': [], 'descriptions': set(), 'humidity': []}
            daily_forecasts[date]['temps'].append(item['main']['temp'])
            daily_forecasts[date]['descriptions'].add(item['weather'][0]['description'])
            daily_forecasts[date]['humidity'].append(item['main']['humidity'])

        for date, daily_data in sorted(daily_forecasts.items()):
            avg_temp = sum(daily_data['temps']) / len(daily_data['temps'])
            avg_humidity = sum(daily_data['humidity']) / len(daily_data['humidity'])
            descriptions = ", ".join(daily_data['descriptions'])
            forecast_summary += f"- {date}: {avg_temp:.1f}°C, {descriptions.title()}, Humidity: {avg_humidity:.0f}%\n"
            
        return forecast_summary
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather forecast: {e}"
    except KeyError:
        return f"Error: Could not retrieve forecast for {city}."

@tool
def calculate_hotel_cost(days: int, price_per_day: float) -> str:
    """Calculates the total hotel cost."""
    total_cost = days * price_per_day
    return f"Hotel cost: {days} days × {price_per_day:.2f}/day = {total_cost:.2f}"

@tool
def calculate_daily_budget(total_budget: float, days: int, hotel_cost: float = 0) -> str:
    """Calculate daily budget after accommodation."""
    remaining = total_budget - hotel_cost
    daily = remaining / days if days > 0 else 0
    return (f"Budget: {total_budget:.2f} total - {hotel_cost:.2f} hotel = {remaining:.2f} remaining. "
            f"Daily budget: {daily:.2f}")

@tool
def calculate_total_trip_cost(hotel_cost: float, daily_expenses: float, days: int, additional_costs: float = 0) -> str:
    """Calculate the total cost of a trip."""
    total_daily = daily_expenses * days
    total_cost = hotel_cost + total_daily + additional_costs
    return (f"Total Trip Cost: {hotel_cost:.2f} (Hotel) + {total_daily:.2f} (Daily) + {additional_costs:.2f} (Additional) = {total_cost:.2f}")

@tool
def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """Get the current exchange rate."""
    c = CurrencyRates()
    try:
        rate = c.get_rate(from_currency, to_currency)
        return f"1 {from_currency} = {rate:.4f} {to_currency}"
    except Exception as e:
        return f"Error getting exchange rate: {str(e)}"

@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Converts an amount from one currency to another."""
    c = CurrencyRates()
    try:
        converted_amount = c.convert(from_currency, to_currency, amount)
        return f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}"
    except RatesNotAvailableError:
        return f"Error: Currency rates for {from_currency} to {to_currency} not available."
    except Exception as e:
        return f"Error converting currency: {str(e)}"

@tool
def create_day_plan(city: str, day_number: int, interests: str = "general") -> str:
    """Create a detailed plan for a specific day."""
    search = TavilySearchResults(max_results=3)
    query = f"day {day_number} itinerary for {interests} in {city}"
    try:
        results = search.invoke(query)
        plan = f"Day {day_number} Plan for {city} ({interests}):\n" + "\n".join([res.get('content', '') for res in results])
        return plan
    except Exception as e:
        return f"Error creating day plan: {str(e)}"

@tool
def create_full_itinerary(city: str, days: int, interests: str = "general") -> str:
    """Create a complete itinerary for the entire trip."""
    itinerary = f"Complete {days}-Day Itinerary for {city}\n\n"
    try:
        for day in range(1, days + 1):
            itinerary += create_day_plan.invoke({"city": city, "day_number": day, "interests": interests}) + "\n\n"
        return itinerary
    except Exception as e:
        return f"Error creating full itinerary: {str(e)}"