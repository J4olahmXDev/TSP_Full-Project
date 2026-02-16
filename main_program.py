import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import calculation_module as calc

# --- ตั้งค่าหน้าเว็บ ---
st.set_page_config(page_title="Logistic Route Planner", layout="wide", page_icon="🚚")

# --- CSS แต่งสวย (Enterprise Look) ---
st.markdown("""
<style>
    .stApp {background-color: #F8FAFC;}
    h1 {color: #1E293B; font-family: 'Arial', sans-serif;}
    .stButton>button {width: 100%; border-radius: 5px; font-weight: bold;}
    .css-1d391kg {padding-top: 1rem;} 
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("🚚 Enterprise Logistics Planner")
    st.caption("Operations Research Module • Route Optimization System")
with col_head2:
    st.markdown("### Status: Active 🟢")

st.divider()

# --- SIDEBAR (Controls) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Session State (ความจำของเว็บ)
    if 'cities' not in st.session_state:
        st.session_state.cities = []

    # Input Form
    with st.form("add_city_form", clear_on_submit=True):
        st.subheader("📍 Add New Node")
        name = st.text_input("Location Name", placeholder="e.g. Warehouse A")
        
        c1, c2 = st.columns(2)
        x = c1.number_input("Latitude (X)", format="%.4f", step=0.1)
        y = c2.number_input("Longitude (Y)", format="%.4f", step=0.1)
        
        submitted = st.form_submit_button("➕ Add Node")
        
        if submitted and name:
            st.session_state.cities.append({'name': name, 'x': x, 'y': y})
            st.success(f"Added: {name}")

    # ปุ่ม Reset
    st.markdown("---")
    if st.button("🗑️ Reset System", type="secondary"):
        st.session_state.cities = []
        st.rerun()

# --- MAIN LAYOUT ---
col1, col2 = st.columns([1, 2])

# Left Column: Data Table
with col1:
    st.subheader("📋 Data Points")
    if st.session_state.cities:
        df = pd.DataFrame(st.session_state.cities)
        # จัด Format ตัวเลขให้สวยงาม
        st.dataframe(
            df.style.format({"x": "{:.4f}", "y": "{:.4f}"}), 
            use_container_width=True,
            height=300
        )
        st.info(f"Total Nodes: {len(st.session_state.cities)}")
    else:
        st.info("No data added. Please use the sidebar.")

# Right Column: Visualization & Result
with col2:
    st.subheader("🗺️ Route Visualization")
    
    if len(st.session_state.cities) >= 2:
        # ปุ่มคำนวณ
        if st.button("🚀 Calculate Optimal Route", type="primary"):
            dist, path = calc.solve_tsp_nearest_neighbor(st.session_state.cities)
            
            # 1. แสดงผลลัพธ์ตัวเลข
            st.success(f"✅ Total Distance: {dist:.4f} Units")
            
            # 2. แสดงลำดับเส้นทาง (Text)
            route_str = " ➔ ".join([c['name'] for c in path])
            st.text_area("Travel Sequence:", value=route_str, disabled=True)
            
            # 3. วาดกราฟด้วย Plotly (Interactive บน iPad)
            path_x = [c['x'] for c in path]
            path_y = [c['y'] for c in path]
            path_names = [c['name'] for c in path]
            
            fig = go.Figure()

            # วาดเส้นเชื่อม (Lines)
            fig.add_trace(go.Scatter(
                x=path_x, y=path_y,
                mode='lines+markers+text',
                text=path_names,
                textposition="top center",
                line=dict(color='#2563EB', width=3, dash='solid'), # เส้นสีน้ำเงิน
                marker=dict(size=12, color='#F59E0B', line=dict(width=2, color='white')), # จุดสีส้ม
                name='Route'
            ))

            # ใส่ลูกศร (Arrows) - ใช้ Annotation เพราะ Plotly Scatter ไม่มีลูกศรในตัว
            for i in range(len(path)-1):
                fig.add_annotation(
                    x=path_x[i+1], y=path_y[i+1], # ปลายลูกศร
                    ax=path_x[i], ay=path_y[i],   # หางลูกศร
                    xref='x', yref='y', axref='x', ayref='y',
                    showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=2, arrowcolor='#2563EB',
                    opacity=0.8
                )

            # ตกแต่งกราฟ
            fig.update_layout(
                xaxis_title="Latitude (X)",
                yaxis_title="Longitude (Y)",
                template="plotly_white",
                height=500,
                margin=dict(l=20, r=20, t=30, b=20),
                hovermode="closest"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
    else:
        st.warning("⚠️ Please add at least 2 nodes to calculate.")
