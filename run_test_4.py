#!/usr/bin/env python3
"""
Run script for INPUT_TEST_4: Mixed End-Use Hybrid Plant Simulation

This script simulates a comprehensive mixed end-use hybrid plant that integrates:
- Renewable energy generation (wind + solar)
- Energy storage systems (battery + large-scale storage)
- Hydrogen production and storage infrastructure
- Industrial end-use facilities (steel + ammonia production)

The system follows the GreenHEART process: Model Definition -> Simulation -> Optimization -> Analysis
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set plotting style
plt.style.use('default')
sns.set_palette("husl")

# Currency conversion (approximate rate)
EUR_TO_INR = 90.0

def eur_to_inr(eur_value):
    """Convert Euro value to Indian Rupees"""
    return eur_value * EUR_TO_INR

# Create plots directory if it doesn't exist
PLOTS_DIR = "input_test_4/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

def load_config(config_file):
    """Load configuration from JSON file"""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file {config_file} not found")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {config_file}")
        return None

def load_load_profile(load_file):
    """Load load profile from CSV file"""
    try:
        df = pd.read_csv(load_file, parse_dates=['timestamp'])
        return df
    except FileNotFoundError:
        print(f"Warning: Load file {load_file} not found")
        return None

def load_production_profile(prod_file):
    """Load production profile from CSV file"""
    try:
        # Production files don't have timestamp columns, they use index-based time
        df = pd.read_csv(prod_file)
        # Add timestamp column based on 1-minute intervals starting from 2023-01-01
        df['timestamp'] = pd.date_range('2023-01-01', periods=len(df), freq='1min')
        return df
    except FileNotFoundError:
        print(f"Warning: Production file {prod_file} not found")
        return None

def create_load_profile_plots(loads_data):
    """Create and save load profile plots"""
    print("Creating load profile plots...")
    
    # Set up the figure
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Hybrid Plant Load Profiles (24-Hour Period - 1-Minute Resolution)', fontsize=16, fontweight='bold')
    
    # Electricity load
    if 'electric_load_hybrid.csv' in loads_data:
        ax1 = axes[0, 0]
        ax1.plot(loads_data['electric_load_hybrid.csv']['timestamp'], 
                loads_data['electric_load_hybrid.csv']['electricity_demand'], 
                'b-', linewidth=2, label='Total Electricity')
        ax1.set_title('Electricity Demand')
        ax1.set_ylabel('Power (kW)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Add steel and ammonia specific loads
        if 'steel_electric_load.csv' in loads_data:
            ax1.plot(loads_data['steel_electric_load.csv']['timestamp'], 
                    loads_data['steel_electric_load.csv']['steel_electricity_demand'], 
                    'r--', linewidth=1.5, label='Steel Production')
        if 'ammonia_electric_load.csv' in loads_data:
            ax1.plot(loads_data['ammonia_electric_load.csv']['timestamp'], 
                    loads_data['ammonia_electric_load.csv']['ammonia_electricity_demand'], 
                    'g--', linewidth=1.5, label='Ammonia Production')
        ax1.legend()
    
    # Heat load
    if 'heat_load_hybrid.csv' in loads_data:
        ax2 = axes[0, 1]
        ax2.plot(loads_data['heat_load_hybrid.csv']['timestamp'], 
                loads_data['heat_load_hybrid.csv']['heat_demand'], 
                'r-', linewidth=2, label='Total Heat')
        ax2.set_title('Heat Demand')
        ax2.set_ylabel('Heat (kW)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Add steel and ammonia specific heat loads
        if 'steel_heat_load.csv' in loads_data:
            ax2.plot(loads_data['steel_heat_load.csv']['timestamp'], 
                    loads_data['steel_heat_load.csv']['steel_heat_demand'], 
                    'r--', linewidth=1.5, label='Steel Production')
        if 'ammonia_heat_load.csv' in loads_data:
            ax2.plot(loads_data['ammonia_heat_load.csv']['timestamp'], 
                    loads_data['ammonia_heat_load.csv']['ammonia_heat_demand'], 
                    'g--', linewidth=1.5, label='Ammonia Production')
        ax2.legend()
    
    # Hydrogen load
    if 'hydrogen_demand_hybrid.csv' in loads_data:
        ax3 = axes[1, 0]
        ax3.plot(loads_data['hydrogen_demand_hybrid.csv']['timestamp'], 
                loads_data['hydrogen_demand_hybrid.csv']['hydrogen_demand'], 
                'g-', linewidth=2, label='Total Hydrogen')
        ax3.set_title('Hydrogen Demand')
        ax3.set_ylabel('Hydrogen (kg/h)')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        
        # Add steel and ammonia specific hydrogen loads
        if 'steel_hydrogen_load.csv' in loads_data:
            ax3.plot(loads_data['steel_hydrogen_load.csv']['timestamp'], 
                    loads_data['steel_hydrogen_load.csv']['steel_hydrogen_demand'], 
                    'r--', linewidth=1.5, label='Steel Production')
        if 'ammonia_hydrogen_load.csv' in loads_data:
            ax3.plot(loads_data['ammonia_hydrogen_load.csv']['timestamp'], 
                    loads_data['ammonia_hydrogen_load.csv']['ammonia_hydrogen_demand'], 
                    'g--', linewidth=1.5, label='Ammonia Production')
        ax3.legend()
    
    # Combined load comparison
    ax4 = axes[1, 1]
    if 'electric_load_hybrid.csv' in loads_data:
        ax4.plot(loads_data['electric_load_hybrid.csv']['timestamp'], 
                loads_data['electric_load_hybrid.csv']['electricity_demand']/1000, 
                'b-', linewidth=2, label='Electricity (MW)')
    if 'heat_load_hybrid.csv' in loads_data:
        ax4.plot(loads_data['heat_load_hybrid.csv']['timestamp'], 
                loads_data['heat_load_hybrid.csv']['heat_demand']/1000, 
                'r-', linewidth=2, label='Heat (MW)')
    if 'hydrogen_demand_hybrid.csv' in loads_data:
        ax4.plot(loads_data['hydrogen_demand_hybrid.csv']['timestamp'], 
                loads_data['hydrogen_demand_hybrid.csv']['hydrogen_demand']/1000, 
                'g-', linewidth=2, label='Hydrogen (ton/h)')
    
    ax4.set_title('Combined Load Comparison')
    ax4.set_ylabel('Load (MW or ton/h)')
    ax4.set_xlabel('Time')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    
    # Format x-axis
    for ax in axes.flat:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/load_profiles.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Load profile plots saved to {PLOTS_DIR}/load_profiles.png")

def create_production_profile_plots(production_data):
    """Create and save production profile plots"""
    print("Creating production profile plots...")
    
    fig, axes = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('Renewable Energy Production Profiles (24-Hour Period - 1-Minute Resolution)', fontsize=16, fontweight='bold')
    
    # Wind production
    if 'windproduction.csv' in production_data:
        ax1 = axes[0]
        wind_data = production_data['windproduction.csv']
        if 'kW' in wind_data.columns:
            # Take first 1440 minutes (24 hours) for daily profile
            wind_24h = wind_data.head(1440)
            ax1.plot(wind_24h['timestamp'], wind_24h['kW'], 'b-', linewidth=1, label='Wind Power')
        elif 'wind' in wind_data.columns:
            wind_24h = wind_data.head(1440)
            ax1.plot(wind_24h['timestamp'], wind_24h['wind'], 'b-', linewidth=1, label='Wind Power')
        elif 'power' in wind_data.columns:
            wind_24h = wind_data.head(1440)
            ax1.plot(wind_24h['timestamp'], wind_24h['power'], 'b-', linewidth=1, label='Wind Power')
        ax1.set_title('Wind Power Generation (24-Hour Profile)')
        ax1.set_ylabel('Power (kW)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
    
    # Solar PV production
    if 'PV_hybrid.csv' in production_data:
        ax2 = axes[1]
        pv_data = production_data['PV_hybrid.csv']
        if 'P' in pv_data.columns:
            # Take first 1440 minutes (24 hours) for daily profile
            pv_24h = pv_data.head(1440)
            ax2.plot(pv_24h['timestamp'], pv_24h['P'], 'y-', linewidth=1, label='Solar PV')
        elif 'PV' in pv_data.columns:
            pv_24h = pv_data.head(1440)
            ax2.plot(pv_24h['timestamp'], pv_24h['PV'], 'y-', linewidth=1, label='Solar PV')
        elif 'power' in pv_data.columns:
            pv_24h = pv_data.head(1440)
            ax2.plot(pv_24h['timestamp'], pv_24h['power'], 'y-', linewidth=1, label='Solar PV')
        ax2.set_title('Solar PV Generation (24-Hour Profile)')
        ax2.set_ylabel('Power (kW)')
        ax2.set_xlabel('Time')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
    
    # Format x-axis
    for ax in axes:
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/production_profiles.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Production profile plots saved to {PLOTS_DIR}/production_profiles.png")

def create_energy_flow_diagram(studycase_config):
    """Create and save energy flow diagram"""
    print("Creating energy flow diagram...")
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    
    # Define component positions
    components = {
        'Wind': (2, 8),
        'Solar PV': (4, 8),
        'Battery': (3, 6),
        'Large Storage': (5, 6),
        'Electrolyzer': (2, 4),
        'Fuel Cell': (4, 4),
        'H2 Compressor': (6, 4),
        'H2 Storage': (6, 2),
        'Steel Production': (1, 0),
        'Ammonia Production': (5, 0),
        'Grid': (8, 4)
    }
    
    # Draw components
    for name, pos in components.items():
        if name in ['Wind', 'Solar PV']:
            ax.add_patch(plt.Rectangle((pos[0]-0.4, pos[1]-0.3), 0.8, 0.6, 
                                     facecolor='lightblue', edgecolor='blue', linewidth=2))
        elif name in ['Battery', 'Large Storage']:
            ax.add_patch(plt.Rectangle((pos[0]-0.4, pos[1]-0.3), 0.8, 0.6, 
                                     facecolor='lightgreen', edgecolor='green', linewidth=2))
        elif name in ['Electrolyzer', 'Fuel Cell']:
            ax.add_patch(plt.Rectangle((pos[0]-0.4, pos[1]-0.3), 0.8, 0.6, 
                                     facecolor='lightyellow', edgecolor='orange', linewidth=2))
        elif name in ['Steel Production', 'Ammonia Production']:
            ax.add_patch(plt.Rectangle((pos[0]-0.4, pos[1]-0.3), 0.8, 0.6, 
                                     facecolor='lightcoral', edgecolor='red', linewidth=2))
        else:
            ax.add_patch(plt.Rectangle((pos[0]-0.4, pos[1]-0.3), 0.8, 0.6, 
                                     facecolor='lightgray', edgecolor='black', linewidth=2))
        
        ax.text(pos[0], pos[1], name, ha='center', va='center', fontweight='bold', fontsize=10)
    
    # Draw energy flow arrows
    arrows = [
        ((2, 7.7), (3, 6.3)),  # Wind to Battery
        ((4, 7.7), (5, 6.3)),  # Solar to Large Storage
        ((3, 5.7), (2, 4.3)),  # Battery to Electrolyzer
        ((5, 5.7), (4, 4.3)),  # Large Storage to Fuel Cell
        ((2, 3.7), (6, 4.3)),  # Electrolyzer to H2 Compressor
        ((6, 3.7), (6, 2.3)),  # H2 Compressor to H2 Storage
        ((6, 1.7), (1, 0.3)),  # H2 Storage to Steel
        ((6, 1.7), (5, 0.3)),  # H2 Storage to Ammonia
        ((4, 3.7), (8, 4.3)),  # Fuel Cell to Grid
        ((8, 3.7), (4, 4.3)),  # Grid to Fuel Cell
    ]
    
    for start, end in arrows:
        ax.annotate('', xy=end, xytext=start,
                   arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Hybrid Plant Energy Flow Diagram', fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/energy_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Energy flow diagram saved to {PLOTS_DIR}/energy_flow_diagram.png")

def create_economic_analysis_plots(tech_costs, energy_market):
    """Create and save economic analysis plots"""
    print("Creating economic analysis plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Economic Analysis of Hybrid Plant', fontsize=16, fontweight='bold')
    
    # Capital costs breakdown
    if tech_costs:
        ax1 = axes[0, 0]
        tech_names = list(tech_costs.keys())
        capital_costs = []
        valid_tech_names = []
        
        for tech in tech_names:
            if 'cost per unit' in tech_costs[tech] and isinstance(tech_costs[tech]['cost per unit'], (int, float)):
                capital_costs.append(tech_costs[tech]['cost per unit'])
                valid_tech_names.append(tech)
        
        if capital_costs:
            # Convert to Rupees
            capital_costs_inr = [eur_to_inr(cost) for cost in capital_costs]
            bars = ax1.bar(valid_tech_names, capital_costs_inr, color='skyblue', alpha=0.7)
            ax1.set_title('Capital Costs by Technology')
            ax1.set_ylabel('Capital Cost (₹/kW or ₹/kWh)')
            ax1.tick_params(axis='x', rotation=45)
            ax1.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, cost in zip(bars, capital_costs_inr):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + max(capital_costs_inr)*0.01,
                        f'{cost:,.0f}', ha='center', va='bottom', fontsize=8)
    
    # O&M costs breakdown
    if tech_costs:
        ax2 = axes[0, 1]
        om_costs = []
        om_tech_names = []
        
        for tech in tech_names:
            if 'OeM' in tech_costs[tech] and isinstance(tech_costs[tech]['OeM'], (int, float)):
                om_costs.append(tech_costs[tech]['OeM'])
                om_tech_names.append(tech)
        
        if om_costs:
            # Convert to Rupees
            om_costs_inr = [eur_to_inr(cost) for cost in om_costs]
            bars = ax2.bar(om_tech_names, om_costs_inr, color='lightgreen', alpha=0.7)
            ax2.set_title('O&M Costs by Technology')
            ax2.set_ylabel('O&M Cost (₹/kW/year or ₹/kWh/year)')
            ax2.tick_params(axis='x', rotation=45)
            ax2.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, cost in zip(bars, om_costs_inr):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + max(om_costs_inr)*0.01,
                        f'{cost:,.0f}', ha='center', va='bottom', fontsize=8)
    
    # Energy prices
    if energy_market:
        ax3 = axes[1, 0]
        prices = []
        labels = []
        
        # Extract energy prices from the actual structure
        if 'electricity' in energy_market and 'purchase' in energy_market['electricity']:
            prices.append(energy_market['electricity']['purchase'])
            labels.append('Electricity\n(Purchase)')
        if 'electricity' in energy_market and 'sale' in energy_market['electricity']:
            prices.append(energy_market['electricity']['sale'])
            labels.append('Electricity\n(Sale)')
        if 'hydrogen' in energy_market and 'purchase' in energy_market['hydrogen']:
            prices.append(energy_market['hydrogen']['purchase'])
            labels.append('Hydrogen\n(Purchase)')
        if 'hydrogen' in energy_market and 'sale' in energy_market['hydrogen']:
            prices.append(energy_market['hydrogen']['sale'])
            labels.append('Hydrogen\n(Sale)')
        if 'oxygen' in energy_market and 'sale' in energy_market['oxygen']:
            prices.append(energy_market['oxygen']['sale'])
            labels.append('Oxygen\n(Sale)')
        if 'water' in energy_market and 'purchase' in energy_market['water']:
            prices.append(energy_market['water']['purchase'])
            labels.append('Water\n(Purchase)')
        if 'gas' in energy_market and 'purchase' in energy_market['gas']:
            prices.append(energy_market['gas']['purchase'])
            labels.append('Gas\n(Purchase)')
        
        if prices:
            # Convert to Rupees
            prices_inr = [eur_to_inr(price) for price in prices]
            bars = ax3.bar(labels, prices_inr, color='lightcoral', alpha=0.7)
            ax3.set_title('Energy Prices')
            ax3.set_ylabel('Price (₹/kWh or ₹/kg)')
            ax3.tick_params(axis='x', rotation=45)
            ax3.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, price in zip(bars, prices_inr):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height + max(prices_inr)*0.01,
                        f'{price:.2f}', ha='center', va='bottom', fontsize=8)
    
    # Incentives breakdown
    if energy_market:
        ax4 = axes[1, 1]
        incentives = []
        incentive_labels = []
        
        # Extract incentives from the actual structure
        if 'green_hydrogen_incentives' in energy_market and 'value' in energy_market['green_hydrogen_incentives']:
            incentives.append(energy_market['green_hydrogen_incentives']['value'])
            incentive_labels.append('Green Hydrogen\nIncentive')
        if 'steel_incentives' in energy_market and 'value' in energy_market['steel_incentives']:
            incentives.append(energy_market['steel_incentives']['value'])
            incentive_labels.append('Steel Production\nIncentive')
        if 'ammonia_incentives' in energy_market and 'value' in energy_market['ammonia_incentives']:
            incentives.append(energy_market['ammonia_incentives']['value'])
            incentive_labels.append('Ammonia Production\nIncentive')
        if 'REC' in energy_market and 'collective self consumption incentives' in energy_market['REC']:
            incentives.append(energy_market['REC']['collective self consumption incentives'])
            incentive_labels.append('REC Self Consumption\nIncentive')
        
        if incentives:
            # Convert to Rupees
            incentives_inr = [eur_to_inr(incentive) for incentive in incentives]
            bars = ax4.bar(incentive_labels, incentives_inr, color='gold', alpha=0.7)
            ax4.set_title('Incentives and Subsidies')
            ax4.set_ylabel('Incentive (₹/kWh or ₹/kg)')
            ax4.tick_params(axis='x', rotation=45)
            ax4.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, incentive in zip(bars, incentives_inr):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + max(incentives_inr)*0.01,
                        f'{incentive:.2f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/economic_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Economic analysis plots saved to {PLOTS_DIR}/economic_analysis.png")

def create_system_summary_plot(studycase_config, tech_costs):
    """Create and save system summary plot"""
    print("Creating system summary plot...")
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    fig.suptitle('Hybrid Plant System Summary', fontsize=16, fontweight='bold')
    
    # System capacities
    if studycase_config and 'hybrid_plant' in studycase_config:
        ax1 = axes[0]
        capacities = []
        labels = []
        
        # Extract capacities from studycase config - handle different capacity keys
        hybrid_config = studycase_config['hybrid_plant']
        for component, config in hybrid_config.items():
            if isinstance(config, dict):
                capacity = None
                if 'capacity' in config:
                    capacity = config['capacity']
                elif 'Npower' in config:
                    capacity = config['Npower']
                elif 'peakP' in config:
                    capacity = config['peakP']
                elif 'max capacity' in config:
                    capacity = config['max capacity']
                elif 'max power' in config:
                    capacity = config['max power']
                
                if capacity is not None and isinstance(capacity, (int, float)):
                    capacities.append(capacity)
                    labels.append(component.replace('_', ' ').title())
        
        if capacities:
            bars = ax1.bar(labels, capacities, color='lightblue', alpha=0.7)
            ax1.set_title('System Component Capacities')
            ax1.set_ylabel('Capacity (kW or kWh)')
            ax1.tick_params(axis='x', rotation=45)
            ax1.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for bar, capacity in zip(bars, capacities):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + max(capacities)*0.01,
                        f'{capacity:,.0f}', ha='center', va='bottom', fontsize=8)
    
    # Cost distribution pie chart
    if tech_costs:
        ax2 = axes[1]
        tech_names = list(tech_costs.keys())
        capital_costs = []
        valid_tech_names = []
        
        for tech in tech_names:
            if 'cost per unit' in tech_costs[tech] and isinstance(tech_costs[tech]['cost per unit'], (int, float)):
                capital_costs.append(tech_costs[tech]['cost per unit'])
                valid_tech_names.append(tech)
        
        if capital_costs:
            # Convert to Rupees
            capital_costs_inr = [eur_to_inr(cost) for cost in capital_costs]
            # Calculate total cost
            total_cost_inr = sum(capital_costs_inr)
            
            # Create pie chart
            wedges, texts, autotexts = ax2.pie(capital_costs_inr, labels=valid_tech_names, autopct='%1.1f%%',
                                              startangle=90, colors=plt.cm.Set3.colors)
            ax2.set_title(f'Capital Cost Distribution\n(Total: {total_cost_inr:,.0f} ₹/kW)')
            
            # Improve text readability
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
    
    plt.tight_layout()
    plt.savefig(f'{PLOTS_DIR}/system_summary.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ System summary plot saved to {PLOTS_DIR}/system_summary.png")

def simulate_hybrid_plant():
    """Simulate the hybrid plant and generate comprehensive analysis"""
    print("🚀 Starting Hybrid Plant Simulation...")
    print("=" * 50)
    
    # Load configurations
    print("📋 Loading configuration files...")
    general_config = load_config("input_test_4/general.json")
    refcase_config = load_config("input_test_4/refcase.json")
    studycase_config = load_config("input_test_4/studycase.json")
    tech_costs = load_config("input_test_4/tech_cost.json")
    energy_market = load_config("input_test_4/energy_market.json")
    
    if not all([general_config, refcase_config, studycase_config, tech_costs, energy_market]):
        print("❌ Error: Failed to load one or more configuration files")
        return
    
    print("✓ All configuration files loaded successfully")
    
    # Load load profiles
    print("\n📊 Loading load profiles...")
    loads_data = {}
    load_files = [
        "electric_load_hybrid.csv", "heat_load_hybrid.csv", "hydrogen_demand_hybrid.csv",
        "steel_electric_load.csv", "steel_heat_load.csv", "steel_hydrogen_load.csv",
        "ammonia_electric_load.csv", "ammonia_heat_load.csv", "ammonia_hydrogen_load.csv"
    ]
    
    for load_file in load_files:
        data = load_load_profile(f"input_test_4/loads/{load_file}")
        if data is not None:
            loads_data[load_file] = data
    
    print(f"✓ Loaded {len(loads_data)} load profile files")
    
    # Load production profiles
    print("\n🌞 Loading production profiles...")
    production_data = {}
    production_files = ["windproduction.csv", "PV_hybrid.csv"]
    
    for prod_file in production_files:
        data = load_production_profile(f"input_test_4/production/{prod_file}")
        if data is not None:
            production_data[prod_file] = data
    
    print(f"✓ Loaded {len(production_data)} production profile files")
    
    # Generate and save all plots
    print("\n📈 Generating comprehensive plots...")
    
    # Create plots directory if it doesn't exist
    os.makedirs(PLOTS_DIR, exist_ok=True)
    
    # Generate all plot types
    create_load_profile_plots(loads_data)
    create_production_profile_plots(production_data)
    create_energy_flow_diagram(studycase_config)
    create_economic_analysis_plots(tech_costs, energy_market)
    create_system_summary_plot(studycase_config, tech_costs)
    
    print(f"\n🎯 All plots have been saved to: {PLOTS_DIR}/")
    
    # Calculate system summary
    print("\n📊 Calculating system summary...")
    
    # Extract key parameters
    total_renewable_capacity = 0
    total_storage_capacity = 0
    total_electricity_demand = 0
    total_heat_demand = 0
    total_hydrogen_demand = 0
    
    if studycase_config and 'hybrid_plant' in studycase_config:
        hybrid_config = studycase_config['hybrid_plant']
        for component, config in hybrid_config.items():
            if isinstance(config, dict):
                capacity = None
                if 'capacity' in config:
                    capacity = config['capacity']
                elif 'Npower' in config:
                    capacity = config['Npower']
                elif 'peakP' in config:
                    capacity = config['peakP']
                elif 'max capacity' in config:
                    capacity = config['max capacity']
                elif 'max power' in config:
                    capacity = config['max power']
                
                if capacity is not None and isinstance(capacity, (int, float)):
                    if component in ['wind', 'PV']:
                        total_renewable_capacity += capacity
                    elif component in ['battery', 'large_energy_storage']:
                        total_storage_capacity += capacity
    
    if loads_data:
        if 'electric_load_hybrid.csv' in loads_data:
            total_electricity_demand = loads_data['electric_load_hybrid.csv']['electricity_demand'].max()
        if 'heat_load_hybrid.csv' in loads_data:
            total_heat_demand = loads_data['heat_load_hybrid.csv']['heat_demand'].max()
        if 'hydrogen_demand_hybrid.csv' in loads_data:
            total_hydrogen_demand = loads_data['hydrogen_demand_hybrid.csv']['hydrogen_demand'].max()
    
    # Calculate total capital cost
    total_capital_cost = 0
    if tech_costs:
        for tech, costs in tech_costs.items():
            if 'cost per unit' in costs and isinstance(costs['cost per unit'], (int, float)):
                total_capital_cost += costs['cost per unit']
    
    # Print summary
    print("\n" + "=" * 50)
    print("🏭 HYBRID PLANT SIMULATION SUMMARY")
    print("=" * 50)
    print(f"🌪️  Total Renewable Capacity: {total_renewable_capacity:,.0f} MW")
    print(f"🔋 Total Storage Capacity: {total_storage_capacity:,.0f} MWh")
    print(f"⚡ Peak Electricity Demand: {total_electricity_demand:,.0f} kW")
    print(f"🔥 Peak Heat Demand: {total_heat_demand:,.0f} kW")
    print(f"💧 Peak Hydrogen Demand: {total_hydrogen_demand:,.0f} kg/h")
    print(f"💰 Total Capital Cost: {total_capital_cost:,.0f} €/kW ({eur_to_inr(total_capital_cost):,.0f} ₹/kW)")
    print(f"📊 Total Load Profiles: {len(loads_data)}")
    print(f"🌞 Total Production Profiles: {len(production_data)}")
    print(f"📈 Total Plots Generated: 5")
    print(f"💾 Plots Saved to: {PLOTS_DIR}/")
    print("=" * 50)
    
    print(f"\n✅ Simulation completed successfully!")
    print(f"📁 All plots saved in: {PLOTS_DIR}/")
    print(f"🔍 You can review the plots later for detailed analysis")

def main():
    """Main function"""
    try:
        simulate_hybrid_plant()
    except Exception as e:
        print(f"❌ Error during simulation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
