# Bedrock Chatbot

A multi-turn chatbot powered by AWS Bedrock (Claude models) routed through the AIRS API Runtime (not Portkey), with a streaming chat UI built on Streamlit.

## Architecture

```
User → Streamlit UI → AIRS API Runtime (not Portkey) → AWS Bedrock (Claude)
```

Every user message is scanned by Prisma AIRS before being sent to Bedrock, and the model response is scanned again before being shown to the user. The app connects directly to AWS Bedrock — no proxy or gateway in the request path.

## Features

- Streaming responses (text appears word-by-word)
- Multi-turn conversation with full message history
- Model selector: Claude Opus 5, Sonnet 5, Fable 5.1, Opus 4.8, Haiku 4.5
- Editable system prompt
- Dark-themed chat UI
- Prompt and response scanning via Prisma AIRS API Runtime
- Security violations blocked before reaching the model or the user

## Prerequisites

- Python 3.9+
- AWS account with Bedrock access enabled and Claude models activated
- IAM user with `bedrock:*` permissions
- Prisma AIRS account with an API key and a security profile created

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
AIRS_API_KEY=your_airs_api_key
```

**4. Set your AIRS profile name**

In `prisma_airs_integration.py`, set `AIRS_PROFILE` to the name of the security profile you created in the Prisma AIRS console:

```python
AIRS_PROFILE = "your-profile-name"
```

**5. Enable Bedrock model access**

In the [AWS Bedrock console](https://console.aws.amazon.com/bedrock/home#/modelaccess), enable access for the Claude models you want to use.

## Run

```bash
venv/bin/streamlit run app.py --server.headless true
```

Opens at `http://localhost:8501`.

## Environment Variables

| Variable | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `AWS_DEFAULT_REGION` | AWS region (e.g. `us-east-1`) |
| `AIRS_API_KEY` | Prisma AIRS API key (`x-pan-token`) |

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
├── app.py                        # Streamlit app — UI and Bedrock client
├── prisma_airs_integration.py    # Prisma AIRS scan function
├── PRISMA_AIRS_INTEGRATION.md    # AIRS integration documentation
├── requirements.txt              # Python dependencies
├── .env                          # Credentials (not committed)
├── .env.example                  # Credentials template
├── .gitignore
└── README.md
```
