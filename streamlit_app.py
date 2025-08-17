import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import subprocess
import os
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Set page config
st.set_page_config(
    page_title="Hybrid Plant Simulation Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .config-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def load_config(config_file):
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {config_file}: {str(e)}")
        return None

def save_config(config_data, config_file):
    """Save configuration to JSON file"""
    try:
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving {config_file}: {str(e)}")
        return False

def run_simulation():
    """Run the hybrid plant simulation"""
    try:
        result = subprocess.run([sys.executable, "run_test_4.py"], 
                              capture_output=True, text=True, cwd=os.getcwd())
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def display_energy_flow_diagram():
    """Display the energy flow diagram"""
    diagram_path = "input_test_4/plots/energy_flow_diagram.png"
    if os.path.exists(diagram_path):
        # Add expander for better viewing
        with st.expander("🔍 Click to expand Energy Flow Diagram", expanded=True):
            st.image(diagram_path, caption="Energy Flow Diagram", use_container_width=True)
            
            # Add download button
            with open(diagram_path, "rb") as f:
                st.download_button(
                    label="📥 Download Energy Flow Diagram",
                    data=f.read(),
                    file_name="energy_flow_diagram.png",
                    mime="image/png"
                )
    else:
        st.warning("Energy flow diagram not found. Please run the simulation first.")

def display_system_summary():
    """Display system summary metrics"""
    summary_path = "input_test_4/plots/system_summary.png"
    if os.path.exists(summary_path):
        with st.expander("🔍 Click to expand System Summary", expanded=True):
            st.image(summary_path, caption="System Summary", use_container_width=True)
            
            with open(summary_path, "rb") as f:
                st.download_button(
                    label="📥 Download System Summary",
                    data=f.read(),
                    file_name="system_summary.png",
                    mime="image/png"
                )
    else:
        st.warning("System summary not found. Please run the simulation first.")

def display_economic_analysis():
    """Display economic analysis plots"""
    analysis_path = "input_test_4/plots/economic_analysis.png"
    if os.path.exists(analysis_path):
        with st.expander("🔍 Click to expand Economic Analysis", expanded=True):
            st.image(analysis_path, caption="Economic Analysis", use_container_width=True)
            
            with open(analysis_path, "rb") as f:
                st.download_button(
                    label="📥 Download Economic Analysis",
                    data=f.read(),
                    file_name="economic_analysis.png",
                    mime="image/png"
                )
    else:
        st.warning("Economic analysis not found. Please run the simulation first.")

def display_load_profiles():
    """Display load profile plots"""
    load_path = "input_test_4/plots/load_profiles.png"
    if os.path.exists(load_path):
        with st.expander("🔍 Click to expand Load Profiles", expanded=True):
            st.image(load_path, caption="Load Profiles", use_container_width=True)
            
            with open(load_path, "rb") as f:
                st.download_button(
                    label="📥 Download Load Profiles",
                    data=f.read(),
                    file_name="load_profiles.png",
                    mime="image/png"
                )
    else:
        st.warning("Load profiles not found. Please run the simulation first.")

def display_production_profiles():
    """Display production profile plots"""
    prod_path = "input_test_4/plots/production_profiles.png"
    if os.path.exists(prod_path):
        with st.expander("🔍 Click to expand Production Profiles", expanded=True):
            st.image(prod_path, caption="Production Profiles", use_container_width=True)
            
            with open(prod_path, "rb") as f:
                st.download_button(
                    label="📥 Download Production Profiles",
                    data=f.read(),
                    file_name="production_profiles.png",
                    mime="image/png"
                )
    else:
        st.warning("Production profiles not found. Please run the simulation first.")

def display_pdf_report():
    """Display PDF report inline"""
    pdf_path = "input_test_4/plots/hybrid_plant_simulation_report.pdf"
    if os.path.exists(pdf_path):
        # File info
        file_size = os.path.getsize(pdf_path) / (1024 * 1024)  # Convert to MB
        st.info(f"📄 PDF Report Size: {file_size:.2f} MB")
        
        # Download button
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name="hybrid_plant_simulation_report.pdf",
            mime="application/pdf"
        )
        
        st.write("**📖 PDF Report Preview:**")
        st.write("The PDF report contains comprehensive analysis of the hybrid plant simulation including:")
        st.write("- Executive summary and key findings")
        st.write("- Detailed economic analysis")
        st.write("- System performance metrics")
        st.write("- Technical specifications")
        st.write("- Recommendations and conclusions")
        
        # Display PDF inline using base64 encoding
        import base64
        pdf_base64 = base64.b64encode(pdf_bytes).decode()
        
        # Create a more responsive PDF viewer
        pdf_html = f"""
        <div style="width: 100%; height: 800px; border: 1px solid #ddd; border-radius: 5px; overflow: hidden;">
            <iframe 
                src="data:application/pdf;base64,{pdf_base64}" 
                width="100%" 
                height="100%" 
                style="border: none;"
                title="Hybrid Plant Simulation Report">
            </iframe>
        </div>
        """
        st.markdown(pdf_html, unsafe_allow_html=True)
        
        st.write("💡 **Tip**: You can zoom in/out and scroll within the PDF viewer above, or download the full report using the button above.")
        
    else:
        st.warning("PDF report not found. Please run the simulation first.")

def display_image_gallery():
    """Display all images in a gallery format"""
    plots_dir = Path("input_test_4/plots")
    if not plots_dir.exists():
        st.warning("No plots directory found. Please run the simulation first.")
        return
    
    # Get all PNG files
    image_files = list(plots_dir.glob("*.png"))
    if not image_files:
        st.warning("No image files found. Please run the simulation first.")
        return
    
    st.subheader("🖼️ Image Gallery")
    st.write("View all simulation results in one place:")
    
    # Create columns for gallery layout
    cols = st.columns(2)
    
    for i, image_file in enumerate(image_files):
        col_idx = i % 2
        with cols[col_idx]:
            st.write(f"**{image_file.stem.replace('_', ' ').title()}**")
            st.image(str(image_file), use_container_width=True)
            
            # Add download button for each image
            with open(image_file, "rb") as f:
                st.download_button(
                    label=f"📥 Download {image_file.stem}",
                    data=f.read(),
                    file_name=image_file.name,
                    mime="image/png",
                    key=f"download_{image_file.stem}"
                )
            st.divider()

def display_csv_outputs():
    """Display all CSV output files with interactive viewing"""
    outputs_dir = Path("input_test_4/outputs")
    if not outputs_dir.exists():
        st.warning("No outputs directory found. Please run the simulation first.")
        return
    
    st.subheader("📊 CSV Output Files")
    st.write("View and download all generated CSV files:")
    
    # Create tabs for different output categories
    tab1, tab2, tab3 = st.tabs(["Intermediate Outputs", "Final Outputs", "Reconciliation Reports"])
    
    with tab1:
        st.write("**🔄 Intermediate Outputs** - Raw data processing and summary statistics")
        intermediate_dir = outputs_dir / "intermediate"
        if intermediate_dir.exists():
            csv_files = list(intermediate_dir.glob("*.csv"))
            if csv_files:
                for csv_file in csv_files:
                    with st.expander(f"📄 {csv_file.stem.replace('_', ' ').title()}", expanded=False):
                        try:
                            # Load and display CSV data
                            df = pd.read_csv(csv_file)
                            
                            # Show file info
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Rows", len(df))
                            with col2:
                                st.metric("Columns", len(df.columns))
                            with col3:
                                file_size = csv_file.stat().st_size / 1024  # KB
                                st.metric("Size", f"{file_size:.1f} KB")
                            
                            # Display data
                            st.dataframe(df, use_container_width=True)
                            
                            # Download button
                            with open(csv_file, "rb") as f:
                                st.download_button(
                                    label=f"📥 Download {csv_file.name}",
                                    data=f.read(),
                                    file_name=csv_file.name,
                                    mime="text/csv",
                                    key=f"download_intermediate_{csv_file.stem}"
                                )
                        except Exception as e:
                            st.error(f"Error loading {csv_file.name}: {str(e)}")
            else:
                st.warning("No intermediate CSV files found.")
        else:
            st.warning("Intermediate outputs directory not found.")
    
    with tab2:
        st.write("**📈 Final Outputs** - Processed results and comprehensive analysis")
        final_dir = outputs_dir / "final"
        if final_dir.exists():
            csv_files = list(final_dir.glob("*.csv"))
            if csv_files:
                for csv_file in csv_files:
                    with st.expander(f"📄 {csv_file.stem.replace('_', ' ').title()}", expanded=False):
                        try:
                            # Load and display CSV data
                            df = pd.read_csv(csv_file)
                            
                            # Show file info
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Rows", len(df))
                            with col2:
                                st.metric("Columns", len(df.columns))
                            with col3:
                                file_size = csv_file.stat().st_size / 1024  # KB
                                st.metric("Size", f"{file_size:.1f} KB")
                            
                            # Display data
                            st.dataframe(df, use_container_width=True)
                            
                            # Download button
                            with open(csv_file, "rb") as f:
                                st.download_button(
                                    label=f"📥 Download {csv_file.name}",
                                    data=f.read(),
                                    file_name=csv_file.name,
                                    mime="text/csv",
                                    key=f"download_final_{csv_file.stem}"
                                )
                        except Exception as e:
                            st.error(f"Error loading {csv_file.name}: {str(e)}")
            else:
                st.warning("No final CSV files found.")
        else:
            st.warning("Final outputs directory not found.")
    
    with tab3:
        st.write("**🔍 Reconciliation Reports** - Data validation and consistency checks")
        reconciliation_dir = outputs_dir / "reconciliation"
        if reconciliation_dir.exists():
            csv_files = list(reconciliation_dir.glob("*.csv"))
            if csv_files:
                for csv_file in csv_files:
                    with st.expander(f"📄 {csv_file.stem.replace('_', ' ').title()}", expanded=False):
                        try:
                            # Load and display CSV data
                            df = pd.read_csv(csv_file)
                            
                            # Show file info
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Rows", len(df))
                            with col2:
                                st.metric("Columns", len(df.columns))
                            with col3:
                                file_size = csv_file.stat().st_size / 1024  # KB
                                st.metric("Size", f"{file_size:.1f} KB")
                            
                            # Special handling for reconciliation summary
                            if "summary_statistics" in csv_file.name:
                                st.success("✅ **Data Quality Summary**")
                                if len(df) > 0:
                                    quality_score = df.iloc[0].get('Data_Quality_Score', 0)
                                    st.metric("Overall Data Quality Score", f"{quality_score:.1f}%")
                            
                            # Display data
                            st.dataframe(df, use_container_width=True)
                            
                            # Download button
                            with open(csv_file, "rb") as f:
                                st.download_button(
                                    label=f"📥 Download {csv_file.name}",
                                    data=f.read(),
                                    file_name=csv_file.name,
                                    mime="text/csv",
                                    key=f"download_reconciliation_{csv_file.stem}"
                                )
                        except Exception as e:
                            st.error(f"Error loading {csv_file.name}: {str(e)}")
            else:
                st.warning("No reconciliation CSV files found.")
        else:
            st.warning("Reconciliation directory not found.")

def display_output_summary():
    """Display summary of all generated outputs"""
    outputs_dir = Path("input_test_4/outputs")
    if not outputs_dir.exists():
        st.warning("No outputs directory found. Please run the simulation first.")
        return
    
    st.subheader("📊 Output Summary")
    
    # Count files in each directory
    summary_data = []
    
    for category in ["intermediate", "final", "reconciliation"]:
        category_dir = outputs_dir / category
        if category_dir.exists():
            csv_files = list(category_dir.glob("*.csv"))
            total_size = sum(f.stat().st_size for f in csv_files) / 1024  # KB
            
            summary_data.append({
                "Category": category.replace("_", " ").title(),
                "Files": len(csv_files),
                "Total Size (KB)": f"{total_size:.1f}",
                "Status": "✅ Available" if csv_files else "⚠️ Empty"
            })
        else:
            summary_data.append({
                "Category": category.replace("_", " ").title(),
                "Files": 0,
                "Total Size (KB)": "0.0",
                "Status": "❌ Not Found"
            })
    
    # Display summary table
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True)
    
    # Show recommendations
    st.subheader("💡 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Outputs", key="refresh_outputs"):
            st.rerun()
    
    with col2:
        if st.button("📥 Download All CSV Files", key="download_all_csv"):
            st.info("Use individual download buttons in the tabs above to download specific files.")
    
    with col3:
        if st.button("📊 View Data Quality", key="view_quality"):
            reconciliation_dir = outputs_dir / "reconciliation"
            summary_file = reconciliation_dir / "reconciliation_summary_statistics.csv"
            if summary_file.exists():
                try:
                    df = pd.read_csv(summary_file)
                    if len(df) > 0:
                        quality_score = df.iloc[0].get('Data_Quality_Score', 0)
                        st.success(f"Data Quality Score: {quality_score:.1f}%")
                    else:
                        st.warning("No quality data available")
                except:
                    st.warning("Could not load quality data")
            else:
                st.warning("Quality report not found")

def main():
    # Header
    st.markdown('<h1 class="main-header">⚡ Hybrid Plant Simulation Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    
    # Check if outputs are available
    outputs_dir = Path("input_test_4/outputs")
    outputs_available = outputs_dir.exists() and any(outputs_dir.rglob("*.csv"))
    
    if outputs_available:
        st.sidebar.success("✅ Outputs Available")
    else:
        st.sidebar.warning("⚠️ No Outputs Found")
    
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Overview", "Configuration", "Simulation", "Results", "Documentation", "Output Files"]
    )
    
    if page == "Overview":
        show_overview()
    elif page == "Configuration":
        show_configuration()
    elif page == "Simulation":
        show_simulation()
    elif page == "Results":
        show_results()
    elif page == "Documentation":
        show_documentation()
    elif page == "Output Files":
        show_output_files()

def show_overview():
    """Show overview page"""
    st.header("🏭 Hybrid Plant Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### System Architecture
        The hybrid plant integrates renewable energy generation with industrial hydrogen production 
        and ammonia synthesis, optimized for Indian market conditions.
        
        **Energy Flow:**
        - Wind + Solar PV → Battery Storage
        - Battery → Electrolyzer → Hydrogen Production
        - Hydrogen → Compressor → Storage/Grid
        - Hydrogen → Ammonia Production
        """)
    
    with col2:
        st.markdown("""
        ### Key Components
        - **Renewable Energy**: Wind (50 MW) + Solar PV (40 MW)
        - **Energy Storage**: Battery (20 MWh)
        - **Hydrogen Infrastructure**: Electrolyzer (25 MW), Compressor, Storage
        - **End Use**: Ammonia Production Facility
        - **Grid Integration**: Bidirectional electricity and hydrogen exchange
        """)
    
    # Load current configuration for metrics
    studycase_config = load_config("input_test_4/studycase.json")
    if studycase_config and 'hybrid_plant' in studycase_config:
        config = studycase_config['hybrid_plant']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            wind_capacity = config.get('wind', {}).get('Npower', 0) / 1000
            st.metric("Wind Capacity", f"{wind_capacity:.1f} MW")
        
        with col2:
            pv_capacity = config.get('PV', {}).get('peakP', 0) / 1000
            st.metric("Solar PV Capacity", f"{pv_capacity:.1f} MW")
        
        with col3:
            battery_capacity = config.get('battery', {}).get('capacity', 0) / 1000
            st.metric("Battery Storage", f"{battery_capacity:.1f} MWh")
        
        with col4:
            electrolyzer_capacity = config.get('electrolyzer', {}).get('Npower', 0) / 1000
            st.metric("Electrolyzer", f"{electrolyzer_capacity:.1f} MW")

def show_configuration():
    """Show configuration page"""
    st.header("⚙️ Configuration Management")
    
    # Load configurations
    studycase_config = load_config("input_test_4/studycase.json")
    tech_costs = load_config("input_test_4/tech_cost.json")
    energy_market = load_config("input_test_4/energy_market.json")
    
    if not all([studycase_config, tech_costs, energy_market]):
        st.error("Failed to load configuration files")
        return
    
    # Tabs for different configuration sections
    tab1, tab2, tab3, tab4 = st.tabs(["System Components", "Technology Costs", "Energy Market", "Load Profiles"])
    
    with tab1:
        st.subheader("System Component Configuration")
        
        if 'hybrid_plant' in studycase_config:
            config = studycase_config['hybrid_plant']
            
            # Wind Configuration
            with st.expander("🌪️ Wind Power Configuration", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    wind_power = st.number_input(
                        "Wind Power (MW)", 
                        value=config.get('wind', {}).get('Npower', 50000) / 1000,
                        min_value=1.0,
                        max_value=1000.0,
                        step=1.0
                    )
                    config['wind']['Npower'] = wind_power * 1000
                
                with col2:
                    wind_cutin = st.number_input(
                        "Cut-in Speed (m/s)",
                        value=config.get('wind', {}).get('WScutin', 3.0),
                        min_value=1.0,
                        max_value=10.0,
                        step=0.1
                    )
                    config['wind']['WScutin'] = wind_cutin
                
                with col3:
                    wind_rated = st.number_input(
                        "Rated Speed (m/s)",
                        value=config.get('wind', {}).get('WSrated', 13.0),
                        min_value=5.0,
                        max_value=20.0,
                        step=0.5
                    )
                    config['wind']['WSrated'] = wind_rated
            
            # Solar PV Configuration
            with st.expander("☀️ Solar PV Configuration", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    pv_power = st.number_input(
                        "Solar PV Power (MW)",
                        value=config.get('PV', {}).get('peakP', 40000) / 1000,
                        min_value=1.0,
                        max_value=1000.0,
                        step=1.0
                    )
                    config['PV']['peakP'] = pv_power * 1000
                
                with col2:
                    pv_tilt = st.number_input(
                        "Tilt Angle (degrees)",
                        value=config.get('PV', {}).get('tilt', 28),
                        min_value=0,
                        max_value=90,
                        step=1
                    )
                    config['PV']['tilt'] = pv_tilt
                
                with col3:
                    pv_losses = st.number_input(
                        "System Losses (%)",
                        value=config.get('PV', {}).get('losses', 12),
                        min_value=0,
                        max_value=30,
                        step=1
                    )
                    config['PV']['losses'] = pv_losses
            
            # Battery Configuration
            with st.expander("🔋 Battery Storage Configuration", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    battery_capacity = st.number_input(
                        "Battery Capacity (MWh)",
                        value=config.get('battery', {}).get('capacity', 20000) / 1000,
                        min_value=1.0,
                        max_value=1000.0,
                        step=1.0
                    )
                    config['battery']['capacity'] = battery_capacity * 1000
                
                with col2:
                    battery_power = st.number_input(
                        "Battery Power (MW)",
                        value=config.get('battery', {}).get('max power', 10000) / 1000,
                        min_value=1.0,
                        max_value=500.0,
                        step=1.0
                    )
                    config['battery']['max power'] = battery_power * 1000
                
                with col3:
                    battery_efficiency = st.number_input(
                        "Battery Efficiency",
                        value=config.get('battery', {}).get('efficiency', 0.9),
                        min_value=0.5,
                        max_value=1.0,
                        step=0.01
                    )
                    config['battery']['efficiency'] = battery_efficiency
            
            # Electrolyzer Configuration
            with st.expander("⚗️ Electrolyzer Configuration", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    electrolyzer_power = st.number_input(
                        "Electrolyzer Power (MW)",
                        value=config.get('electrolyzer', {}).get('Npower', 25000) / 1000,
                        min_value=1.0,
                        max_value=100.0,
                        step=1.0
                    )
                    config['electrolyzer']['Npower'] = electrolyzer_power * 1000
                
                with col2:
                    electrolyzer_modules = st.number_input(
                        "Number of Modules",
                        value=config.get('electrolyzer', {}).get('number of modules', 250),
                        min_value=1,
                        max_value=1000,
                        step=10
                    )
                    config['electrolyzer']['number of modules'] = electrolyzer_modules
                
                with col3:
                    electrolyzer_model = st.selectbox(
                        "Stack Model",
                        ["PEM General", "SOFC", "simple"],
                        index=0
                    )
                    config['electrolyzer']['stack model'] = electrolyzer_model
            
            # Hydrogen Storage Configuration
            with st.expander("💧 Hydrogen Storage Configuration", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    h2_storage_capacity = st.number_input(
                        "Storage Capacity (kg)",
                        value=config.get('hydrogen_storage', {}).get('max capacity', 5000),
                        min_value=100,
                        max_value=100000,
                        step=100
                    )
                    config['hydrogen_storage']['max capacity'] = h2_storage_capacity
                
                with col2:
                    h2_storage_pressure = st.number_input(
                        "Storage Pressure (bar)",
                        value=config.get('hydrogen_storage', {}).get('pressure', 300),
                        min_value=50,
                        max_value=1000,
                        step=10
                    )
                    config['hydrogen_storage']['pressure'] = h2_storage_pressure
    
    with tab2:
        st.subheader("Technology Cost Configuration")
        
        # Create a form for cost updates
        with st.form("cost_config_form"):
            st.write("Update technology costs (₹/kW or ₹/kWh):")
            
            col1, col2 = st.columns(2)
            
            with col1:
                pv_cost = st.number_input(
                    "Solar PV Cost (₹/kW)",
                    value=tech_costs.get('PV', {}).get('cost per unit', 45000),
                    min_value=10000,
                    max_value=100000,
                    step=1000
                )
                
                wind_cost = st.number_input(
                    "Wind Cost (₹/kW)",
                    value=tech_costs.get('wind', {}).get('cost per unit', 65000),
                    min_value=20000,
                    max_value=150000,
                    step=1000
                )
                
                battery_cost = st.number_input(
                    "Battery Cost (₹/kWh)",
                    value=tech_costs.get('battery', {}).get('cost per unit', 75000),
                    min_value=20000,
                    max_value=200000,
                    step=1000
                )
                
                electrolyzer_cost = st.number_input(
                    "Electrolyzer Cost (₹/kW)",
                    value=tech_costs.get('electrolyzer', {}).get('cost per unit', 135000),
                    min_value=50000,
                    max_value=300000,
                    step=5000
                )
            
            with col2:
                compressor_cost = st.number_input(
                    "Hydrogen Compressor Cost (₹/kW)",
                    value=tech_costs.get('hydrogen_compressor', {}).get('cost per unit', 35000),
                    min_value=10000,
                    max_value=100000,
                    step=1000
                )
                
                storage_cost = st.number_input(
                    "Hydrogen Storage Cost (₹/kW)",
                    value=tech_costs.get('hydrogen_storage', {}).get('cost per unit', 60000),
                    min_value=10000,
                    max_value=150000,
                    step=1000
                )
                
                ammonia_cost = st.number_input(
                    "Ammonia Production Cost (₹/kW)",
                    value=tech_costs.get('ammonia_production', {}).get('cost per unit', 25000),
                    min_value=5000,
                    max_value=100000,
                    step=1000
                )
            
            if st.form_submit_button("Update Costs"):
                tech_costs['PV']['cost per unit'] = pv_cost
                tech_costs['wind']['cost per unit'] = wind_cost
                tech_costs['battery']['cost per unit'] = battery_cost
                tech_costs['electrolyzer']['cost per unit'] = electrolyzer_cost
                tech_costs['hydrogen_compressor']['cost per unit'] = compressor_cost
                tech_costs['hydrogen_storage']['cost per unit'] = storage_cost
                tech_costs['ammonia_production']['cost per unit'] = ammonia_cost
                
                if save_config(tech_costs, "input_test_4/tech_cost.json"):
                    st.success("Technology costs updated successfully!")
    
    with tab3:
        st.subheader("Energy Market Configuration")
        
        with st.form("market_config_form"):
            st.write("Update energy market parameters:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                electricity_purchase = st.number_input(
                    "Electricity Purchase Price (₹/kWh)",
                    value=energy_market.get('electricity', {}).get('purchase', 0.12),
                    min_value=0.01,
                    max_value=1.0,
                    step=0.01
                )
                
                electricity_sale = st.number_input(
                    "Electricity Sale Price (₹/kWh)",
                    value=energy_market.get('electricity', {}).get('sale', 0.08),
                    min_value=0.01,
                    max_value=1.0,
                    step=0.01
                )
                
                hydrogen_purchase = st.number_input(
                    "Hydrogen Purchase Price (₹/kg)",
                    value=energy_market.get('hydrogen', {}).get('purchase', 2.5),
                    min_value=0.1,
                    max_value=10.0,
                    step=0.1
                )
                
                hydrogen_sale = st.number_input(
                    "Hydrogen Sale Price (₹/kg)",
                    value=energy_market.get('hydrogen', {}).get('sale', 2.0),
                    min_value=0.1,
                    max_value=10.0,
                    step=0.1
                )
            
            with col2:
                green_h2_incentive = st.number_input(
                    "Green Hydrogen Incentive (₹/kg)",
                    value=energy_market.get('green_hydrogen_incentives', {}).get('value', 1.5),
                    min_value=0.0,
                    max_value=10.0,
                    step=0.1
                )
                
                ammonia_incentive = st.number_input(
                    "Ammonia Production Incentive (₹/kg)",
                    value=energy_market.get('ammonia_incentives', {}).get('value', 0.05),
                    min_value=0.0,
                    max_value=5.0,
                    step=0.01
                )
                
                interest_rate = st.number_input(
                    "Interest Rate (%)",
                    value=energy_market.get('interest rate', 0.085) * 100,
                    min_value=1.0,
                    max_value=20.0,
                    step=0.1
                )
            
            if st.form_submit_button("Update Market Parameters"):
                energy_market['electricity']['purchase'] = electricity_purchase
                energy_market['electricity']['sale'] = electricity_sale
                energy_market['hydrogen']['purchase'] = hydrogen_purchase
                energy_market['hydrogen']['sale'] = hydrogen_sale
                energy_market['green_hydrogen_incentives']['value'] = green_h2_incentive
                energy_market['ammonia_incentives']['value'] = ammonia_incentive
                energy_market['interest rate'] = interest_rate / 100
                
                if save_config(energy_market, "input_test_4/energy_market.json"):
                    st.success("Energy market parameters updated successfully!")
    
    with tab4:
        st.subheader("Load Profile Information")
        st.info("""
        Load profiles are stored as CSV files in the `input_test_4/loads/` directory.
        The system currently uses the following load profiles:
        - `electric_load_hybrid.csv` - Total electricity demand
        - `heat_load_hybrid.csv` - Total heat demand  
        - `hydrogen_demand_hybrid.csv` - Total hydrogen demand
        - `ammonia_electric_load.csv` - Ammonia facility electricity demand
        - `ammonia_heat_load.csv` - Ammonia facility heat demand
        - `ammonia_hydrogen_load.csv` - Ammonia facility hydrogen demand
        """)
        
        # Display load profile files
        loads_dir = Path("input_test_4/loads")
        if loads_dir.exists():
            load_files = list(loads_dir.glob("*.csv"))
            if load_files:
                st.write("**Available Load Profile Files:**")
                for file in load_files:
                    st.write(f"- {file.name}")
            else:
                st.warning("No load profile files found")

def show_simulation():
    """Show simulation page"""
    st.header("🚀 Run Simulation")
    
    st.markdown("""
    ### Simulation Overview
    The hybrid plant simulation analyzes the energy flows, economics, and performance 
    of the integrated renewable energy and hydrogen production system.
    """)
    
    # Simulation controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Simulation Parameters")
        
        # Check if configuration files exist
        config_files = [
            "input_test_4/studycase.json",
            "input_test_4/tech_cost.json", 
            "input_test_4/energy_market.json"
        ]
        
        missing_files = [f for f in config_files if not os.path.exists(f)]
        if missing_files:
            st.error(f"Missing configuration files: {', '.join(missing_files)}")
            return
        
        st.success("✅ All configuration files are present")
        
        # Load current configuration for display
        studycase_config = load_config("input_test_4/studycase.json")
        if studycase_config and 'hybrid_plant' in studycase_config:
            config = studycase_config['hybrid_plant']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Wind Power", f"{config.get('wind', {}).get('Npower', 0)/1000:.1f} MW")
                st.metric("Solar PV", f"{config.get('PV', {}).get('peakP', 0)/1000:.1f} MW")
            
            with col2:
                st.metric("Battery Storage", f"{config.get('battery', {}).get('capacity', 0)/1000:.1f} MWh")
                st.metric("Electrolyzer", f"{config.get('electrolyzer', {}).get('Npower', 0)/1000:.1f} MW")
            
            with col3:
                st.metric("H2 Storage", f"{config.get('hydrogen_storage', {}).get('max capacity', 0):.0f} kg")
                st.metric("Peak Demand", "33 MW")
    
    with col2:
        st.subheader("Run Simulation")
        
        if st.button("🚀 Start Simulation", type="primary", use_container_width=True):
            with st.spinner("Running simulation..."):
                success, stdout, stderr = run_simulation()
                
                if success:
                    st.success("✅ Simulation completed successfully!")
                    
                    # Display simulation output
                    with st.expander("Simulation Output", expanded=False):
                        st.text(stdout)
                    
                    # Show quick results
                    st.subheader("📊 Quick Results")
                    
                    # Check for generated plots
                    plots_dir = Path("input_test_4/plots")
                    if plots_dir.exists():
                        plot_files = list(plots_dir.glob("*.png"))
                        if plot_files:
                            st.success(f"Generated {len(plot_files)} plot files")
                        else:
                            st.warning("No plot files generated")
                else:
                    st.error("❌ Simulation failed!")
                    with st.expander("Error Details", expanded=True):
                        st.text(stderr)

def show_results():
    """Show results page"""
    st.header("📊 Simulation Results")
    
    # Check if results exist
    plots_dir = Path("input_test_4/plots")
    if not plots_dir.exists():
        st.warning("No simulation results found. Please run the simulation first.")
        return
    
    # Results tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "Output Summary", "CSV Files", "Energy Flow", "System Summary", "Economic Analysis", "Load Profiles", "Production Profiles", "PDF Report", "Image Gallery"
    ])
    
    with tab1:
        st.subheader("📊 Output Summary")
        display_output_summary()
    
    with tab2:
        st.subheader("📄 CSV Output Files")
        display_csv_outputs()
    
    with tab3:
        st.subheader("Energy Flow Diagram")
        display_energy_flow_diagram()
    
    with tab4:
        st.subheader("System Summary")
        display_system_summary()
    
    with tab5:
        st.subheader("Economic Analysis")
        display_economic_analysis()
    
    with tab6:
        st.subheader("Load Profiles")
        display_load_profiles()
    
    with tab7:
        st.subheader("Production Profiles")
        display_production_profiles()
    
    with tab8:
        st.subheader("PDF Report")
        display_pdf_report()
    
    with tab9:
        st.subheader("Image Gallery")
        display_image_gallery()
    
    # Download section
    st.subheader("📥 Download All Results")
    
    if plots_dir.exists():
        # Show file information
        st.write("**📊 Available Files:**")
        
        # Get all files
        all_files = list(plots_dir.glob("*"))
        if all_files:
            file_info = []
            for file in all_files:
                size_mb = file.stat().st_size / (1024 * 1024)
                file_info.append({
                    "File": file.name,
                    "Type": file.suffix.upper(),
                    "Size (MB)": f"{size_mb:.2f}"
                })
            
            # Display file table
            import pandas as pd
            df = pd.DataFrame(file_info)
            st.dataframe(df, use_container_width=True)
            
            # Download buttons
            st.write("**📥 Download Options:**")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Individual Files:**")
                for file in all_files:
                    with open(file, "rb") as f:
                        st.download_button(
                            label=f"📥 {file.name}",
                            data=f.read(),
                            file_name=file.name,
                            mime="application/octet-stream",
                            key=f"download_{file.name}"
                        )
            
            with col2:
                st.write("**Quick Actions:**")
                if st.button("🔄 Refresh Results", key="refresh_results"):
                    st.rerun()
                
                st.write("💡 **Tip**: Use the individual tabs above for detailed viewing of each result type.")
        else:
            st.warning("No result files found. Please run the simulation first.")

def show_documentation():
    """Show documentation page"""
    st.header("📚 Documentation")
    
    # Create tabs for different documentation sections
    tab1, tab2, tab3, tab4 = st.tabs(["Model Inputs", "Technology Components", "Output Generation", "Quick Guide"])
    
    with tab1:
        st.subheader("📋 Model Inputs Documentation")
        st.markdown("""
        This section provides a comprehensive overview of all inputs being taken by the model, 
        including what variables are considered, what is assumed implicitly, and what is not used.
        """)
        
        # Load and display the Model Inputs Documentation
        try:
            with open("input_test_4/MODEL_INPUTS_DOCUMENTATION.md", "r", encoding="utf-8") as f:
                model_docs = f.read()
            
            # Convert markdown to HTML for better display
            try:
                import markdown
                html_content = markdown.markdown(model_docs, extensions=['tables', 'fenced_code'])
            except ImportError:
                # Fallback if markdown library is not available
                st.warning("Markdown library not available. Displaying raw markdown.")
                st.markdown(model_docs)
                return
            
            # Display with custom CSS for better formatting
            st.markdown("""
            <style>
            .documentation-content {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #1f77b4;
                margin: 10px 0;
            }
            .documentation-content table {
                border-collapse: collapse;
                width: 100%;
                margin: 10px 0;
            }
            .documentation-content th, .documentation-content td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            .documentation-content th {
                background-color: #1f77b4;
                color: white;
            }
            .documentation-content h1, .documentation-content h2, .documentation-content h3 {
                color: #1f77b4;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            .documentation-content code {
                background-color: #e9ecef;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div class="documentation-content">{html_content}</div>', unsafe_allow_html=True)
            
            # Add download button for the documentation
            with open("input_test_4/MODEL_INPUTS_DOCUMENTATION.md", "r", encoding="utf-8") as f:
                st.download_button(
                    label="📥 Download Model Inputs Documentation (PDF)",
                    data=f.read(),
                    file_name="MODEL_INPUTS_DOCUMENTATION.md",
                    mime="text/markdown"
                )
                
        except FileNotFoundError:
            st.error("Model Inputs Documentation file not found. Please ensure the file exists in the input_test_4 directory.")
        except Exception as e:
            st.error(f"Error loading Model Inputs Documentation: {str(e)}")
    
    with tab2:
        st.subheader("🔧 Technology Components Analysis")
        st.markdown("""
        This section provides a comprehensive analysis of all technology components, 
        their inputs/outputs, capabilities, and limitations to give a clear picture 
        of what the simulation can and cannot do.
        """)
        
        # Load and display the Technology Components Analysis
        try:
            with open("input_test_4/TECHNOLOGY_COMPONENTS_ANALYSIS.md", "r", encoding="utf-8") as f:
                tech_docs = f.read()
            
            # Convert markdown to HTML for better display
            try:
                import markdown
                html_content = markdown.markdown(tech_docs, extensions=['tables', 'fenced_code'])
            except ImportError:
                # Fallback if markdown library is not available
                st.warning("Markdown library not available. Displaying raw markdown.")
                st.markdown(tech_docs)
                return
            
            # Display with custom CSS for better formatting
            st.markdown("""
            <style>
            .tech-documentation-content {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #28a745;
                margin: 10px 0;
            }
            .tech-documentation-content table {
                border-collapse: collapse;
                width: 100%;
                margin: 10px 0;
            }
            .tech-documentation-content th, .tech-documentation-content td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            .tech-documentation-content th {
                background-color: #28a745;
                color: white;
            }
            .tech-documentation-content h1, .tech-documentation-content h2, .tech-documentation-content h3 {
                color: #28a745;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            .tech-documentation-content code {
                background-color: #e9ecef;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div class="tech-documentation-content">{html_content}</div>', unsafe_allow_html=True)
            
            # Add download button for the documentation
            with open("input_test_4/TECHNOLOGY_COMPONENTS_ANALYSIS.md", "r", encoding="utf-8") as f:
                st.download_button(
                    label="📥 Download Technology Components Analysis (PDF)",
                    data=f.read(),
                    file_name="TECHNOLOGY_COMPONENTS_ANALYSIS.md",
                    mime="text/markdown"
                )
                
        except FileNotFoundError:
            st.error("Technology Components Analysis file not found. Please ensure the file exists in the input_test_4 directory.")
        except Exception as e:
            st.error(f"Error loading Technology Components Analysis: {str(e)}")
    
    with tab3:
        st.subheader("📊 Output Generation System")
        st.markdown("""
        This section provides comprehensive documentation of the output generation system 
        that creates intermediate and final CSV files, along with a detailed reconciliation 
        exercise to validate data consistency and robustness.
        """)
        
        # Load and display the Output Generation Documentation
        try:
            with open("input_test_4/OUTPUT_GENERATION_DOCUMENTATION.md", "r", encoding="utf-8") as f:
                output_docs = f.read()
            
            # Convert markdown to HTML for better display
            try:
                import markdown
                html_content = markdown.markdown(output_docs, extensions=['tables', 'fenced_code'])
            except ImportError:
                # Fallback if markdown library is not available
                st.warning("Markdown library not available. Displaying raw markdown.")
                st.markdown(output_docs)
                return
            
            # Display with custom CSS for better formatting
            st.markdown("""
            <style>
            .output-documentation-content {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #ffc107;
                margin: 10px 0;
            }
            .output-documentation-content table {
                border-collapse: collapse;
                width: 100%;
                margin: 10px 0;
            }
            .output-documentation-content th, .output-documentation-content td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            .output-documentation-content th {
                background-color: #ffc107;
                color: white;
            }
            .output-documentation-content h1, .output-documentation-content h2, .output-documentation-content h3 {
                color: #ffc107;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            .output-documentation-content code {
                background-color: #e9ecef;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div class="output-documentation-content">{html_content}</div>', unsafe_allow_html=True)
            
            # Add download button for the documentation
            with open("input_test_4/OUTPUT_GENERATION_DOCUMENTATION.md", "r", encoding="utf-8") as f:
                st.download_button(
                    label="📥 Download Output Generation Documentation (PDF)",
                    data=f.read(),
                    file_name="OUTPUT_GENERATION_DOCUMENTATION.md",
                    mime="text/markdown"
                )
                
        except FileNotFoundError:
            st.error("Output Generation Documentation file not found. Please ensure the file exists in the input_test_4 directory.")
        except Exception as e:
            st.error(f"Error loading Output Generation Documentation: {str(e)}")
    
    with tab4:
        st.subheader("🚀 Quick Start Guide")
        st.markdown("""
        ### Hybrid Plant Simulation Quick Guide
        
        This application provides an interactive interface for configuring and running 
        a hybrid renewable energy and hydrogen production plant simulation.
        
        #### System Components
        
        **🌪️ Wind Power**
        - Capacity: Configurable wind power generation
        - Technology: Power curve model with configurable parameters
        - Location: Optimized for Indian wind conditions
        
        **☀️ Solar PV**
        - Capacity: Configurable solar power generation
        - Technology: Fixed tilt with tracking options
        - Location: Optimized for Indian solar conditions
        
        **🔋 Battery Storage**
        - Capacity: Configurable energy storage
        - Technology: Lithium-ion battery with efficiency modeling
        - Purpose: Energy time-shifting and grid stability
        
        **⚗️ Electrolyzer**
        - Capacity: Configurable hydrogen production
        - Technology: PEM electrolyzer with modular design
        - Purpose: Green hydrogen production from renewable electricity
        
        **💧 Hydrogen Infrastructure**
        - Compressor: Multi-stage hydrogen compression
        - Storage: High-pressure hydrogen storage
        - Purpose: Hydrogen handling and distribution
        
        **🏭 Ammonia Production**
        - Capacity: Industrial ammonia synthesis facility
        - Technology: Green ammonia production from hydrogen
        - Purpose: End-use application and energy carrier
        
        #### Configuration Files
        
        - **studycase.json**: System component configuration
        - **tech_cost.json**: Technology cost parameters
        - **energy_market.json**: Energy prices and incentives
        - **Load profiles**: CSV files with demand patterns
        
        #### Simulation Outputs
        
        - Energy flow diagrams
        - Economic analysis
        - System performance metrics
        - Load and production profiles
        - PDF summary report
        
        #### Usage Instructions
        
        1. **Configuration**: Modify system parameters in the Configuration tab
        2. **Simulation**: Run the simulation in the Simulation tab
        3. **Results**: View and download results in the Results tab
        4. **Documentation**: Reference the detailed documentation tabs above
        
        #### Key Features
        
        ✅ **127 Explicit Input Parameters** across 6 major categories  
        ✅ **16 Technology Components** with detailed modeling  
        ✅ **Real Weather Data Integration** via PVGIS  
        ✅ **Comprehensive Economic Analysis** with Indian market data  
        ✅ **High Temporal Resolution** simulation capability  
        ✅ **Multi-Energy System** modeling (electricity, heat, hydrogen, oxygen)  
        
        #### Model Capabilities
        
        **What the simulation CAN do:**
        - System design and component sizing
        - Economic feasibility analysis
        - Technology comparison studies
        - Long-term strategic planning
        - Policy impact assessment
        - Multi-year performance analysis
        
        **What the simulation CANNOT do:**
        - Real-time control and operation
        - Day-ahead optimization
        - Grid stability analysis
        - Component failure modeling
        - Maintenance scheduling
        
        #### Getting Started
        
        1. **Review Documentation**: Start with the detailed documentation tabs
        2. **Configure System**: Use the Configuration tab to set up your system
        3. **Run Simulation**: Execute the simulation in the Simulation tab
        4. **Analyze Results**: Review comprehensive results in the Results tab
        5. **Download Reports**: Save all analysis and documentation for further use
        """)
        
        # Add a summary metrics section
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Input Parameters", "127", "Explicit parameters")
        with col2:
            st.metric("Technology Components", "16", "Available technologies")
        with col3:
            st.metric("Energy Carriers", "4", "Electricity, Heat, H₂, O₂")
        
        # Add a capabilities summary
        st.subheader("📊 Model Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **✅ Strengths:**
            - Comprehensive multi-energy modeling
            - High technical detail
            - Real weather integration
            - Detailed economic analysis
            - Long-term analysis capability
            - Modular component design
            """)
        
        with col2:
            st.markdown("""
            **⚠️ Limitations:**
            - No real-time control
            - Simplified operations
            - Fixed technology options
            - No environmental impact
            - Basic grid integration
            """)

def show_output_files():
    """Show output files page"""
    st.header("📊 Output Files Viewer")
    
    st.markdown("""
    ### Comprehensive Output Analysis
    
    This page provides direct access to all generated CSV files from the simulation.
    You can view, analyze, and download all output data in one place.
    """)
    
    # Check if outputs exist
    outputs_dir = Path("input_test_4/outputs")
    if not outputs_dir.exists():
        st.warning("⚠️ No output files found. Please run the simulation first to generate outputs.")
        st.info("💡 **To generate outputs:** Go to the Simulation page and click 'Start Simulation'")
        return
    
    # Display output summary
    display_output_summary()
    
    st.divider()
    
    # Display all CSV files
    display_csv_outputs()
    
    # Additional features
    st.divider()
    st.subheader("🔧 Advanced Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📈 Data Analysis Tips:**
        - Use the expandable sections to view detailed data
        - Download CSV files for external analysis
        - Check reconciliation reports for data quality
        - Review recommendations for improvements
        """)
    
    with col2:
        st.markdown("""
        **💾 File Categories:**
        - **Intermediate**: Raw data processing
        - **Final**: Processed results and analysis
        - **Reconciliation**: Data validation reports
        """)

if __name__ == "__main__":
    main()
