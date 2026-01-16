# Deployment Options

Since this project has a `Dockerfile`, you can deploy it for **FREE** on several platforms.

## Option 1: Hugging Face Spaces (Recommended & 100% Free)
Hugging Face Spaces is designed for Streamlit apps and stays online.

1.  **Create an Account**: Go to [huggingface.co](https://huggingface.co/) and sign up.
2.  **Create a New Space**:
    *   Click **New Space** (top right).
    *   **Space Name**: `migration-audit-platform`.
    *   **SDK**: Select **Docker** (Best for custom configs) OR **Streamlit** (Easier/Faster).
    *   **License**: MIT (optional).
    *   **Visibility**: Public.
    *   Click **Create Space**.
3.  **Deploy Code**:
    *   **Easy Way**: Click "Files" -> "Add file" -> "Upload files" and upload your `app.py`, `requirements.txt`, and `Dockerfile`.
    *   **Git Way**: Use the git commands shown on the creation page to push this `streamlit-frontend` folder to the Space.

## Option 2: Render (Free Tier)
Render is a great general-purpose cloud provider.

1.  **Create an Account**: Go to [dashboard.render.com](https://dashboard.render.com/).
2.  **New Web Service**:
    *   Click **New +** -> **Web Service**.
    *   Connect your GitHub account and select your repository.
3.  **Settings**:
    *   **Name**: `migration-audit`.
    *   **Region**: Closest to you (e.g., Oregon or Frankfurt).
    *   **Branch**: `main`.
    *   **Root Directory**: `streamlit-frontend` (Important!).
    *   **Runtime**: **Docker**.
    *   **Plan**: **Free**.
4.  **Click Create Web Service**.

> **Note**: The Free tier on Render "sleeps" after 15 minutes of inactivity. The first request after sleeping will take ~30 seconds to load.

## Option 3: Railway (Trial / Paid)
Railway is extremely easy but eventually requires a payment method.

1.  Go to [railway.app](https://railway.app/).
2.  Click **New Project** -> **Deploy from GitHub repo**.
3.  It will read the `Dockerfile` automatically.
4.  Go to Settings -> Generate Domain to make it accessible.
