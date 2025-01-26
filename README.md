# Makers Tech ChatBot

## Project Overview
Makers Tech ChatBot is a web application designed to interact with an e-commerce chatbot that provides real-time product information, including inventory checks, product recommendations, and more. The backend is built with Flask, while the frontend is powered by Streamlit for an interactive and user-friendly experience.

## Features
- **ChatBot Interaction**: Users can interact with the chatbot to query product availability, stock levels, and more.
- **Personalized Product Recommendations**: Based on user interaction history, the chatbot will provide personalized product suggestions.
- **Admin Dashboard**: Admins can access real-time product stock data, view stock levels in graphical representations, and manage product information.

## Technologies Used
- **Backend**: Flask (API server)
- **Frontend**: Streamlit (User interface)
- **Database**: SQLite (Used for inventory and user data storage)
- **Data Visualization**: Plotly (For displaying stock and product data)
- **Python Libraries**:
  - requests (For making HTTP requests)
  - pandas (For handling and processing data)
  - matplotlib/plotly (For generating charts and graphs)

## Installation

### Prerequisites
Before getting started, ensure that you have the following installed:
- Python 3.7 or higher
- Pip (Python package installer)
- SQLite (For database management)

### Steps to Set Up the Project

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/santiagogr10/Assistant-Makers-Tech.git
   cd Assistant-Makers-Tech


2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Start the Backend**:
   ```bash
   flask --app run.py run

5. **Start the Frontend**
   ```bash
   cd frontend
   streamlit run app.py
