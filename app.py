
import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="🎬 Film Production Dashboard",
    layout="wide",
)

# ----------------------------
# Custom Dark Theme Styling
# ----------------------------
st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background: linear-gradient(135deg, #0e1117, #1c1f26);
    }
    h1, h2, h3 {
        color: #f5c518;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Sample Data
# ----------------------------
data = {
    "Movie Title": ["Inception", "Titanic", "Avatar", "The Dark Knight", "Avengers: Endgame"],
    "Director": ["Christopher Nolan", "James Cameron", "James Cameron", "Christopher Nolan", "Anthony & Joe Russo"],
    "Genre": ["Sci-Fi", "Romance", "Sci-Fi", "Action", "Action"],
    "Budget ($M)": [160, 200, 237, 185, 356],
    "Revenue ($M)": [836, 2200, 2923, 1006, 2797],
}

df = pd.DataFrame(data)

# ROI Calculation
df["ROI (%)"] = ((df["Revenue ($M)"] - df["Budget ($M)"]) / df["Budget ($M)"]) * 100

# ----------------------------
# Sidebar Inputs
# ----------------------------
st.sidebar.header("🎥 Add New Movie")

title = st.sidebar.text_input("Movie Title")
director = st.sidebar.text_input("Director")
genre = st.sidebar.selectbox("Genre", ["Action", "Drama", "Sci-Fi", "Comedy", "Romance", "Horror"])
budget = st.sidebar.number_input("Budget ($M)", min_value=1.0)
revenue = st.sidebar.number_input("Revenue ($M)", min_value=0.0)

if st.sidebar.button("➕ Add Movie"):
    if title and director:
        new_row = {
            "Movie Title": title,
            "Director": director,
            "Genre": genre,
            "Budget ($M)": budget,
            "Revenue ($M)": revenue,
            "ROI (%)": ((revenue - budget) / budget) * 100 if budget > 0 else 0
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        st.sidebar.success("Movie added successfully! 🎉")
    else:
        st.sidebar.error("Please fill all required fields!")

# ----------------------------
# Main Title
# ----------------------------
st.title("🎬 Film Production Dashboard")
st.markdown("Analyze movie performance, budgets, and profitability 🍿")

# ----------------------------
# Data Table
# ----------------------------
st.subheader("📊 Movie Data Table")
st.dataframe(df, use_container_width=True)

# ----------------------------
# Bar Chart (Budget vs Revenue)
# ----------------------------
st.subheader("📈 Budget vs Revenue Comparison")

bar_fig = px.bar(
    df,
    x="Movie Title",
    y=["Budget ($M)", "Revenue ($M)"],
    barmode="group",
    template="plotly_dark",
    title="Budget vs Revenue"
)

st.plotly_chart(bar_fig, use_container_width=True)

# ----------------------------
# Pie Chart (Genre Distribution)
# ----------------------------
st.subheader("🎭 Genre Distribution")

genre_count = df["Genre"].value_counts().reset_index()
genre_count.columns = ["Genre", "Count"]

pie_fig = px.pie(
    genre_count,
    names="Genre",
    values="Count",
    template="plotly_dark",
    title="Genre Share"
)

st.plotly_chart(pie_fig, use_container_width=True)

# ----------------------------
# ROI Highlight Section
# ----------------------------
st.subheader("💰 ROI Insights")

top_movie = df.loc[df["ROI (%)"].idxmax()]

st.success(
    f"🏆 Highest ROI: **{top_movie['Movie Title']}** "
    f"({top_movie['ROI (%)']:.2f}%)"
)

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown("✨ Built with Streamlit & Plotly | Cinematic Dashboard Experience 🎬")
