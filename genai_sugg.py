# Load environment variables from .env file
from openai import OpenAI
from dotenv import load_dotenv
import os

from prompt_builder import get_user_message, generate_assistant_message

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def generate_suggestion(scanned_items, suggestion_type):
    system_message = generate_assistant_message(suggestion_type)
    user_message = get_user_message(scanned_items,suggestion_type)
    print("user message is " + str(user_message))
    print("system message is " + str(system_message))
    try:

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )

        # Split the response message by newlines to get a list of strings
        response_message = completion.choices[0].message.content

        # print(response_message)
        # responses = [line for line in response_message.split('\n')[1:] if line.strip()]

        return response_message

    except Exception as e:
        print(e)
        pass


if __name__ == "__main__":
    print(generate_suggestion(['lemon'],"storage"))
