import streamlit as st
import joblib
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.datasets import load_iris

# ---------------------------------------------------------
# Page Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="Iris Species Predictor",
    page_icon="🌿",
    layout="wide"
)

# ---------------------------------------------------------
# Load Model & Dataset
# ---------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load('iris_model.pkl')

@st.cache_data
def get_data():
    raw = load_iris()
    cols = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
    df = pd.DataFrame(raw.data, columns=cols)
    df['species'] = [raw.target_names[i].title() for i in raw.target]
    return df, raw.target_names, cols

model = load_model()
df, target_names, feature_cols = get_data()

# ---------------------------------------------------------
# Sidebar: User Controls
# ---------------------------------------------------------
with st.sidebar:
    st.title("🌿 Settings & Inputs")
    st.write("Tune the measurements to test the flower classifier.")
    
    st.divider()
    st.subheader("Measurements (cm)")
    
    sepal_len = st.slider("Sepal Length", 4.0, 8.0, 5.8, 0.1)
    sepal_wid = st.slider("Sepal Width", 2.0, 4.5, 3.0, 0.1)
    petal_len = st.slider("Petal Length", 1.0, 7.0, 4.3, 0.1)
    petal_wid = st.slider("Petal Width", 0.1, 2.5, 1.3, 0.1)
    
    st.divider()
    st.caption("Random Forest Model trained with scikit-learn.")

# ---------------------------------------------------------
# Main View Header
# ---------------------------------------------------------
st.title("Iris Flower Species Predictor")
st.markdown("An interactive ML dashboard to predict and compare flower dimensions.")

# ---------------------------------------------------------
# Make Prediction
# ---------------------------------------------------------
input_df = pd.DataFrame(
    [[sepal_len, sepal_wid, petal_len, petal_wid]],
    columns=feature_cols
)

prediction_idx = model.predict(input_df)[0]
predicted_species = target_names[prediction_idx].title()

probabilities = model.predict_proba(input_df)[0]
confidence = probabilities[prediction_idx] * 100

# ---------------------------------------------------------
# Results & Visualization Section
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("🎯 Prediction")
    
    # Modern Teal/Ocean Gradient Card
    st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #0ba360 0%, #3cba92 100%);
            padding: 22px;
            border-radius: 14px;
            color: white;
            text-align: center;
            margin-bottom: 20px;
        ">
            <p style="margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.9;">Predicted Species</p>
            <h2 style="margin: 6px 0; font-size: 34px; color: white;">{predicted_species}</h2>
            <p style="margin: 0; font-size: 15px; opacity: 0.95;">Confidence: <b>{confidence:.1f}%</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    # Probability Breakdown
    prob_chart_df = pd.DataFrame({
        'Species': [name.title() for name in target_names],
        'Probability': [p * 100 for p in probabilities]
    })
    
    fig_prob = px.bar(
        prob_chart_df,
        x='Probability',
        y='Species',
        orientation='h',
        text='Probability',
        color='Probability',
        color_continuous_scale='Mint',
        range_x=[0, 105],
        title="Model Probability by Class"
    )
    fig_prob.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig_prob.update_layout(height=240, margin=dict(l=10, r=20, t=35, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig_prob, use_container_width=True)

with col2:
    st.subheader("📊 Your Inputs vs Dataset Mean")
    
    clean_labels = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']
    user_values = [sepal_len, sepal_wid, petal_len, petal_wid]
    mean_values = [df[col].mean() for col in feature_cols]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Bar(
        name='Your Values',
        x=clean_labels,
        y=user_values,
        marker_color='#10b981'
    ))
    fig_radar.add_trace(go.Bar(
        name='Dataset Average',
        x=clean_labels,
        y=mean_values,
        marker_color='#64748b'
    ))
    fig_radar.update_layout(
        barmode='group',
        height=355,
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# ---------------------------------------------------------
# Species Reference Cards
# ---------------------------------------------------------
st.divider()
st.subheader("📖 Quick Species Guide")

c1, c2, c3 = st.columns(3)
with c1:
    with st.container(border=True):
        st.markdown("### 🌸 Setosa")
        st.write("Notable for having short, wide petals. Easily separated from the other two species.")
with c2:
    with st.container(border=True):
        st.markdown("### 🌺 Versicolor")
        st.write("Features intermediate petal sizes. Can sometimes share dimensions with Virginica.")
with c3:
    with st.container(border=True):
        st.markdown("### 🌻 Virginica")
        st.write("Has the longest and widest petals on average among all three species.")

# ---------------------------------------------------------
# Data Exploration Section
# ---------------------------------------------------------
st.divider()
with st.expander("🔍 Explore the Iris Training Data"):
    tab_data, tab_charts = st.tabs(["Raw Data Preview", "Feature Distributions"])
    
    with tab_data:
        st.dataframe(df, use_container_width=True, height=220)
        
    with tab_charts:
        chosen_feature = st.selectbox("Choose a dimension to inspect:", clean_labels)
        internal_col = feature_cols[clean_labels.index(chosen_feature)]
        
        fig_hist = px.histogram(
            df,
            x=internal_col,
            color="species",
            marginal="box",
            barmode="overlay",
            title=f"{chosen_feature} by Species"
        )
        fig_hist.update_layout(height=350)
        st.plotly_chart(fig_hist, use_container_width=True)
