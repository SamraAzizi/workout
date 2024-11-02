from langflow.load import run_flow_from_json
from dotenv import load_dotenv

load_dotenv()

TWEAKS = {
  "TextInput-bVL1G": {
    "input_value": "what is the back workout routine"
  },
  
  "TextInput-CO6Ln": {
    "input_value": "50kg, 140cm , female, active workout"
  },
 
}

result = run_flow_from_json(flow="Aiv2.json",
                            input_value="message",
                            session_id="", # provide a session id if you want to use session state
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)
print(result[0].outputs[0].results["text"].data["text"])