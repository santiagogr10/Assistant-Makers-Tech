# Makers Tech ChatBot

## Project Overview
Makers Tech ChatBot is a web application designed to interact with an e-commerce chatbot that provides real-time product information, including inventory checks, product recommendations, and more. The backend is built with Flask, while the frontend is powered by Streamlit for an interactive and user-friendly experience.

## Features
- **ChatBot Interaction**: Users can interact with the chatbot to query product availability, stock levels, and more.
- **Personalized Product Recommendations**: Based on user interaction history, the chatbot will provide personalized product suggestions.
- **Admin Dashboard**: Admins can access real-time product stock data, view stock levels in graphical representations, and manage product information.
- **Real-time Stock Monitoring**: Track inventory levels and receive low stock alerts.
- **Multi-user Support**: Different user roles with personalized experiences.

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
- Git (For version control)

### Steps to Set Up the Project

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/santiagogr10/Assistant-Makers-Tech.git
   cd Assistant-Makers-Tech
   ```

2. **Create a Virtual Environment**:
   
   For Windows:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
   
   For macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**:
   - Create a `.env` file in the root directory
   - Add your DeepSeek API key:
     ```
     DEEPSEEK_API_KEY=your_api_key_here
     ```

5. **Start the Backend**:
   
   For Windows:
   ```bash
   flask --app run.py run
   ```
   
   For macOS/Linux:
   ```bash
   export FLASK_APP=run.py
   flask run
   ```

6. **Start the Frontend**:
   ```bash
   cd frontend
   streamlit run app.py
   ```

## Project Structure
```
Assistant-Makers-Tech/
├── backend/
│   ├── __init__.py
│   ├── deepseek_client.py
│   ├── deepseek_integration.py
│   ├── inventory_routes.py
│   └── database_reader.py
├── frontend/
│   ├── app.py
│   └── chatbot_ui.py
├── .env
├── .gitignore
├── requirements.txt
└── run.py
```

## Usage
1. Access the application at `http://localhost:8501`
2. Log in with your user ID
3. Start chatting with the AI assistant
4. Access the admin dashboard for inventory management


## License
This project is licensed under the MIT License - see the LICENSE file for details.
