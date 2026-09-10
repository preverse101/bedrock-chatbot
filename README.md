# Bedrock Chatbot

A multi-turn chatbot powered by AWS Bedrock (Claude models) routed through the AI Gateway (Portkey), with a streaming chat UI built on Streamlit.

## Architecture

```
User → Streamlit UI → AI Gateway (Portkey) → AWS Bedrock (Claude)
```

All LLM requests are routed through AI Gateway, which provides request logging, observability, and governance. AWS Bedrock credentials are stored as a virtual key in AI Gateway — the app itself only needs the AI Gateway API key.

## Features

- Streaming responses (text appears word-by-word)
- Multi-turn conversation with full message history
- Model selector: Claude Opus 5, Sonnet 5, Fable 5.1, Opus 4.8, Haiku 4.5
- Editable system prompt
- Dark-themed chat UI
- All traffic logged and observable in AI Gateway dashboard

## Prerequisites

- Python 3.9+
- AWS account with Bedrock access enabled and Claude models activated
- IAM user with `bedrock:*` permissions
- AI Gateway (Portkey) account with a Bedrock virtual key configured

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/preverse101/bedrock-chatbot.git
cd bedrock-chatbot
```

**2. Create a virtual environment and install dependencies**
```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

**3. Configure credentials**
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1
PORTKEY_API_KEY=your_ai_gateway_api_key
```

> The AWS credentials are used to set up the Bedrock virtual key in AI Gateway.
> The app itself only calls AI Gateway using `PORTKEY_API_KEY` at runtime.

**4. Set up AI Gateway virtual key**

- Log into [AI Gateway (Portkey)](https://portkey.ai)
- Go to Virtual Keys → Add New → select AWS Bedrock
- Enter your AWS credentials and region
- Name it `bedrock-dev-integration`
- Save the virtual key

**5. Enable Bedrock model access**

In the [AWS Bedrock console](https://console.aws.amazon.com/bedrock/home#/modelaccess), enable access for the Claude models you want to use.

## Run

```bash
venv/bin/streamlit run app.py
```

Opens at `http://localhost:8501`.

## Environment Variables

| Variable | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `AWS_DEFAULT_REGION` | AWS region (e.g. `us-east-1`) |
| `PORTKEY_API_KEY` | AI Gateway API key |

## Models Available

| Display Name | Bedrock Inference Profile |
|---|---|
| Claude Opus 5 | `us.anthropic.claude-opus-5` |
| Claude Sonnet 5 | `us.anthropic.claude-sonnet-5` |
| Claude Fable 5.1 | `us.anthropic.claude-fable-5-1` |
| Claude Opus 4.8 | `us.anthropic.claude-opus-4-8` |
| Claude Haiku 4.5 | `us.anthropic.claude-haiku-4-5-20251001-v1:0` |

## Project Structure

```
bedrock-chatbot/
├── app.py              # Streamlit app — UI and AI Gateway client
├── requirements.txt    # Python dependencies
├── .env                # Credentials (not committed)
├── .env.example        # Credentials template
├── .gitignore
└── README.md
```
