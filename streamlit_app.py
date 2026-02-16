import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import math

# ==========================================
# 1. ส่วนคำนวณ (LOGIC: Python แท้ๆ)
# ==========================================
def get_dist(c1, c2):
    return math.sqrt((c1['x'] - c2['x'])**2 + (c1['y'] - c2['y'])**2)

def solve_tsp_nearest_neighbor(cities):
    if not cities:
        return 0, []
    
    unvisited = cities[:]
    # เริ่มที่เมืองแรกที่ User ใส่เข้ามา
    current_city = unvisited.pop(0)
    route_path = [current_city]
    total_distance = 0

    while unvisited:
        # หาเมืองที่ใกล้ที่สุด
        nearest_city = min(unvisited, key=lambda city: get_dist(current_city, city))
        total_distance += get_dist(current_city, nearest_city)
        current_city = nearest_city
        route_path.append(current_city)
        unvisited.remove(current_city)

    # วนกลับจุดเริ่มต้น
    if len(route_path) > 1:
        total_distance += get_dist(route_path[-1], route_path[0])
        route_path.append(route_path[0])
        
    return total_distance, route_path

# ==========================================
# 2. ส่วนหน้าจอเว็บ (UI: Streamlit)
# ==========================================
st.set_page_config(page_title="Logistics Planner Pro", layout="wide", page_icon="🚚")

# --- CSS แต่งธีม Enterprise (Navy Blue) ---
st.markdown("""
<style>
    .stApp {background-color: #F8FAFC;}
    h1, h2, h3 {color: #1E3A8A; font-family: 'Arial', sans-serif;}
    .stButton>button {
        background-color: #1E3A8A; 
        color: white; 
        border-radius: 8px; 
        height: 50px; 
        font-weight: bold;
    }
    .stButton>button:hover {background-color: #172554; border-color: white;}
    div[data-testid="stMetricValue"] {font-size: 24px; color: #10B981;}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🚚 Enterprise Logistics Planner")
    st.caption("Operations Research Module • Python Based System")
with col2:
    st.success("System Active 🟢")

st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    if 'cities' not in st.session_state:
        st.session_state.cities = []

    with st.form("entry_form", clear_on_submit=True):
        st.subheader("Add New Location")
        name = st.text_input("Location Name", placeholder="e.g. Warehouse A")
        c1, c2 = st.columns(2)
        x = c1.number_input("Latitude (X)", format="%.4f", step=0.0001)
        y = c2.number_input("Longitude (Y)", format="%.4f", step=0.0001)
        
        submitted = st.form_submit_button("➕ Add Node")
        if submitted and name:
            st.session_state.cities.append({'name': name, 'x': x, 'y': y})
            st.toast(f"Added: {name}", icon="✅")

    st.markdown("---")
    if st.button("🗑️ Reset System"):
        st.session_state.cities = []
        st.rerun()

# --- MAIN AREA ---
col_left, col_right = st.columns([1, 2])

# Left: Table
with col_left:
    st.subheader("📋 Data Points")
    if st.session_state.cities:
        df = pd.DataFrame(st.session_state.cities)
        st.dataframe(
            df.style.format({"x": "{:.4f}", "y": "{:.4f}"}),
            use_container_width=True,
            height=400
        )
    else:
        st.info("Waiting for data entry...")

# Right: Visualization
with col_right:
    st.subheader("🗺️ Route Optimization Map")
    
    if len(st.session_state.cities) >= 2:
        # ปุ่มคำนวณ
        if st.button("🚀 Calculate Optimal Route", type="primary"):
            dist, path = solve_tsp_nearest_neighbor(st.session_state.cities)
            
            # แสดงผลลัพธ์
            st.success(f"✅ Total Distance: {dist:.4f} Units")
            
            route_str = " ➔ ".join([c['name'] for c in path])
            st.code(f"Sequence: {route_str}", language="text")
            
            # วาดกราฟ Plotly (Interactive บน iPad)
            path_x = [c['x'] for c in path]
            path_y = [c['y'] for c in path]
            path_names = [c['name'] for c in path]
            
            fig = go.Figure()
            
            # เส้นทาง
            fig.add_trace(go.Scatter(
                x=path_x, y=path_y,
                mode='lines+markers+text',
                text=path_names, textposition="top center",
                line=dict(color='#2563EB', width=3),
                marker=dict(size=12, color='#F59E0B', line=dict(width=2, color='white')),
                name='Route'
            ))

            # ลูกศร
            for i in range(len(path)-1):
                fig.add_annotation(
                    x=path_x[i+1], y=path_y[i+1], ax=path_x[i], ay=path_y[i],
                    xref='x', yref='y', axref='x', ayref='y',
                    showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor='#2563EB', opacity=0.8
                )

            fig.update_layout(
                xaxis_title="Latitude (X)", yaxis_title="Longitude (Y)",
                template="plotly_white", height=500,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Please add at least 2 locations to calculate.")
