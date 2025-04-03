# Streamlit App for Social Media and Mental Health Analysis

## Introduction
This project is a Streamlit-based web application that visualizes and analyzes social media's impact on mental health using the dataset from Kaggle: [Social Media and Mental Health](https://www.kaggle.com/datasets/souvikahmed071/social-media-and-mental-health). The app integrates Seaborn for data visualization and Gemini AI for insights.

## Features
- Interactive data visualization with Seaborn
- User-friendly web interface using Streamlit
- AI-generated insights with Gemini AI
- Dynamic filtering and data exploration
- Sentiment analysis (if applicable)

## Technologies Used
- **Frontend**: Streamlit
- **Backend**: Python
- **Libraries**: Pandas, NumPy, Seaborn, Matplotlib, Gemini AI SDK
- **Dataset**: Social Media and Mental Health from Kaggle

## Installation
### Prerequisites
- Python (>=3.8)
- Kaggle API (for dataset retrieval)
- Google API Key (for Gemini AI integration)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/streamlit-mental-health.git
   cd streamlit-mental-health
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up Gemini AI API key (replace `YOUR_API_KEY` with actual key):
   ```bash
   export GEMINI_API_KEY="YOUR_API_KEY"
   ```
   *(For Windows: `set GEMINI_API_KEY=YOUR_API_KEY`)*

5. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage
- Open the application in the browser.
- Select filters and visualize insights.
- Explore AI-driven analysis for mental health trends.

## Data Sources
- [Social Media and Mental Health Dataset](https://www.kaggle.com/datasets/souvikahmed071/social-media-and-mental-health)
- Ensure compliance with dataset usage policies.

