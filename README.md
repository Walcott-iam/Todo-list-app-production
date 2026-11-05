# Containerized To-Do App with CI/CD Deployment to Azure

## Project Overview
This project demonstrates the end-to-end lifecycle of a web application. It covers local development testing, Docker containerization, automated CI/CD via GitHub Actions, and deployment to Microsoft Azure App Service.

## Architecture & Tech Stack
*   **Application:** Python (Flask) with SQLite database.
*   **Containerization:** Docker (Multi-stage build, non-root user).
*   **CI/CD:** GitHub Actions (Builds image, pushes to GHCR, deploys to Azure).
*   **Cloud Hosting:** Azure App Service (Linux Web App, Free Tier).
*   **Registry:** GitHub Container Registry (`ghcr.io`).

---

## Step-by-Step Implementation

### Phase 1: Local Testing & Development
Before containerizing, the application was tested locally to ensure the developer's code worked.
1. Created and activated a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Installed dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ran the Flask app locally on port 8000 to verify the frontend and backend connected successfully.

### Phase 2: Docker Containerization
Created a multi-stage `Dockerfile` to keep the final image lightweight and secure.
*   **Stage 1 (Builder):** Installs build tools (`gcc`), creates a virtual environment (`/opt/venv`), and installs Python dependencies.
*   **Stage 2 (Production):** Copies the completed `venv` from the builder stage, copies the application code, creates a non-root user (`appuser`), and runs Gunicorn on port 8000.
*   *Key Fix:* Used a `venv` inside the container to ensure the `gunicorn` executable had all its paths correctly mapped.

### Phase 3: Azure Infrastructure Setup
1.  **Azure App Service:** Created a Linux Web App on the Free F1 tier, configured to pull a custom Docker container.
2.  **Environment Variables:** Set `WEBSITES_PORT=8000` in Azure App Settings so Azure knows which port Gunicorn is listening on.
3.  **Authentication:** Generated an Azure Service Principal using the Azure CLI and saved the JSON credentials as a GitHub Secret (`AZURE_CREDENTIALS`).

### Phase 4: The CI/CD Pipeline (GitHub Actions)
Created a workflow (`.github/workflows/main.yml`) that automates the deployment on every push to `main`.

**Challenges Overcome in the YAML:**
*   **Permissions:** Added `packages: write` to allow GitHub Actions to push to the Container Registry.
*   **Lowercase Tag:** Added a Bash script step to force the repository name and username to lowercase (Docker requirement).
*   **Provenance:** Added `provenance: false` to fix the "unknown blob" push error.
*   **Auth:** Switched from Publish Profile (XML) to Service Principal (JSON) for reliable Azure authentication.

---

## Evidence & Screenshots

### 1. Local Application Testing
*The Flask app running locally in a virtual environment before Dockerization.*
![App running at localhost:8000](https://github.com/Walcott-iam/Todo-list-app-production/blob/main/Task61.png)

### 2. Docker Build Success
*The terminal output showing the multi-stage Docker image built successfully.*
![Terminal showing docker build complete](https://github.com/Walcott-iam/Todo-list-app-production/blob/main/task62.png)

### 3. Local Container Running
*The Docker container running in the background, serving the app on port 8000.*
*![Terminal showing docker ps](https://github.com/Walcott-iam/Todo-list-app-production/blob/main/Task63.png)

### 4. Azure web App Configuration
![GitHub Actions green checkmark](https://github.com/Walcott-iam/Todo-list-app-production/blob/main/Task64.png)

### 5. Live Azure Application
*The fully deployed To-Do app running live on Azure App Service.*
![Live Azure URL](https://github.com/Walcott-iam/Todo-list-app-production/blob/main/Task65.png)

---

## How to Run Locally
```bash
# Build the image
docker build -t todo-capstone-app .

# Run the container
docker run -d -p 8000:8000 --name my-todo-app todo-capstone-app
```
Visit `http://localhost:8000` in your browser.
```
