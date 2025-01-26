# 🛠️ Makers Tech ChatBot

**Makers Tech ChatBot** is a cutting-edge web application designed to enhance e-commerce experiences with an AI-powered chatbot. It delivers real-time product information, personalized recommendations, and powerful inventory management tools. The backend leverages Flask for robust API handling, while the frontend, powered by Streamlit, offers an intuitive user interface.

---

# 🌟 Features
- **💬 Seamless ChatBot Interaction**  
  Engage with the chatbot to check product availability, stock levels, and more.

- **🎯 Personalized Product Recommendations**  
  Receive tailored suggestions based on your interaction history.

- **📊 Admin Dashboard**  
  Visualize real-time stock data with interactive graphs and manage product details effortlessly.

- **📦 Real-time Stock Monitoring**  
  Stay updated on inventory levels and receive alerts for low stock.

- **👥 Multi-User Support**  
  Personalized experiences for different user roles (e.g., customers, admins).

---

# 🛠️ Technologies Used
| **Category**       | **Tools/Frameworks**                                                   |
|---------------------|------------------------------------------------------------------------|
| **Backend**         | Flask                                                                 |
| **Frontend**        | Streamlit                                                             |
| **Database**        | SQLite                                                                |
| **Data Visualization** | Plotly                                                           |
| **Python Libraries** | requests, pandas, matplotlib, plotly                                |

---

# 🚀 Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.7 or higher
- Pip (Python package installer)
- SQLite
- Git

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

📂 Project Structure
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

# 🎯 Usage
1. Access the application at `http://localhost:8501`
2. Log in with your user ID
3. Start chatting with the AI assistant
4. Access the admin dashboard for inventory management


# 📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
