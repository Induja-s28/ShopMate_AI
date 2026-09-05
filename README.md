# 🛍️ ShopMate AI

**ShopMate AI** is an AI-powered shopping assistant developed for the **Razorpay AI Builder Internship 2026 – Track 1: AI Growth & Agentic Commerce**.

It helps users discover suitable products based on their category, budget, and personal requirements, compare products using AI, and manage a smart shopping cart.

## 🚀 Features

- 🤖 AI-powered personalized product recommendations
- 💰 Category and budget-based product filtering
- ⚖️ AI Product Comparison
- 🛒 Smart Shopping Cart
- 🔢 Quantity management
- 💵 Automatic subtotal and total calculation
- 📋 Order Summary
- ✅ Demo Checkout Flow
- 🎯 Preference-based shopping assistance

## 🧠 How It Works

1. User selects a product category.
<<<<<<< HEAD
2. User sets their maximum budget.
3. User describes their requirements.
4. ShopMate AI filters matching products.
5. Groq-powered AI analyzes the available products and recommends suitable options.
6. Users can compare two products based on their priorities.
7. Selected products can be added to the smart cart.
=======
2. User sets the maximum budget.
3. User describes their requirements.
4. ShopMate AI filters matching products.
5. AI analyzes the available products and provides personalized recommendations.
6. Users can compare two products based on their priorities.
7. Selected products can be added to the shopping cart.
>>>>>>> 0517301 (Add project README)
8. The app calculates quantities, subtotals, and the final order total.
9. Users can proceed through a demo checkout flow.

## 🛠️ Tech Stack

- Python
- Streamlit
- Pandas
- Groq API
- LLM: `openai/gpt-oss-20b`
- CSV Product Dataset
- Git & GitHub

## 📂 Project Structure

```text
ShopMate_AI/
├── app.py
├── products.csv
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Induja-s28/ShopMate_AI.git
cd ShopMate_AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project folder:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Run the application:

```bash
streamlit run app.py
```

## 🔐 Security

API keys and environment variables are excluded from the GitHub repository using `.gitignore`.

Never upload your actual Groq API key to GitHub.

## 🎯 Project Objective

The objective of ShopMate AI is to simplify online product discovery by combining structured product filtering with AI-generated recommendations and comparisons.

The application demonstrates an AI-assisted commerce journey:

**User Intent → Product Filtering → AI Recommendation → Product Comparison → Smart Cart → Demo Checkout**

## 🔮 Future Improvements

- Real-time product catalog integration
- Secure payment gateway integration
- User authentication
- Larger product database
- Recommendation history
- Enhanced agentic shopping workflows

## 👩‍💻 Developer

**Induja Kakarla**

GitHub: **Induja-s28**

---

⭐ Built as part of the Razorpay AI Builder Internship 2026.
