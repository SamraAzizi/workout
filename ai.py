from langflow.load import run_flow_from_json
from dotenv import load_dotenv
import requests
from typing import Optional
import json
import os

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "cbbb7940-be72-4327-871c-3cd4a7256d45"
APPLICATION_TOKEN = os.getenv("LANGFLOW_TOKEN")


def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level  # Indentation for nested levels
    
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")

    return ", ".join(strings)





def ask_ai(profile, question):
    TWEAKS = {
        "TextInput-XjIKI": {
            "input_value": question
        },
        "TextInput-176Ns": {
            "input_value": dict_to_string(profile)
        },
    }

    result = run_flow_from_json(flow="Aiv2.json",
                                input_value="message",
                                fallback_to_env_vars=True,
                                tweaks=TWEAKS)

    return result[0].outputs[0].results["text"].data["text"]


def get_macro(profile, goals):
    TWEAKS = {
        "TextInput-PR5Jb": {
            "input_value": ", ".join(goals)
        },
        "TextInput-PrfY9": {
            "input_value": dict_to_string(profile)
        }
    }
    
    return run_flow("", tweaks=TWEAKS, application_token=APPLICATION_TOKEN)


def run_flow(message: str,
             output_type: str = "chat",
             input_type: str = "chat",
             tweaks: Optional[dict] = None,
             application_token: Optional[str] = None) -> dict:
    
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/macro"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {
            "Authorization": "Bearer " + application_token,
            "Content-Type": "application/json"
        }

    print(f"Using application token: {application_token}")
    
    # Make the API request
    response = requests.post(api_url, json=payload, headers=headers)

    # Check for errors in the response
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response Text: {response.text}")
        return None  # or raise an exception, or handle as needed

    # Check if the response is empty
    if not response.text:
        print("Error: Received empty response")
        return None

    # Parse the JSON response
    try:
        response_json = response.json()
        # Ensure that the expected structure exists
        if "outputs" in response_json and response_json["outputs"]:
            return json.loads(response_json["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])
        else:
            print("Error: Unexpected response structure")
            print(f"Response JSON: {response_json}")
            return None
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {str(e)}")
        print(f"Response Text: {response.text}")
        return None
