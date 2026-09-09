# Bedrock Chatbot

A multi-turn chatbot powered by AWS Bedrock and Claude, with a clean streaming UI built on Streamlit.

## Features

- Streaming responses (text appears word-by-word)
- Multi-turn conversation with full history
- Model selector: Claude Opus 5, Sonnet 5, Fable 5.1, Opus 4.8, Haiku 4.5
- Editable system prompt
- Dark-themed chat UI

## Prerequisites

- Python 3.9+
- AWS account with Bedrock access enabled
- IAM user with `bedrock:*` permissions

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/bedrock-chatbot.git
cd bedrock-chatbot
```

**2. Create a virtual environment and install dependencies**
```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```

**3. Configure AWS credentials**
```bash
cp .env.example .env
```
Edit `.env` and fill in your AWS credentials:
```
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=us-east-1
```

**4. Enable Bedrock model access**

In the [AWS Bedrock console](https://console.aws.amazon.com/bedrock/home#/modelaccess), enable access for the Claude models you want to use.

## Run

```bash
venv/bin/streamlit run app.py
```

Opens at `http://localhost:8501`.
