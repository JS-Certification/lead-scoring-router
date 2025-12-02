# Zoho Score Router

A FastAPI application that routes applicants based on their AI-generated qualification score from Zoho CRM.

> **[View Full Flow Documentation](docs/FLOW.md)** - Includes Mermaid diagrams and detailed step-by-step flow.

## How It Works

1. User submits a Zoho Form → generates a 10-char Submission ID
2. Zoho CRM stores the submission and runs LLM-based scoring
3. User is redirected to `/?key={SUBMISSION_ID}`
4. Router queries Zoho CRM for the score
5. **Score >= threshold** → Redirect to booking page (qualified)
6. **Score < threshold** → Redirect to thank you page (not qualified)

## Quick Start

### 1. Clone and Install

```bash
git clone <your-repo>
cd jscs-router
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Zoho credentials (see below)
```

### 3. Run Locally

```bash
uvicorn app.main:app --reload
```

Visit: `http://localhost:8000/?key=test@example.com`

## Zoho API Setup

### Step 1: Create a Self Client

1. Go to [Zoho API Console](https://api-console.zoho.com/)
2. Click **Add Client** → Select **Self Client**
3. Note down your **Client ID** and **Client Secret**

### Step 2: Generate Grant Token

1. In the Self Client, click **Generate Code**
2. Enter scope: `ZohoCRM.modules.custom.READ`
   - This scope covers all custom modules (like Form_Submissions)
3. Set time duration (e.g., 10 minutes)
4. Enter a description and click **Create**
5. Copy the generated **Grant Token**

### Step 3: Exchange Grant Token for Refresh Token

Run this curl command (replace placeholders):

```bash
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "grant_type=authorization_code" \
  -d "client_id=YOUR_CLIENT_ID" \
  -d "client_secret=YOUR_CLIENT_SECRET" \
  -d "code=YOUR_GRANT_TOKEN"
```

The response will contain your **refresh_token**. Save this - it doesn't expire.

### Step 4: Configure Environment Variables

Add to your `.env` file:

```
ZOHO_CLIENT_ID=your_client_id
ZOHO_CLIENT_SECRET=your_client_secret
ZOHO_REFRESH_TOKEN=your_refresh_token
SUCCESS_REDIRECT_URL=https://calendly.com/your-link
```

## Configuration Options

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ZOHO_CLIENT_ID` | Yes | - | Zoho OAuth Client ID |
| `ZOHO_CLIENT_SECRET` | Yes | - | Zoho OAuth Client Secret |
| `ZOHO_REFRESH_TOKEN` | Yes | - | Zoho OAuth Refresh Token |
| `SUCCESS_REDIRECT_URL` | Yes | - | URL to redirect when score >= threshold |
| `ZOHO_MODULE_NAME` | No | `Form_Submissions` | Zoho CRM module API name |
| `ZOHO_SCORE_FIELD` | No | `Score` | Field name containing the score |
| `ZOHO_KEY_FIELD` | No | `Email` | Field name to search by (matches `?key=` param) |
| `SCORE_THRESHOLD` | No | `70` | Minimum score for success redirect |
| `THANK_YOU_PAGE_URL` | No | - | External thank you page URL |
| `ZOHO_API_DOMAIN` | No | `https://www.zohoapis.com` | Zoho API domain |
| `ZOHO_ACCOUNTS_URL` | No | `https://accounts.zoho.com` | Zoho accounts URL |

## Deploy to Railway

### Option 1: Deploy from GitHub

1. Push this repo to GitHub
2. Go to [Railway](https://railway.app/)
3. Click **New Project** → **Deploy from GitHub repo**
4. Select your repository
5. Add environment variables in **Variables** tab
6. Railway will auto-detect the Dockerfile and deploy

### Option 2: Deploy with Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

Then add environment variables in the Railway dashboard.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/?key=<value>` | GET | Main routing endpoint |
| `/thank-you` | GET | Thank you page |
| `/health` | GET | Health check |

## Development

```bash
# Run with auto-reload
uvicorn app.main:app --reload --port 8000

# Run with Docker
docker build -t zoho-router .
docker run -p 8000:8000 --env-file .env zoho-router
```
