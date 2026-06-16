import pandas as pd
import streamlit as st
import plotly.express as px

# 1. Dashboard Theme aur Layout Design
st.set_page_config(page_title="Sakshi | Job Analytics", layout="wide")

st.title("📊 Data Analyst Job Market Insights Dashboard")
st.markdown("This interactive platform extracts real-time technology trends from corporate job postings.")

# 2. Processed Data Load Karna
df = pd.read_csv("processed_jobs.csv")

# 3. Premium KPI Metrics Cards Section
st.subheader("🎯 Key Market Performance Indicators")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div style='background-color:#1E1E2F; padding:20px; border-radius:10px; border-left: 5px solid #8884d8;'>", unsafe_allow_html=True)
    st.metric(label="Total Job Postings Scanned", value=f"{len(df)} Jobs")
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    skills = ['SQL', 'Python', 'Power_BI', 'Tableau', 'Excel']
    top_skill = max(skills, key=lambda s: df[s].sum())
    st.markdown("<div style='background-color:#1E1E2F; padding:20px; border-radius:10px; border-left: 5px solid #82ca9d;'>", unsafe_allow_html=True)
    st.metric(label="Top In-Demand Skill", value=top_skill.replace('_', ' '))
    st.markdown("</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div style='background-color:#1E1E2F; padding:20px; border-radius:10px; border-left: 5px solid #ffc658;'>", unsafe_allow_html=True)
    st.metric(label="Active Employment City Hubs", value=f"{df['Location'].nunique()} Cities")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4. Filter System inside the Dashboard
st.sidebar.header("🔍 Filter Analytics Panel")
selected_location = st.sidebar.selectbox(
    "Choose Target City Hub:", 
    ["All Locations"] + list(df['Location'].unique())
)

if selected_location != "All Locations":
    filtered_df = df[df['Location'] == selected_location]
else:
    filtered_df = df

# 5. Visual Interactive Analytics Chart Section
st.subheader(f"📈 Technology Skill Frequency Matrix ({selected_location})")

# Dynamically formatting skill data for chart layout
skills_counts = {
    "SQL": filtered_df['SQL'].sum(),
    "Python": filtered_df['Python'].sum(),
    "Power BI": filtered_df['Power_BI'].sum(),
    "Excel": filtered_df['Excel'].sum(),
    "Tableau": filtered_df['Tableau'].sum()
}

chart_data = pd.DataFrame(list(skills_counts.items()), columns=['Technical Tool', 'Job Requirement Count'])
chart_data = chart_data.sort_values(by='Job Requirement Count', ascending=False)

# Creating a high-quality interactive bar graph
fig = px.bar(chart_data, x='Technical Tool', y='Job Requirement Count', 
             color='Job Requirement Count', 
             color_continuous_scale='Turbo',
             template='plotly_dark',
             text_auto=True)

fig.update_layout(
    xaxis_title="Core Technical Skills",
    yaxis_title="Number of Corporate Postings",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    coloraxis_showscale=False
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 6. Corporate Data Preview Control Panel
st.subheader("📋 Active Corporate Openings Registry")
st.dataframe(
    filtered_df[['Job Title', 'Company Name', 'Location', 'Salary Estimate']].head(10), 
    use_container_width=True
)
