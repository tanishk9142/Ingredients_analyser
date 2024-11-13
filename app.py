import os
import logging
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
import json
import re

# Load environment variables
load_dotenv()
openai_client = OpenAI()

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
MAX_INPUT_LENGTH = 500  # Set a max length for ingredient input


# Color mapping function
def color_mapping(color_code):
    mapping = {
        "red": "red",
        "yellow": "yellow",
        "purple": "purple",
        "white": "white"
    }
    return mapping.get(color_code, "black")  # Default to black if no match


# Home route (for input form)
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle text input
@app.route('/process', methods=['POST'])
def process_text():
    text = request.form.get('ingredients')

    # Input validation: Check for empty input and length
    if not text or not isinstance(text, str) or len(text.strip()) == 0:
        return jsonify({"error": "No valid text input provided"}), 400
    if len(text) > MAX_INPUT_LENGTH:
        return jsonify({"error": f"Input exceeds maximum length of {MAX_INPUT_LENGTH} characters."}), 400

    # Call OpenAI API to analyze ingredients
    response = analyze_ingredients(text)

    # Handle cases where the response might not be in the expected format
    if isinstance(response, dict) and "error" in response:
        return jsonify(response), 500

    return jsonify(response), 200


# Analyze ingredients with OpenAI
def analyze_ingredients(text):
    try:
        # Sanitize the input by removing any unwanted characters
        text = re.sub(r'[^a-zA-Z0-9, ]', '', text)

        # Modify the prompt to request JSON output
        prompt = f"""Analyze the following ingredients and identify any harmful ones. Provide the result as a JSON array in the format: 
        [
            {{"name": "Ingredient", "is_harmful": "y/n", "can_cause": "description", "category": "harmful/moderate/non-harmful", "color_code": "yellow/red/purple/white"}}
        ]: {text}"""

        # Make API call using the updated method with a timeout
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            timeout=30  # Set a timeout for the request
        )

        # Check if the response contains any error
        if not response.choices:
            raise OpenAIError("No response choices returned from OpenAI.")

        # Extract the message content properly
        api_response = response.choices[0].message.content

        # Debugging: Log the API response to see what is returned
        logging.info("API Response: %s", api_response)

        # Process the response
        return format_response(api_response)
    except OpenAIError as e:
        logging.error("OpenAI API error: %s", str(e))
        return {"error": "An error occurred while communicating with the OpenAI API."}
    except Exception as e:
        logging.error("General error during analysis: %s", str(e))
        return {"error": "An unexpected error occurred while analyzing ingredients."}


# Format the API response into HTML with explanations for color codes
def format_response(api_response):
    try:
        start_index = api_response.find('[')
        end_index = api_response.rfind(']') + 1

        if start_index == -1 or end_index == -1:
            return {"error": "Invalid response format"}

        json_part = api_response[start_index:end_index]
        ingredients = json.loads(json_part)

        if not isinstance(ingredients, list):
            return {"error": "Response is not in the expected format."}

        result_html = ''
        for ing in ingredients:
            color_explanation = ''
            if ing["color_code"] == "red":
                color_explanation = "This ingredient is harmful due to its high saturated fat content and potential health risks."
            elif ing["color_code"] == "yellow":
                color_explanation = "This ingredient is moderate; it may have benefits but also potential risks in high amounts."
            elif ing["color_code"] == "purple":
                color_explanation = "This ingredient is generally safe but may cause allergies or reactions in sensitive individuals."
            elif ing["color_code"] == "white":
                color_explanation = "This ingredient is considered non-harmful and safe for most people."

            result_html += f'''
                <div class="card mb-3" style="border-left: 5px solid {color_mapping(ing["color_code"])};">
                    <div class="card-body">
                        <h5 class="ingredient" style="color: {color_mapping(ing["color_code"])};" onclick="toggleDetails(this)">
                            <i class="fas {'fa-check-circle' if ing['color_code'] == 'white' else 'fa-exclamation-circle'}"></i>
                            {ing["name"]}
                        </h5>
                        <div class="details" style="display: none;">{color_explanation}</div>
                    </div>
                </div>
            '''

        return result_html if result_html else "No flagged ingredient found."
    except json.JSONDecodeError:
        logging.error("Failed to decode API response as JSON.")
        return {"error": "Failed to decode API response as JSON."}
    except Exception as e:
        logging.error("Error formatting response: %s", str(e))
        return {"error": "An unexpected error occurred while formatting the response."}



if __name__ == '__main__':
    app.run(debug=True)