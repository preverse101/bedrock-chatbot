# Integrating Prisma AIRS into a Chatbot Application

## What is Prisma AIRS?

Prisma AI Runtime Security (AIRS) is a Palo Alto Networks security service that scans AI prompts and responses in real time. It detects threats like prompt injection, data leakage, malicious code, and policy violations before they reach the model or the user.

---

## How It Works in This Application

Every message goes through AIRS twice — once before hitting the LLM, once after:

```
User message
     │
     ▼
AIRS scans prompt ──── BLOCK ──► "Request blocked by security policy"
     │
   ALLOW
     │
     ▼
LLM generates response
     │
     ▼
AIRS scans response ── BLOCK ──► "Response blocked by security policy"
     │
   ALLOW
     │
     ▼
Response shown to user
```

---

## Prerequisites

- A Prisma AIRS account with API access
- An AIRS API key (`x-pan-token`)
- An AIRS security profile already created in the console (e.g. `chatbot-bedrock`)

---

## Step 1 — The Integration Script

Create a file called `prisma_airs_integration.py` in your project:

```python
import requests
import os

AIRS_API_KEY = os.environ["AIRS_API_KEY"]
AIRS_ENDPOINT = "https://service.api.aisecurity.paloaltonetworks.com"
AIRS_PROFILE = "your-profile-name"   # replace with your actual profile name

def scan_content(prompt: str, response: str = None, ai_model: str = "unknown") -> dict:
    content = {"prompt": prompt}
    if response:
        content["response"] = response

    payload = {
        "ai_profile": {"profile_name": AIRS_PROFILE},
        "metadata": {
            "app_name": "bedrock-chatbot",   # identifies your app in the AIRS console
            "ai_model": ai_model             # the actual model ID passed in at runtime
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
```

**Key parameters:**
| Parameter | Description |
|---|---|
| `AIRS_API_KEY` | Your AIRS API key, loaded from environment |
| `AIRS_ENDPOINT` | Fixed Prisma AIRS endpoint — do not change |
| `AIRS_PROFILE` | The name of the security profile you created in AIRS console |
| `prompt` | The user's input text |
| `response` | The LLM's output text (optional — include to scan responses too) |
| `ai_model` | The model ID used for this request — shown as-is in the AIRS console |

**Metadata fields (`app_name`, `ai_model`)** appear as **Application Name** and model info in the AIRS session console. Set `app_name` to a fixed string identifying your application.

`ai_model` is optional — it defaults to `"unknown"` if not passed. However, passing it dynamically is recommended when your application supports multiple models (e.g. a dropdown that lets users switch between Claude Opus, Sonnet, Haiku). Without it, all sessions in the AIRS console will show the same placeholder regardless of which model was actually used, making it harder to correlate security events to a specific model.

---

## Step 2 — Store Credentials

Add your API key to your `.env` file. Never hardcode it in the script.

```
AIRS_API_KEY=your_airs_api_key_here
```

The script reads it at runtime via `os.environ["AIRS_API_KEY"]`.

---

## Step 3 — Import and Call in Your Application

At the top of your app file, import the scan function:

```python
from prisma_airs_integration import scan_content
```

Then wrap your LLM call with AIRS scans. This is the only change needed to the application logic:

**Before (no security scanning):**
```python
response_text = call_your_llm(user_input)
show_to_user(response_text)
```

**After (with AIRS scanning):**
```python
prompt_scan = scan_content(prompt=user_input, ai_model=model_id)
if prompt_scan.get("action") == "block":
    show_to_user("Your request was blocked by security policy.")
else:
    response_text = call_your_llm(user_input)
    response_scan = scan_content(prompt=user_input, response=response_text, ai_model=model_id)
    if response_scan.get("action") == "block":
        show_to_user("The AI response was blocked by security policy.")
    else:
        show_to_user(response_text)
```

`model_id` here is the runtime model identifier (e.g. `us.anthropic.claude-opus-5` on AWS Bedrock). Pass whichever model ID your LLM client is using so the AIRS console shows the actual model per session.

---

## What the AIRS Response Looks Like

A typical scan result:

```json
{
  "action": "allow",
  "category": "benign",
  "profile_name": "chatbot-bedrock",
  "prompt_detected": {
    "injection": false,
    "dlp": false,
    "malicious_code": false,
    "url_cats": false
  },
  "report_id": "Rbc428e2a-...",
  "scan_id": "bc428e2a-..."
}
```

The only field you need to check is `action`. Its value is determined entirely by your security profile — the profile defines which threat categories to scan for and what action to take when each one fires:
- `"allow"` — no configured rules triggered, or all that triggered are set to allow in the profile
- `"block"` — at least one rule triggered and its action in the profile is set to block

---

## File Structure After Integration

```
your-app/
├── app.py                        # main application — imports scan_content
├── prisma_airs_integration.py    # AIRS scan function
├── .env                          # contains AIRS_API_KEY (never commit this)
└── requirements.txt              # add: requests>=2.31.0
```

---

## Summary of Changes to an Existing Application

1. Add `prisma_airs_integration.py` to the project
2. Set `AIRS_PROFILE` to your profile name in the script
3. Add `AIRS_API_KEY` to `.env`
4. Add `requests` to `requirements.txt`
5. Import `scan_content` at the top of your app
6. Wrap the LLM call: scan prompt → call LLM → scan response → show result
