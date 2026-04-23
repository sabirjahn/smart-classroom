
# Smart Classroom Monitoring System 🎓☁️

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![Azure](https://img.shields.io/badge/Deployment-Microsoft_Azure-blue)
![AI](https://img.shields.io/badge/AI-DeepFace-orange)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-brightgreen)

A cloud-native, AI-powered web application designed to analyze student engagement, attention, and emotional states in real-time using computer vision.

## 🏗️ Architecture

Unlike traditional local scripts, this project is fully architected for the Cloud (PaaS):
- **Frontend Engine**: HTML5, JS (Uses WebRTC API to capture local webcam frames, bypassing cloud hardware limitations).
- **Backend API**: Python (Flask / Gunicorn) processes Base64 encoded video frames.
- **AI Core**: DeepFace (CNN models) extracts emotional states and face counts.
- **Infrastructure**: Containerized with Docker, automated via GitHub Actions, and hosted on Microsoft Azure Web App for Containers.
- **Security**: Routed via Cloudflare with strict HTTPS encryption.

## ✨ Key Features

- **Real-time Emotion Detection**: Analyzes facial expressions instantly via client-side WebRTC cameras.
- **Cloud-Native & Containerized**: Fully reproducible environment using Docker and `docker-compose`.
- **CI/CD Pipeline**: Automated builds and deployments to Azure via GitHub Actions.
- **Advanced Analytics**: Visualizes emotion trends and dominant classroom moods on a dynamic dashboard.
- **SQLite Database**: Lightweight, container-volume-mapped database for session persistence.

## 🚀 Getting Started (Docker - Recommended)

The easiest way to run this project is using Docker.

### Prerequisites
- [Docker](https://www.docker.com/) and Docker Compose installed on your machine.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/sabirjahn/smart-classroom.git
   cd smart-classroom
   ```

2. Build and start the container:
   ```bash
   docker-compose up --build -d
   ```

3. Access the application:
   Open your browser and navigate to `http://localhost:5000`

## 💻 Manual Local Setup (Without Docker)

If you prefer to run it without Docker:

1. Clone the repository and set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

## ☁️ Cloud Deployment (CI/CD)

This repository is configured with a fully automated CI/CD pipeline using **GitHub Actions** (`.github/workflows/deploy.yml`). 

Any push to the `main` branch automatically:
1. Builds the Docker image.
2. Pushes the updated image to **GitHub Container Registry (GHCR)**.
3. Triggers an Azure Webhook to pull the latest image and seamlessly restart the production container on Microsoft Azure.

## 📝 License

This project is licensed under the MIT License.