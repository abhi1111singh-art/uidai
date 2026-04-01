"""
🇮🇳 AADHAAR SYSTEM INTELLIGENCE DASHBOARD 🇮🇳
UIDAI Hackathon 2025 - Premium Submission
Theme: Aadhaar Card Colors (Orange #FF6B35, Blue #004E89, White, Saffron)
Design Philosophy: Government + Modern + Data-Driven
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION - AADHAAR THEME
# ============================================================================
st.set_page_config(
    page_title="Aadhaar Intelligence System",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM CSS - AADHAAR CARD INSPIRED DESIGN
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --primary-blue: #0B3C5D;
    --secondary-blue: #1F6AE1;
    --accent-saffron: #F4A261;
    --success-green: #2A9D8F;
    --warning-amber: #E9C46A;
    --danger-red: #E76F51;
    --bg-light: #F5F7FA;
    --card-bg: #FFFFFF;
    --text-dark: #1F2937;
    --text-muted: #6B7280;
}

/* App Base */
.stApp {
    background-color: var(--bg-light);
    font-family: 'Inter', sans-serif;
    color: var(--text-dark);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B3C5D 0%, #092C44 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%);
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.06);
    border-left: 6px solid var(--accent-saffron);
    text-align: center;
}
.main-title {
    font-size: 3rem;
    font-weight: 700;
    color: var(--primary-blue);
}
.main-subtitle {
    font-size: 1.2rem;
    color: var(--text-muted);
}
.tagline {
    font-size: 0.95rem;
    color: var(--secondary-blue);
}

/* Metric Cards */
.metric-card {
    background: var(--card-bg);
    border-radius: 14px;
    padding: 1.6rem;
    box-shadow: 0 6px 20px rgba(0,0,0,0.06);
    border-left: 4px solid var(--secondary-blue);
    transition: all 0.25s ease;
}
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.10);
}
.metric-value {
    font-size: 2.3rem;
    font-weight: 700;
    color: var(--primary-blue);
}
.metric-label {
    font-size: 0.8rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Section Headers */
.section-header {
    background: linear-gradient(90deg, var(--primary-blue), var(--secondary-blue));
    color: white;
    padding: 1rem 1.6rem;
    border-radius: 12px;
    font-size: 1.4rem;
    font-weight: 600;
    margin: 2.2rem 0 1.2rem 0;
}

/* Info Boxes */
.info-box {
    background: #FFFFFF;
    border-left: 4px solid var(--secondary-blue);
    padding: 1.2rem;
    border-radius: 10px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}
.success-box {
    background: #ECFDF5;
    border-left: 4px solid var(--success-green);
}
.warning-box {
    background: #FFFBEB;
    border-left: 4px solid var(--warning-amber);
}
.critical-box {
    background: #FEF2F2;
    border-left: 4px solid var(--danger-red);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, var(--secondary-blue), #3B82F6);
    border-radius: 10px;
    padding: 0.7rem 1.8rem;
    font-weight: 600;
    border: none;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #2563EB, var(--secondary-blue));
}

/* Tables */
.dataframe th {
    background-color: var(--primary-blue) !important;
    color: white !important;
}
.dataframe tr:hover {
    background-color: #F1F5F9 !important;
}

/* Footer */
.footer {
    background: #0B3C5D;
    color: #E5E7EB;
    padding: 2.5rem;
    border-radius: 14px;
    margin-top: 3rem;
    text-align: center;
}

/* Hide Streamlit Branding */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# DATA LOADING FUNCTION
# ============================================================================
@st.cache_data
def load_data():
    """Load and process Aadhaar data"""
    try:
        df = pd.read_csv('aadhaar_master_dataset.csv')
        return df
    except FileNotFoundError:
        st.error("⚠️ Data file not found! Please upload '1768656754929_aadhaar_master_dataset.csv'")
        st.stop()

@st.cache_data
def calculate_metrics(df):
    """Calculate all novel metrics"""
    state_metrics = df.groupby('state').agg({
        'Total_Enrolment': 'sum',
        'Bio_Updates': 'sum',
        'Demo_Updates': 'sum',
        'Enrol_0_5': 'sum',
        'Enrol_5_17': 'sum',
        'Enrol_18_plus': 'sum',
        'Biometric_Update_Rate': 'mean'
    }).reset_index()
    
    # Novel Metrics
    state_metrics['EQI'] = (1 - (state_metrics['Bio_Updates'] / state_metrics['Total_Enrolment'])).clip(lower=0)
    state_metrics['Demo_Update_Rate'] = state_metrics['Demo_Updates'] / state_metrics['Total_Enrolment']
    state_metrics['Friction_Index'] = (state_metrics['Bio_Updates'] + state_metrics['Demo_Updates']) / state_metrics['Total_Enrolment']
    state_metrics['Child_Enrolment'] = state_metrics['Enrol_0_5'] + state_metrics['Enrol_5_17']
    state_metrics['Child_Ratio'] = state_metrics['Child_Enrolment'] / (state_metrics['Child_Enrolment'] + state_metrics['Enrol_18_plus'])
    
    # Health Score (0-100)
    quality_score = state_metrics['EQI'] * 100
    accessibility_score = (1 - state_metrics['Friction_Index'].clip(upper=1)) * 100
    state_metrics['Health_Score'] = (quality_score * 0.6) + (accessibility_score * 0.4)
    
    return state_metrics.sort_values('Health_Score', ascending=False).reset_index(drop=True)

@st.cache_data
def detect_anomalies(df):
    """Detect statistical anomalies"""
    bio_rates = df[df['Biometric_Update_Rate'] > 0]['Biometric_Update_Rate']
    mean_rate = bio_rates.mean()
    std_rate = bio_rates.std()
    
    df['Z_Score'] = (df['Biometric_Update_Rate'] - mean_rate) / std_rate
    anomalies = df[(abs(df['Z_Score']) > 2.5) & (df['Total_Enrolment'] > 1000)].copy()
    anomalies['Severity'] = anomalies['Z_Score'].abs().apply(lambda x: 'Critical' if x > 3 else 'Warning')
    
    return anomalies.sort_values('Z_Score', ascending=False)

# ============================================================================
# LOAD DATA
# ============================================================================
df = load_data()
state_metrics = calculate_metrics(df)
anomalies = detect_anomalies(df)

# ============================================================================
# HEADER SECTION - NATIONAL PRIDE
# ============================================================================
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🇮🇳 Aadhaar System Intelligence Engine</h1>
    <p class="main-subtitle">Advanced Analytics for India's Digital Identity Infrastructure</p>
    <p class="tagline">"Transforming Data into Actionable Governance" | UIDAI Hackathon 2025</p>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR - NAVIGATION & FILTERS
# ============================================================================
with st.sidebar:
    st.markdown("### 🎯 Navigation")
    page = st.radio(
        "Select View:",
        ["🏠 Executive Dashboard", "📊 Deep Analytics", "🎯 Recommendations", "🚨 Anomaly Detection", "📥 Export & Reports"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 🔧 Filters")
    selected_states = st.multiselect("Select States:", options=df['state'].unique(), default=df['state'].unique()[:5])
    
    st.markdown("---")
    st.markdown("### 📖 About")
    st.markdown("""
    **Novel Metrics:**
    - **EQI**: Enrolment Quality Index
    - **Friction Index**: Citizen Burden Score
    - **Health Score**: System Performance (0-100)
    
    **Data Coverage:**
    - {} States
    - {} Records
    - {:.0f}-{:.0f} Timeline
    """.format(df['state'].nunique(), len(df), df['Year'].min(), df['Year'].max()))

# ============================================================================
# PAGE 1: EXECUTIVE DASHBOARD
# ============================================================================
if page == "🏠 Executive Dashboard":
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">🏛️ States Analyzed</p>
            <h2 class="metric-value">{df['state'].nunique()}</h2>
            <p class="metric-delta" style="color: #138808;">✓ Complete Coverage</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_health = state_metrics['Health_Score'].mean()
        health_color = "#138808" if avg_health >= 70 else "#F59E0B" if avg_health >= 50 else "#DC2626"
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">💯 Avg Health Score</p>
            <h2 class="metric-value" style="color: {health_color};">{avg_health:.1f}</h2>
            <p class="metric-delta">National Average</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        critical_count = len(state_metrics[state_metrics['Health_Score'] < 50])
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">⚠️ Critical States</p>
            <h2 class="metric-value" style="color: #DC2626;">{critical_count}</h2>
            <p class="metric-delta">Need Urgent Action</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-label">🔍 Anomalies</p>
            <h2 class="metric-value" style="color: #FF6B35;">{len(anomalies)}</h2>
            <p class="metric-delta">Detected Issues</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">🗺️ National Health Map</div>', unsafe_allow_html=True)
    
    # India Map Visualization
    fig_map = px.choropleth(
        state_metrics,
        locations='state',
        locationmode='country names',
        color='Health_Score',
        hover_data=['EQI', 'Friction_Index', 'Total_Enrolment'],
        color_continuous_scale=['#DC2626', '#F59E0B', '#138808'],
        range_color=[0, 100],
        title='System Health Score by State'
    )
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_layout(
        height=500,
        font=dict(family="Noto Sans"),
        title_font_size=20,
        title_font_color='#004E89'
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Top & Bottom Performers
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">🏆 Top 5 Performers</div>', unsafe_allow_html=True)
        top5 = state_metrics.head(5)[['state', 'Health_Score', 'EQI', 'Friction_Index']]
        
        fig_top = go.Figure(go.Bar(
            x=top5['Health_Score'],
            y=top5['state'],
            orientation='h',
            marker=dict(
                color=top5['Health_Score'],
                colorscale=[[0, '#138808'], [1, '#0066AA']],
                line=dict(color='#004E89', width=2)
            ),
            text=top5['Health_Score'].round(1),
            textposition='outside'
        ))
        fig_top.update_layout(
            height=300,
            xaxis_title="Health Score",
            showlegend=False,
            font=dict(family="Noto Sans", size=12)
        )
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">⚠️ Bottom 5 States</div>', unsafe_allow_html=True)
        bottom5 = state_metrics.tail(5)[['state', 'Health_Score', 'EQI', 'Friction_Index']]
        
        fig_bottom = go.Figure(go.Bar(
            x=bottom5['Health_Score'],
            y=bottom5['state'],
            orientation='h',
            marker=dict(
                color=bottom5['Health_Score'],
                colorscale=[[0, '#DC2626'], [1, '#F59E0B']],
                line=dict(color='#004E89', width=2)
            ),
            text=bottom5['Health_Score'].round(1),
            textposition='outside'
        ))
        fig_bottom.update_layout(
            height=300,
            xaxis_title="Health Score",
            showlegend=False,
            font=dict(family="Noto Sans", size=12)
        )
        st.plotly_chart(fig_bottom, use_container_width=True)
    
    # Key Insights Box
    st.markdown(f"""
    <div class="info-box">
        <h3 style="color: #004E89; margin-top: 0;">🎯 Key Insights</h3>
        <ul>
            <li><strong>{state_metrics.iloc[0]['state']}</strong> leads with Health Score of <strong>{state_metrics.iloc[0]['Health_Score']:.1f}</strong></li>
            <li><strong>{critical_count} states</strong> require immediate intervention (Health Score < 50)</li>
            <li>National average EQI: <strong>{state_metrics['EQI'].mean():.3f}</strong></li>
            <li><strong>{len(anomalies)} anomalies</strong> detected across {anomalies['state'].nunique()} states</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE 2: DEEP ANALYTICS
# ============================================================================
elif page == "📊 Deep Analytics":
    
    st.markdown('<div class="section-header">📈 Advanced Metric Analysis</div>', unsafe_allow_html=True)
    
    # EQI vs Friction Scatter
    fig_scatter = px.scatter(
        state_metrics,
        x='EQI',
        y='Friction_Index',
        size='Total_Enrolment',
        color='Health_Score',
        hover_data=['state'],
        color_continuous_scale=['#DC2626', '#F59E0B', '#138808'],
        title='Enrolment Quality Index vs Friction Index',
        labels={'EQI': 'Enrolment Quality Index', 'Friction_Index': 'Friction Index'}
    )
    fig_scatter.update_layout(
        height=500,
        font=dict(family="Noto Sans", size=14),
        title_font_size=20,
        title_font_color='#004E89'
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Time Series Analysis
    st.markdown('<div class="section-header">📅 Time-Series Trends</div>', unsafe_allow_html=True)
    
    df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(day=1))
    monthly_trends = df.groupby('Date').agg({
        'Total_Enrolment': 'sum',
        'Bio_Updates': 'sum',
        'Demo_Updates': 'sum'
    }).reset_index()
    
    fig_trends = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Total Enrolments Over Time', 'Update Trends'),
        vertical_spacing=0.15
    )
    
    fig_trends.add_trace(
        go.Scatter(x=monthly_trends['Date'], y=monthly_trends['Total_Enrolment'],
                  mode='lines+markers', name='Enrolments',
                  line=dict(color='#004E89', width=3)),
        row=1, col=1
    )
    
    fig_trends.add_trace(
        go.Scatter(x=monthly_trends['Date'], y=monthly_trends['Bio_Updates'],
                  mode='lines+markers', name='Bio Updates',
                  line=dict(color='#FF6B35', width=2)),
        row=2, col=1
    )
    
    fig_trends.add_trace(
        go.Scatter(x=monthly_trends['Date'], y=monthly_trends['Demo_Updates'],
                  mode='lines+markers', name='Demo Updates',
                  line=dict(color='#138808', width=2)),
        row=2, col=1
    )
    
    fig_trends.update_layout(
        height=600,
        font=dict(family="Noto Sans"),
        showlegend=True
    )
    st.plotly_chart(fig_trends, use_container_width=True)
    
    # State Comparison Table
    st.markdown('<div class="section-header">📋 Complete State Rankings</div>', unsafe_allow_html=True)
    
    display_df = state_metrics[['state', 'Health_Score', 'EQI', 'Friction_Index', 'Child_Ratio', 'Total_Enrolment']].copy()
    display_df.columns = ['State', 'Health Score', 'EQI', 'Friction Index', 'Child Ratio', 'Total Enrolments']
    display_df['Health Score'] = display_df['Health Score'].round(1)
    display_df['EQI'] = display_df['EQI'].round(3)
    display_df['Friction Index'] = display_df['Friction Index'].round(3)
    display_df['Child Ratio'] = display_df['Child Ratio'].round(3)
    
    st.dataframe(display_df, use_container_width=True, height=400)

# ============================================================================
# PAGE 3: RECOMMENDATIONS
# ============================================================================
elif page == "🎯 Recommendations":
    
    st.markdown('<div class="section-header">🎯 Automated Recommendations Engine</div>', unsafe_allow_html=True)
    
    recommendations = []
    
    for idx, row in state_metrics.iterrows():
        if row['EQI'] < 0.7:
            recommendations.append({
                'State': row['state'],
                'Priority': 'HIGH',
                'Category': 'Quality',
                'Action': 'Operator Retraining',
                'Impact': 'Reduce updates by 20-30%',
                'Cost': '₹2-5L',
                'Timeline': '3 months'
            })
        
        if row['Friction_Index'] > 0.3:
            recommendations.append({
                'State': row['state'],
                'Priority': 'CRITICAL',
                'Category': 'Access',
                'Action': 'Mobile Update Camps',
                'Impact': 'Serve 50,000+ citizens',
                'Cost': '₹10-15L',
                'Timeline': 'Immediate'
            })
        
        if row['Health_Score'] < 50:
            recommendations.append({
                'State': row['state'],
                'Priority': 'CRITICAL',
                'Category': 'Infrastructure',
                'Action': 'System Overhaul',
                'Impact': '40%+ improvement',
                'Cost': '₹20-50L',
                'Timeline': '6 months'
            })
    
    rec_df = pd.DataFrame(recommendations)
    
    # Priority Distribution
    col1, col2, col3 = st.columns(3)
    
    critical = len(rec_df[rec_df['Priority'] == 'CRITICAL'])
    high = len(rec_df[rec_df['Priority'] == 'HIGH'])
    
    with col1:
        st.markdown(f"""
        <div class="critical-box">
            <h2 style="color: #DC2626; margin: 0;">{critical}</h2>
            <p style="margin: 0;">Critical Priority</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="warning-box">
            <h2 style="color: #F59E0B; margin: 0;">{high}</h2>
            <p style="margin: 0;">High Priority</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_cost = (critical * 25) + (high * 3.5)
        st.markdown(f"""
        <div class="info-box">
            <h2 style="color: #004E89; margin: 0;">₹{total_cost:.0f}L</h2>
            <p style="margin: 0;">Total Investment</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Filter
    priority_filter = st.multiselect("Filter by Priority:", options=['CRITICAL', 'HIGH'], default=['CRITICAL', 'HIGH'])
    filtered_recs = rec_df[rec_df['Priority'].isin(priority_filter)]
    
    st.dataframe(filtered_recs, use_container_width=True, height=400)
    
    # Download Button
    csv = filtered_recs.to_csv(index=False)
    st.download_button(
        label="📥 Download Recommendations",
        data=csv,
        file_name="aadhaar_recommendations.csv",
        mime="text/csv"
    )

# ============================================================================
# PAGE 4: ANOMALY DETECTION
# ============================================================================
elif page == "🚨 Anomaly Detection":
    
    st.markdown('<div class="section-header">🔍 Statistical Anomaly Detection</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="warning-box">
            <h3 style="color: #F59E0B; margin-top: 0;">Anomalies Detected</h3>
            <h2 style="color: #004E89; margin: 0;">{len(anomalies)}</h2>
            <p>Across {anomalies['state'].nunique()} states</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        critical_anomalies = len(anomalies[anomalies['Severity'] == 'Critical'])
        st.markdown(f"""
        <div class="critical-box">
            <h3 style="color: #DC2626; margin-top: 0;">Critical Severity</h3>
            <h2 style="color: #004E89; margin: 0;">{critical_anomalies}</h2>
            <p>Require immediate attention</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Anomaly Timeline
    anomalies_sorted = anomalies.sort_values('Date')
    
    fig_anomaly = px.scatter(
        anomalies_sorted,
        x='Date',
        y='Biometric_Update_Rate',
        color='Severity',
        size='Total_Enrolment',
        hover_data=['state', 'Year', 'Month'],
        color_discrete_map={'Critical': '#DC2626', 'Warning': '#F59E0B'},
        title='Anomaly Timeline'
    )
    fig_anomaly.update_layout(
        height=400,
        font=dict(family="Noto Sans")
    )
    st.plotly_chart(fig_anomaly, use_container_width=True)
    
    # Anomaly Table
    st.markdown("### Detailed Anomaly Report")
    anomaly_display = anomalies[['state', 'Year', 'Month', 'Biometric_Update_Rate', 'Severity', 'Total_Enrolment']].copy()
    anomaly_display.columns = ['State', 'Year', 'Month', 'Update Rate', 'Severity', 'Enrolments']
    st.dataframe(anomaly_display, use_container_width=True, height=400)

# ============================================================================
# PAGE 5: EXPORT & REPORTS
# ============================================================================
elif page == "📥 Export & Reports":
    
    st.markdown('<div class="section-header">📥 Download Center</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3 style="color: #004E89; margin-top: 0;">📦 Available Exports</h3>
        <p>Download complete analysis results, visualizations, and reports</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Data Exports")
        
        # State Rankings
        rankings_csv = state_metrics.to_csv(index=False)
        st.download_button(
            label="📈 State Rankings (CSV)",
            data=rankings_csv,
            file_name="state_rankings.csv",
            mime="text/csv"
        )
        
        # Anomalies
        anomalies_csv = anomalies.to_csv(index=False)
        st.download_button(
            label="🚨 Anomalies Report (CSV)",
            data=anomalies_csv,
            file_name="anomalies_report.csv",
            mime="text/csv"
        )
    
    with col2:
        st.markdown("#### 📄 Summary Reports")
        
        # Executive Summary
        summary_text = f"""
AADHAAR SYSTEM INTELLIGENCE - EXECUTIVE SUMMARY
{'='*60}

OVERVIEW:
- Total States Analyzed: {df['state'].nunique()}
- Data Records: {len(df):,}
- Date Range: {df['Year'].min():.0f} - {df['Year'].max():.0f}

KEY METRICS:
- National Health Score: {state_metrics['Health_Score'].mean():.1f}/100
- Average EQI: {state_metrics['EQI'].mean():.3f}
- Average Friction Index: {state_metrics['Friction_Index'].mean():.3f}

TOP PERFORMER:
- State: {state_metrics.iloc[0]['state']}
- Health Score: {state_metrics.iloc[0]['Health_Score']:.1f}

CRITICAL FINDINGS:
- States Below Health Score 50: {len(state_metrics[state_metrics['Health_Score'] < 50])}
- Total Anomalies Detected: {len(anomalies)}
- Critical Recommendations: {len(rec_df[rec_df['Priority'] == 'CRITICAL'])}

INVESTMENT REQUIRED:
- Critical Interventions: ₹{(critical * 25):.0f} Lakhs
- High Priority Actions: ₹{(high * 3.5):.0f} Lakhs
- Total: ₹{(critical * 25 + high * 3.5):.0f} Lakhs

Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        st.download_button(
            label="📋 Executive Summary (TXT)",
            data=summary_text,
            file_name="executive_summary.txt",
            mime="text/plain"
        )
    
    # Methodology
    st.markdown('<div class="section-header">📖 Methodology</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-box">
        <h4 style="color: #138808; margin-top: 0;">Novel Metrics Explained</h4>
        
        <p><strong>1. Enrolment Quality Index (EQI)</strong></p>
        <code>EQI = 1 - (Biometric Updates / Total Enrolments)</code>
        <p>Measures initial enrolment quality. Higher values indicate better quality.</p>
        
        <p><strong>2. Friction Index</strong></p>
        <code>Friction = (Bio Updates + Demo Updates) / Total Enrolments</code>
        <p>Quantifies citizen burden in maintaining identity. Lower is better.</p>
        
        <p><strong>3. System Health Score</strong></p>
        <code>Health = (EQI × 60%) + ((1 - Friction) × 40%)</code>
        <p>Composite metric (0-100) combining quality and accessibility.</p>
        
        <p><strong>4. Child Enrolment Ratio</strong></p>
        <code>Ratio = Child Enrolments / Total Enrolments</code>
        <p>Demographic indicator for youth coverage tracking.</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div class="footer">
    <h3 style="margin-top: 0;">🇮🇳 Aadhaar System Intelligence Engine</h3>
    <p>UIDAI Hackathon 2025 | Unlocking Societal Trends in Aadhaar Enrolment and Updates</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        Novel Analytics • Predictive Intelligence • Actionable Recommendations
    </p>
    <p style="font-size: 0.8rem; margin-top: 1rem;">
        Built with 🧡 for India's Digital Identity Infrastructure
    </p>
</div>
""", unsafe_allow_html=True)