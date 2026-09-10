import requests
import os

AIRS_API_KEY = os.environ["AIRS_API_KEY"]
AIRS_ENDPOINT = "https://service.api.aisecurity.paloaltonetworks.com"
AIRS_PROFILE = "chatbot-bedrock"

def scan_content(prompt: str, response: str = None, ai_model: str = "unknown") -> dict:
    """Scan a prompt (and optionally a response) with AIRS API Intercept."""
    content = {"prompt": prompt}
    if response:
        content["response"] = response

    payload = {
        "ai_profile": {"profile_name": AIRS_PROFILE},
        "metadata": {
            "app_name": "bedrock-chatbot",
            "ai_model": ai_model
        },
        "contents": [content]
    }

    resp = requests.post(
        f"{AIRS_ENDPOINT}/v1/scan/sync/request",
        headers={
            "x-pan-token": AIRS_API_KEY,
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()

def chat_with_ai(user_prompt: str) -> str:
    """Example: scan prompt, call AI model, scan response, return."""
    # 1. Scan the user's prompt
    prompt_scan = scan_content(prompt=user_prompt)
    if prompt_scan["action"] == "block":
        return "Your request was blocked by security policy."

    # 2. Send to your AI model (example: OpenAI)
    ai_response = call_your_ai_model(user_prompt)

    # 3. Scan the AI model's response
    response_scan = scan_content(
        prompt=user_prompt,
        response=ai_response
    )
    if response_scan["action"] == "block":
        return "The AI response was blocked by security policy."

    # 4. Return the safe response
    return ai_response