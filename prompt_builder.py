import requests
from datetime import datetime


def generate_assistant_message(suggestion_type):
    # Dictionary to store different suggestion types and their corresponding templates
    assistant_templates = {
        'storage': (
            "The assistant is tasked with providing personalized storage tips for perishable items based on the user's current location and the season. "
            "The tips should focus on how to properly store each item to maximize freshness and reduce waste, considering local climate and typical storage practices."
            "\n\nExample Prompt:\n"
            "\"Given the following scanned items: tomatoes, broccoli, and carrots, and considering that the user is currently in Rogers, Arkansas, United States during the summer season, "
            "generate personalized storage tips that advise on the best methods to keep these items fresh for as long as possible. Consider any region- and season-specific practices for storing these items.\""
        ),

        'nutritional': (
            "The assistant is tasked with providing nutritional information about scanned perishable items. "
            "The information should highlight the key nutrients and health benefits of each item, and consider any region-specific dietary relevance."
            "\n\nExample Prompt:\n"
            "\"Given the following scanned items: tomatoes, broccoli, and carrots, and considering that the user is currently in Rogers, Arkansas, United States, "
            "generate personalized nutritional information that highlights the key health benefits of these items. Include any relevant details on how these foods contribute to a balanced diet, particularly in the context of regional dietary preferences.\""
        ),

        'sustainability': (
            "The assistant is tasked with offering sustainability tips related to the use and disposal of scanned perishable items. "
            "The tips should focus on environmentally friendly practices, including reducing waste, composting, and supporting local agriculture."
            "\n\nExample Prompt:\n"
            "\"Given the following scanned items: tomatoes, broccoli, and carrots, and considering that the user is currently in Rogers, Arkansas, United States, "
            "generate personalized sustainability tips that encourage environmentally friendly practices. Include suggestions on how to reduce waste, compost scraps, and support local agriculture, tailored to the current season and region.\""
        ),

        'pairing': (
            "The assistant is tasked with suggesting complementary non-perishable items that pair well with the scanned perishable items. "
            "These suggestions should focus on creating balanced meals and enhancing the use of perishable items, considering local and seasonal preferences."
            "\n\nExample Prompt:\n"
            "\"Given the following scanned items: tomatoes, broccoli, and carrots, and considering that the user is currently in Rogers, Arkansas, United States during the summer season, "
            "generate personalized suggestions for non-perishable items that pair well with these scanned items. Ensure the suggestions complement the scanned items to create balanced meals and consider local and seasonal preferences.\""
        ),

        'mealplan': (
            "The assistant is tasked with generating personalized meal plans based on scanned fruits and vegetables. "
            "The meal plan should consider the user's current location and the season to provide region- and season-specific dietary preferences and cuisine. "
            "Additionally, the meal plan should include suggestions for complementary ingredients, focusing on local, seasonal produce. "
            "The ingredients should be presented as clickable links, allowing users to add them to their shopping list."
            "\n\nExample Prompt:\n"
            "\"Given the following scanned items: tomatoes, broccoli, carrots, and considering that the user is currently in Rogers, Arkansas, United States during the summer season, "
            "generate a personalized meal plan that considers the dietary preferences and cuisine typical of the Arkansas region during the summer season. "
            "Suggest any additional ingredients that might complement these scanned items for a complete meal. "
            "Take into account local, seasonal produce available in Arkansas during summer. Additionally, when listing the ingredients, make them clickable so users can add them to their shopping list by clicking on them.\""
            "\n\nExpected Output:\n"
            "**Meal Plan:**\n"
            "1. **Grilled Tomato and Broccoli Salad**:\n"
            "- **Ingredients**: [Tomatoes](#), [Broccoli](#), [Red Onion](#), [Feta Cheese](#), [Olive Oil](#), [Lemon Juice](#)\n"
            "- **Instructions**: Grill the tomatoes and broccoli until charred. Combine with thinly sliced red onion, crumbled feta cheese, and a dressing made from olive oil and lemon juice. Serve chilled.\n\n"
            "2. **Southern-Style Barbecue Carrots**:\n"
            "- **Ingredients**: [Carrots](#), [Brown Sugar](#), [Butter](#), [BBQ Sauce](#)\n"
            "- **Instructions**: Roast the carrots with butter and brown sugar until tender. Toss in your favorite BBQ sauce and grill for a few minutes to caramelize. Serve as a side dish with any summer meal.\n\n"
            "**Additional Suggestions**:\n"
            "- Consider adding [Cornbread](#) or [Collard Greens](#) to complement the meal plan.\n"
            "- Make a refreshing summer drink with [Lemonade](#).\n\n"
            "**Local Seasonal Produce**:\n"
            "- During summer in Arkansas, consider incorporating fresh [Peaches](#) or [Watermelon](#) into your meals or desserts for a truly local experience."
        )
    }

    # Get the corresponding template based on the suggestion type
    return assistant_templates.get(suggestion_type, "Invalid suggestion type provided.")


def generate_user_message(region, city, season, scanned_items, suggestion_type):
    # Join scanned items into a single string
    items_list = ', '.join(scanned_items)

    # Dictionary to store different suggestion types and their corresponding templates
    suggestion_templates = {
        'storage': f"I've just scanned some {items_list}. Can you give me tips on how to store these items to keep them fresh for as long as possible? I’m in {city}, {region}, and it’s currently {season}, so any tips specific to this season and region would be great.",

        'nutritional': f"I’ve scanned {items_list}. Could you tell me more about their nutritional benefits? I’m interested in how these might fit into a healthy diet, especially considering I’m in {city}, {region}, during the {season}.",

        'sustainability': f"I’ve just scanned some {items_list}. Do you have any sustainability tips for using and storing these items? I’d like to reduce waste and support local farming practices here in {city}, {region}.",

        'pairing': f"I scanned some {items_list}. Can you suggest some non-perishable items that would pair well with these for balanced meals? I’m in {city}, {region}, and it’s {season} right now, so anything seasonally appropriate would be helpful."
    }

    # Get the corresponding template based on the suggestion type
    return suggestion_templates.get(suggestion_type, "Invalid suggestion type provided.")


# Function to get the current location using an IP-based geolocation service
def get_current_location():
    response = requests.get('http://ip-api.com/json/')
    data = response.json()
    return data['city'], data['regionName'], data['country']


# Function to determine the current season based on the month
def get_current_season():
    month = datetime.now().month
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    elif month in [9, 10, 11]:
        return 'fall'


# Function to generate a prompt based on the template
def build_prompt(scanned_items, city, region, country, season):
    prompt = f"""
    Given the following scanned items: {', '.join(scanned_items)}, and considering that the user is currently in {city}, {region}, {country} during the {season} season,
    generate a personalized meal plan mostly avaliable in {city}, {region}, {country}. Please focus on  cuisine  avaliable in {city}, {region}, {country} during the {season} season and suggest any additional ingredients that might complement these scanned items for a complete meal. 
    Take into account local, seasonal produce available in {region} during {season}. Additionally, when listing the ingredients, make them clickable so users can add them to their shopping list by clicking on them.
    """
    return prompt


# Example usage with actual data
def get_user_message(scanned_items,suggestion_type):
    # Example scanned items
    # scanned_items = ["tomatoes", "broccoli", "carrots"]

    # Fetch current location and season
    city, region, country = get_current_location()
    season = get_current_season()

    # Fetch cuisine and dietary preferences dynamically
    #cuisine, dietary_preferences = fetch_cuisine_and_dietary_preferences(region, season)

    # Generate the prompt using the template
    prompt = generate_user_message(region,city,season,scanned_items,suggestion_type)
    return prompt


# Run the main function
if __name__ == "__main__":
    pass
    # main()
