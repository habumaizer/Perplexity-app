# Prompt Application

This project is a simplified version of Perplexity AI, designed to retrieve and process information based on user queries and provide follow-up recommendations. The application uses FastAPI for backend services, MongoDB for data storage, and Transformer models for natural language processing.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- **MongoDB**: A NoSQL database used for storing user sessions and interactions.
- **Transformers**: Hugging Face's library used for natural language processing tasks like summarization.
- **Jinja2**: A templating engine for rendering HTML.
- **Docker**: For containerizing the application to ensure consistent environments.
- **python-dotenv**: For managing environment variables.
- **better_profanity**: For filtering inappropriate content in user queries.

## Features

- **User Query Input**: Accepts user queries through a web interface.
- **Response Generation**: Processes user queries and generates responses using Perplexity AI.
- **Follow-up Recommendations**: Provides dynamic follow-up questions based on the AI's response.
- **Politeness Check**: Filters out inappropriate content in user queries.

## Setup and Running the Application

### Prerequisites

- Python 3.7+
- Docker (optional, for running in a container)
- MongoDB

> [!CAUTION]
> Application takes 1-2 Minutes to be accessible on the browser because of downloading

### Environment Variables

Create a `.env` file in the root directory of your project and add your environment variables:

PERPLEXITY_API_KEY=your-api-key
MONGODB_URI=mongodb://USERNAME:PASSWORD@localhost:27017/

### Running the Application with Docker

1. **Clone the repository**:

   ```sh
   git clone https://github.com/habumaizer/perplexity-Query-App.git
   cd perplexity-Query-App

2. **Start**:

   ```sh
   docker-compose up --build

### Running the Application Locally

1. **Clone the repository**:

   ```sh
   git clone https://github.com/habumaizer/perplexity-Query-App.git
   cd perplexity-Query-App


2. **Start MongoDB**:

   ```sh
   docker-compose -f docker-compose-mongo.yml up -d

3. **Install dependencies**:

   ```sh
   pip3 install -r requirements.txt

4. **Run the FastAPI application**:

   ```sh
   uvicorn main:app --reload
   Open your browser and go to http://127.0.0.1:8000/