import pandas as pd

df  = pd.read_csv('restaurants.csv')
df1 = pd.read_csv('weather.csv')
df2 = pd.read_csv('tram_stations.csv')


class Task:
    def handle_input(self):
        pass

class WeatherTask(Task):
    keywords = ["weather", "temperature"]

    def handle_input(self, user_input, context):
        weather_cities = set(df1['city'].str.lower())
        weather_city = next((c for c in weather_cities if c in user_input.lower()), None)

        if weather_city:
            response = get_weather_forecast(weather_city)
            print(response)
        else:
            response = "The weather somewhere is 30 degrees and the sun is shining. Can you specify what city you are interested in?"
            specified_city = input("City: ")
            response = get_weather_forecast(specified_city)
            print(response)

        

class RestaurantTask(Task):
    keywords = ["restaurant", "food", "lunch", "dinner", "eat"]

    def handle_input(self, user_input, context):
        cities = set(df['city'].str.lower())
        costs = set(df['cost'].str.lower())

        city = next((c for c in cities if c in user_input.lower()), None)
        cost = next((c for c in costs if c in user_input.lower()), None)

        if city and cost:
            response = find_restaurant(city, cost)
        elif city:
            cost_input = input(f"Sure, you want to eat in {city}. What price range are you looking for? (Cheap/Expensive) ")
            cost = next((c for c in costs if c in cost_input.lower()), None)
            if cost:
                response = find_restaurant(city, cost)
            else:
                response = "I'm sorry, I couldn't determine the price range for the restaurant search."
        elif cost:
            city_input = input(f"Sure, you want to eat in a {cost} restaurant. In which city are you looking? ")
            city = next((c for c in cities if c in city_input.lower()), None)
            if city:
                response = find_restaurant(city, cost)
            else:
                response = "I'm sorry, I couldn't determine the city for the restaurant search."
        else:
            city_input = input("Sure, where would you like to eat? ")
            cost_input = input("Great! What price range are you looking for? (Cheap/Expensive) ")
            city = next((c for c in cities if c in city_input.lower()), None)
            cost = next((c for c in costs if c in cost_input.lower()), None)
            if city and cost:
                response = find_restaurant(city, cost)
            else:
                response = "I'm sorry, I couldn't determine both the city and price range for the restaurant search."

        print(response)

class findTheTram(Task):
    keywords = ["tram", "travel","go", "take"]
    def handle_input(self, user_input, context):
        departures = set(df2['departure'].str.lower())
        d_times = set(df2['d_time'].str.lower())
        arrivals = set(df2['arrival'].str.lower())
        a_times = set(df2['a_time'].str.lower())

        departure = next((c for c in departures if c in user_input.lower()), None)
        d_time = next((c for c in d_times if c in user_input.lower()), None)
        arrival = next((c for c in arrivals if c in user_input.lower()), None)
        a_time = next((c for c in a_times if c in user_input.lower()), None)

        if departure and arrival:
            a_time = input(f"Sure, at what time would you like to arrive at {arrival}? ")
            response = find_tram(departure, arrival, a_time)
        elif arrival:
            departure = input(f"Sure, where would you like to depart from? ")
            a_time = input(f"At what time would you like to arrive at {arrival}? ")
            response = find_tram(departure, arrival, a_time)
        elif departure:
            arrival = input(f"Sure, where would you like to arrive? ")
            a_time = input(f"At what time would you like to arrive at {arrival}? ")
            response = find_tram(departure, arrival, a_time)
        else:
            departure_input = input("Sure, where would you like to depart from? ")
            arrival_input = input("Great! Where would you like to arrive? ")
            departure = next((c for c in departures if c in departure_input.lower()), None)
            arrival = next((c for c in arrivals if c in arrival_input.lower()), None)
            if departure and arrival:
                a_time = input("When would you like to arrive? ")
                response = find_tram(departure, arrival, a_time)
            else:
                response = "I'm sorry, I couldn't determine both the city and price range for the restaurant search."

        print(response)

    


def find_restaurant(city, cost):
    matching_restaurants = df[(df['city'].str.lower() == city) & (df['cost'].str.lower() == cost)]
    if not matching_restaurants.empty:
        selected_restaurant = matching_restaurants.sample()['name'].iloc[0]
        return f"I found a {cost} restaurant in {city.capitalize()}: {selected_restaurant}."
    else:
        return f"Sorry, I couldn't find a {cost} restaurant in {city.capitalize()}."
    
def get_weather_forecast(city):
    matching_weather = df1[df1['city'].str.lower() == city.lower()]

    if not matching_weather.empty:
        selected_weather = matching_weather.sample().iloc[0]
        return f"The weather in {city.capitalize()} is {selected_weather['weather']} with a temperature of {selected_weather['temperature']}°C."
    else:
        return f"Sorry, I couldn't find the weather forecast for {city.capitalize()}."

def find_tram(departure, arrival, a_time):
    matching_tram = df2[(df2['departure'].str.lower() == departure) & (df2['arrival'].str.lower() == arrival) & (df2['a_time'].str.lower() == a_time)]
    if not matching_tram.empty:
        selected_tram = matching_tram.sample()['d_time'].iloc[0]
        return f"I found a tram traveling from {departure} at {selected_tram} to {arrival} arriving {a_time}."
    else:
        return f"Sorry, I couldn't find  {departure} to {arrival}."

def main():
    print("Hi, my name is Antoxander!")

    tasks = [WeatherTask(), RestaurantTask(), findTheTram()]
    context = {}

    while True:
        user_input = input("How can I assist you? ")

        for task in tasks:
            if any(keyword in user_input.lower() for keyword in task.keywords):
                task.handle_input(user_input, context)
                break
        else:
            print("I'm sorry, I didn't understand that request.")

if __name__ == "__main__":
    main()