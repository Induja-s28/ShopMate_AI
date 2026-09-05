import streamlit as st
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

@st.cache_resource
def get_groq_client():
    return Groq(api_key=api_key)

@st.cache_data
def load_products():
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

    query = """
    SELECT
        name,
        category,
        price,
        rating,
        ram,
        storage,
        processor,
        battery,
        description
    FROM products
    """

    products_df = pd.read_sql(query, connection)
    connection.close()

    return products_df

products = load_products()
client = get_groq_client()
products = load_products()
st.set_page_config(
    page_title="ShopMate AI",
    page_icon="🛍️",
    layout="wide"
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("🛍️ ShopMate AI")

    st.write(
        "An AI-powered shopping assistant built for "
        "personalized recommendations and agentic commerce."
    )

    st.divider()

    st.subheader("✨ Features")

    st.write("• AI Product Recommendations")
    st.write("• Category & Budget Filtering")
    st.write("• AI Product Comparison")
    st.write("• Smart Shopping Cart")
    st.write("• Quantity & Order Summary")
    st.write("• Demo Checkout")

    st.divider()

    st.subheader("🤖 AI Model")
    st.write("Groq API")
    st.write("openai/gpt-oss-20b")

    st.divider()

    st.caption(
        "Razorpay AI Builder Internship 2026"
    )
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main-title {
    font-size: 48px;
    font-weight: 800;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #666;
    margin-bottom: 30px;
}

.product-card {
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #ddd;
    background-color: #fafafa;
    margin-bottom: 15px;
}

.price {
    font-size: 22px;
    font-weight: bold;
}

.rating {
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">🛍️ ShopMate AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your Intelligent Agentic Shopping Assistant</div>',
    unsafe_allow_html=True
)

st.write(
    "Shop smarter with AI. Select your category, budget and preferences "
    "to receive personalized product recommendations."
)
st.divider()

# -----------------------------
# Filters
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    categories = ["All"] + sorted(products["category"].unique().tolist())

    selected_category = st.selectbox(
        "📂 Select Product Category",
        categories
    )

with col2:
    max_product_price = int(products["price"].max())

    budget = st.slider(
        "💰 Maximum Budget (₹)",
        min_value=1000,
        max_value=max_product_price + 5000,
        value=max_product_price,
        step=1000
    )

# -----------------------------
# User preference
# -----------------------------
user_query = st.text_area(
    "🤖 Tell ShopMate AI what you need",
    placeholder=(
        "Example: I need a laptop for coding, college projects "
        "and good battery life."
    ),
    height=100
)

# -----------------------------
# Filter products
# -----------------------------
filtered_products = products[products["price"] <= budget]

if selected_category != "All":
    filtered_products = filtered_products[
        filtered_products["category"] == selected_category
    ]

st.write(
    f"**Available matching products: {len(filtered_products)}**"
)

# -----------------------------
# Recommendation button
# -----------------------------
if st.button(
    "✨ Find My Best Products",
    type="primary",
    use_container_width=True
):

    if user_query.strip() == "":
        st.warning("Please describe what you are looking for.")

    elif filtered_products.empty:
        st.error(
            "No products are available for the selected category and budget."
        )

    else:

        product_data = filtered_products.to_string(index=False)

        prompt = f"""
You are ShopMate AI, an intelligent agentic commerce shopping assistant.

Customer preference:
{user_query}

Selected category:
{selected_category}

Maximum budget:
₹{budget}

Available products:
{product_data}

Your task:

Recommend up to the best 3 products from ONLY the available products.

For every recommendation provide:

Product Name
Price
Rating
Why it matches the customer's requirement

Then provide:

Best Overall Choice
One short reason explaining why it is the best option.

Rules:
- Never recommend a product outside the given budget.
- Never invent products.
- Only use products from the supplied list.
- Keep the explanation simple and professional.
"""

        try:

            with st.spinner(
                "ShopMate AI is analysing the best products for you..."
            ):

                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are ShopMate AI, a helpful "
                                "AI shopping assistant."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            answer = response.choices[0].message.content

            st.success("✅ AI Recommendations Ready")

            st.markdown(answer)

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# -----------------------------
# Product catalogue
# -----------------------------
st.divider()

st.subheader("🛒 Available Products")

display_products = filtered_products.reset_index(drop=True)

if display_products.empty:

    st.info("No products available with these filters.")

else:

    for index, product in display_products.iterrows():

        with st.container(border=True):

            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                st.subheader(product["name"])
                st.write(product["description"])

            with col2:
                st.metric(
                    "Price",
                    f"₹{int(product['price']):,}"
                )

            with col3:
                st.metric(
                    "Rating",
                    f"⭐ {product['rating']}"
                )

st.divider()
# -----------------------------
# AI Product Comparison
# -----------------------------
st.divider()

st.subheader("⚖️ AI Product Comparison")

st.write(
    "Select two products and let ShopMate AI decide which one "
    "better matches your needs."
)

comparison_products = products["name"].tolist()

comp_col1, comp_col2 = st.columns(2)

with comp_col1:
    product_1 = st.selectbox(
        "Select Product 1",
        comparison_products,
        key="product_1"
    )

with comp_col2:
    product_2 = st.selectbox(
        "Select Product 2",
        comparison_products,
        index=1 if len(comparison_products) > 1 else 0,
        key="product_2"
    )

comparison_need = st.text_input(
    "What is most important to you?",
    placeholder="Example: Coding performance, battery life and value for money"
)

if st.button(
    "🤖 Compare with AI",
    use_container_width=True
):

    if product_1 == product_2:
        st.warning("Please select two different products.")

    elif comparison_need.strip() == "":
        st.warning("Please tell AI what is important to you.")

    else:
        row_1 = products[
            products["name"] == product_1
        ].iloc[0]

        row_2 = products[
            products["name"] == product_2
        ].iloc[0]

        comparison_prompt = f"""
You are ShopMate AI, an intelligent shopping assistant.

The customer wants to compare these two products.

PRODUCT 1
Name: {row_1['name']}
Category: {row_1['category']}
Price: ₹{row_1['price']}
Rating: {row_1['rating']}
RAM: {row_1['ram']}
Storage: {row_1['storage']}
Processor: {row_1['processor']}
Battery: {row_1['battery']}
Description: {row_1['description']}

PRODUCT 2
Name: {row_2['name']}
Category: {row_2['category']}
Price: ₹{row_2['price']}
Rating: {row_2['rating']}
RAM: {row_2['ram']}
Storage: {row_2['storage']}
Processor: {row_2['processor']}
Battery: {row_2['battery']}
Description: {row_2['description']}

Customer priority:
{comparison_need}

Compare ONLY using the supplied information.

Explain:
1. Price comparison
2. Rating comparison
3. Strength of Product 1
4. Strength of Product 2
5. Best Choice
6. Why it is the better choice for this customer

Keep the response simple, concise and professional.
"""

        try:
            with st.spinner(
                "AI is comparing the products..."
            ):

                comparison_response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content":
                            "You are an AI product comparison assistant."
                        },
                        {
                            "role": "user",
                            "content": comparison_prompt
                        }
                    ]
                )

            comparison_answer = (
                comparison_response.choices[0].message.content
            )

            st.success("✅ Comparison Complete")
            st.markdown(comparison_answer)

        except Exception as e:
            st.error(f"Comparison failed: {e}")
# -----------------------------
# -----------------------------
# Smart Cart & Checkout
# -----------------------------
st.divider()

st.subheader("🛒 Smart Shopping Cart")

product_names = products["name"].tolist()

selected_product = st.selectbox(
    "Choose a product to purchase",
    product_names,
    key="cart_product"
)

selected_row = products[
    products["name"] == selected_product
].iloc[0]

quantity = st.number_input(
    "Quantity",
    min_value=1,
    max_value=10,
    value=1,
    step=1
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Selected Product",
        selected_product
    )

with col2:
    st.metric(
        "Price",
        f"₹{int(selected_row['price']):,}"
    )

with col3:
    st.metric(
        "Rating",
        f"⭐ {selected_row['rating']}"
    )

if "cart" not in st.session_state:
    st.session_state.cart = []

if st.button(
    "🛒 Add to Cart",
    use_container_width=True
):

    existing_item = None

    for item in st.session_state.cart:
        if item["name"] == selected_product:
            existing_item = item
            break

    if existing_item:
        existing_item["quantity"] += quantity
    else:
        st.session_state.cart.append(
            {
                "name": selected_product,
                "price": int(selected_row["price"]),
                "quantity": quantity
            }
        )

    st.success(
        f"{selected_product} added to your cart!"
    )

if st.session_state.cart:

    st.subheader("🧾 Your Cart")

    total = 0

    for index, item in enumerate(st.session_state.cart):

        item_total = item["price"] * item["quantity"]
        total += item_total

        with st.container(border=True):

            c1, c2, c3, c4 = st.columns([4, 2, 2, 2])

            with c1:
                st.write(f"### {item['name']}")

            with c2:
                st.write(f"Price")
                st.write(f"₹{item['price']:,}")

            with c3:
                st.write("Quantity")
                st.write(item["quantity"])

            with c4:
                st.write("Subtotal")
                st.write(f"₹{item_total:,}")

            if st.button(
                "❌ Remove",
                key=f"remove_{index}",
                use_container_width=True
            ):
                st.session_state.cart.pop(index)
                st.rerun()

    st.write(f"## Total: ₹{total:,}")

    col_clear, col_checkout = st.columns(2)

    with col_clear:
        if st.button(
            "🗑️ Clear Cart",
            use_container_width=True
        ):
            st.session_state.cart = []
            st.rerun()

    with col_checkout:
        if st.button(
            "💳 Proceed to Checkout",
            type="primary",
            use_container_width=True
        ):

            st.success("🎉 Order Ready!")

            st.subheader("📦 Order Summary")

            for item in st.session_state.cart:
                st.write(
                    f"{item['name']} × {item['quantity']} "
                    f"= ₹{item['price'] * item['quantity']:,}"
                )

            st.write(f"### Final Amount: ₹{total:,}")

            st.info(
                "Demo Checkout Only — no real payment is processed. "
                "In production, this step can connect to a secure "
                "payment gateway."
            )

else:
    st.info("Your cart is currently empty.")

st.caption(
    "ShopMate AI • AI Growth & Agentic Commerce Project"
)