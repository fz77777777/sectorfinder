import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="Institutional Volume Heatmap Scanner", layout="wide")
st.title("🔥 Smart Money Multi-Day Industry Volume Heatmap")
st.write("Yeh advance scanner multiple days ke lookback par industries aur stocks me hone wali institutional buying (Volume Spikes) ko track karta hai.")

# 1. Mega Database with Large, Mid, & Small Caps mapped to exact Industry
@st.cache_data
def get_mega_stock_database():
    stocks_data = [
        # --- RAILWAYS ---
        {"ticker": "IRFC.NS", "name": "IRFC", "industry": "Railways", "cap": "Large Cap"},
        {"ticker": "RVNL.NS", "name": "RVNL", "industry": "Railways", "cap": "Mid Cap"},
        {"ticker": "IRCON.NS", "name": "IRCON", "industry": "Railways", "cap": "Mid Cap"},
        {"ticker": "RAILTEL.NS", "name": "RailTEL", "industry": "Railways", "cap": "Small Cap"},
        {"ticker": "TITAGARH.NS", "name": "Titagarh Rail", "industry": "Railways", "cap": "Small Cap"},
        {"ticker": "TEXRAIL.NS", "name": "Texmaco Rail", "industry": "Railways", "cap": "Small Cap"},
        
        # --- DEFENSE ---
        {"ticker": "HAL.NS", "name": "Hindustan Aeronautics", "industry": "Defense", "cap": "Large Cap"},
        {"ticker": "BEL.NS", "name": "Bharat Electronics", "industry": "Defense", "cap": "Large Cap"},
        {"ticker": "MAZDOCK.NS", "name": "Mazagon Dock", "industry": "Defense", "cap": "Mid Cap"},
        {"ticker": "COCHINSHIP.NS", "name": "Cochin Shipyard", "industry": "Defense", "cap": "Mid Cap"},
        {"ticker": "BDL.NS", "name": "Bharat Dynamics", "industry": "Defense", "cap": "Mid Cap"},
        {"ticker": "BEML.NS", "name": "BEML Limited", "industry": "Defense", "cap": "Small Cap"},
        
        # --- GREEN ENERGY & POWER ---
        {"ticker": "NTPC.NS", "name": "NTPC", "industry": "Green Energy & Power", "cap": "Large Cap"},
        {"ticker": "TATAPOWER.NS", "name": "Tata Power", "industry": "Green Energy & Power", "cap": "Large Cap"},
        {"ticker": "SUZLON.NS", "name": "Suzlon Energy", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        {"ticker": "IREDA.NS", "name": "IREDA", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        {"ticker": "SJVN.NS", "name": "SJVN", "industry": "Green Energy & Power", "cap": "Mid Cap"},
        {"ticker": "NHPC.NS", "name": "NHPC", "industry": "Green Energy & Power", "cap": "Large Cap"},
        {"ticker": "KPIGREEN.NS", "name": "KPI Green Energy", "industry": "Green Energy & Power", "cap": "Small Cap"},
        
        # --- BANKING & FINANCE ---
        {"ticker": "HDFCBANK.NS", "name": "HDFC Bank", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "ICICIBANK.NS", "name": "ICICI Bank", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "SBIN.NS", "name": "State Bank of India", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "PNB.NS", "name": "Punjab National Bank", "industry": "Banking & Finance", "cap": "Large Cap"},
        {"ticker": "IDFCFIRSTB.NS", "name": "IDFC First Bank", "industry": "Banking & Finance", "cap": "Mid Cap"},
        {"ticker": "UNIONBANK.NS", "name": "Union Bank", "industry": "Banking & Finance", "cap": "Mid Cap"},
        {"ticker": "SOUTHBANK.NS", "name": "South Indian Bank", "industry": "Banking & Finance", "cap": "Small Cap"},
        
        # --- IT & SOFTWARE ---
        {"ticker": "TCS.NS", "name": "TCS", "industry": "IT & Software", "cap": "Large Cap"},
        {"ticker": "INFY.NS", "name": "Infosys", "industry": "IT & Software", "cap": "Large Cap"},
        {"ticker": "WIPRO.NS", "name": "Wipro", "industry": "IT & Software", "cap": "Large Cap"},
        {"ticker": "KPITTECH.NS", "name": "KPIT Technologies", "industry": "IT & Software", "cap": "Mid Cap"},
        {"ticker": "TATAELXSI.NS", "name": "Tata Elxsi", "industry": "IT & Software", "cap": "Mid Cap"},
        {"ticker": "ZENSARTECH.NS", "name": "Zensar Tech", "industry": "IT & Software", "cap": "Small Cap"},
        {"ticker": "HAPPSTMND.NS", "name": "Happiest Minds", "industry": "IT & Software", "cap": "Small Cap"},
        
        # --- CHEMICALS & FERTILIZERS ---
        {"ticker": "SRF.NS", "name": "SRF Limited", "industry": "Chemicals", "cap": "Large Cap"},
        {"ticker": "TATACHEM.NS", "name": "Tata Chemicals", "industry": "Chemicals", "cap": "Mid Cap"},
        {"ticker": "DEEPAKNTR.NS", "name": "Deepak Nitrite", "industry": "Chemicals", "cap": "Mid Cap"},
        {"ticker": "FACT.NS", "name": "FACT", "industry": "Chemicals", "cap": "Mid Cap"},
        {"ticker": "GNFC.NS", "name": "GNFC", "industry": "Chemicals", "cap": "Small Cap"},
        {"ticker": "RCF.NS", "name": "Rashtriya Chemicals", "industry": "Chemicals", "cap": "Small Cap"},
        
        # --- INFRASTRUCTURE & REALTY ---
        {"ticker": "LT.NS", "name": "Larsen & Toubro", "industry": "Infrastructure & Realty", "cap": "Large Cap"},
        {"ticker": "DLF.NS", "name": "DLF", "industry": "Infrastructure & Realty", "cap": "Large Cap"},
        {"ticker": "GMRINFRA.NS", "name": "GMR Infra", "industry": "Infrastructure & Realty", "cap": "Mid Cap"},
        {"ticker": "GODREJPROP.NS", "name": "Godrej Properties", "industry": "Infrastructure & Realty", "cap": "Mid Cap"},
        {"ticker": "NBCC.NS", "name": "NBCC India", "industry": "Infrastructure & Realty", "cap": "Small Cap"},
        {"ticker": "ITDCEM.NS", "name": "ITD Cementation", "industry": "Infrastructure & Realty", "cap": "Small Cap"},
        
        # --- AUTOMOBILES & EV ---
        {"ticker": "TATAMOTORS.NS", "name": "Tata Motors", "industry": "Automobiles & EV", "cap": "Large Cap"},
        {"ticker": "M&M.NS", "name": "Mahindra & Mahindra", "industry": "Automobiles & EV", "cap": "Large Cap"},
        {"ticker": "MARUTI.NS", "name": "Maruti Suzuki", "industry": "Automobiles & EV", "cap": "Large Cap"},
        {"ticker": "TVSMOTOR.NS", "name": "TVS Motor", "industry": "Automobiles & EV", "cap": "Large Cap"},
        {"ticker": "AMARAJABAT.NS", "name": "Amara Raja Energy", "industry": "Automobiles & EV", "cap": "Mid Cap"},
        {"ticker": "OLECTRA.NS", "name": "Olectra Greentech", "industry": "Automobiles & EV", "cap": "Small Cap"},
        
        # --- PHARMA & HEALTHCARE ---
        {"ticker": "SUNPHARMA.NS", "name": "Sun Pharma", "industry": "Pharma & Healthcare", "cap": "Large Cap"},
        {"ticker": "CIPLA.NS", "name": "Cipla", "industry": "Pharma & Healthcare", "cap": "Large Cap"},
        {"ticker": "DRREDDY.NS", "name": "Dr Reddy's Labs", "industry": "Pharma & Healthcare", "cap": "Large Cap"},
        {"ticker": "LUPIN.NS", "name": "Lupin", "industry": "Pharma & Healthcare", "cap": "Mid Cap"},
        {"ticker": "GLENMARK.NS", "name": "Glenmark Pharma", "industry": "Pharma & Healthcare", "cap": "Mid Cap"},
        {"ticker": "JUBLPHARMA.NS", "name": "Jubilant Pharma", "industry": "Pharma & Healthcare", "cap": "Small Cap"},
        
        # --- METALS & MINING ---
        {"ticker": "TATASTEEL.NS", "name": "Tata Steel", "industry": "Metals & Mining", "cap": "Large Cap"},
        {"ticker": "JSWSTEEL.NS", "name": "JSW Steel", "industry": "Metals & Mining", "cap": "Large Cap"},
        {"ticker": "HINDALCO.NS", "name": "Hindalco", "industry": "Metals & Mining", "cap": "Large Cap"},
        {"ticker": "SAIL.NS", "name": "SAIL", "industry": "Metals & Mining", "cap": "Mid Cap"},
        {"ticker": "NMDC.NS", "name": "NMDC", "industry": "Metals & Mining", "cap": "Mid Cap"},
        {"ticker": "JINDALSTEL.NS", "name": "Jindal Steel", "industry": "Metals & Mining", "cap": "Mid Cap"},
        {"ticker": "MAHSEAMLES.NS", "name": "Maharashtra Seamless", "industry": "Metals & Mining", "cap": "Small Cap"}
    ]
    return pd.DataFrame(stocks_data)

# 2. Advanced Multi-Day Volume Engine
def fetch_multiday_volume(df_db, lookback_days):
    tickers = df_db['ticker'].tolist()
    total_period = "3mo" if lookback_days <= 3 else "6mo"
    
    data = yf.download(tickers, period=total_period, progress=False)
    if data.empty or 'Volume' not in data.columns or 'Close' not in data.columns:
        st.error("Yahoo Finance server connectivity issue. Refresh kijiye.")
        return pd.DataFrame()
        
    volume_df = data['Volume'].ffill().bfill()
    close_df = data['Close'].ffill().bfill()
    
    results = []
    for _, row in df_db.iterrows():
        t = row['ticker']
        if t in volume_df.columns and len(volume_df[t]) >= (lookback_days + 20):
            current_window_vol = volume_df[t].iloc[-lookback_days:].sum()
            historical_base_avg = volume_df[t].iloc[:-lookback_days].tail(20).mean() * lookback_days
            
            price_initial = close_df[t].iloc[-lookback_days - 1]
            price_final = close_df[t].iloc[-1]
            price_delta_pct = ((price_final - price_initial) / price_initial) * 100
            
            if historical_base_avg > 0:
                spike_ratio = current_window_vol / historical_base_avg
                results.append({
                    "ticker": t,
                    "name": row['name'],
                    "industry": row['industry'],
                    "cap": row['cap'],
                    "current_volume": int(current_window_vol),
                    "base_volume": int(historical_base_avg),
                    "volume_spike": round(spike_ratio, 2),
                    "price_change_%": round(price_delta_pct, 2)
                })
    return pd.DataFrame(results)

# --- UI Controls Configuration Sidebar ---
st.sidebar.header("🎯 Scanner Setup")

lookback_label = st.sidebar.selectbox(
    "Choose Analysis Window", 
    ["Yesterday (1 Day)", "Past 3 Days", "Past 7 Days", "Past 15 Days"]
)
duration_map = {
    "Yesterday (1 Day)": 1,
    "Past 3 Days": 3,
    "Past 7 Days": 7,
    "Past 15 Days": 15
}
days_selected = duration_map[lookback_label]

market_cap_filter = st.sidebar.selectbox("Market Cap Universe", ["All Caps (Large+Mid+Small)", "Large Cap", "Mid Cap", "Small Cap"])

# Load Database core
df_db = get_mega_stock_database()

with st.spinner("Processing High-Volume Inflows... Please wait."):
    df_raw_stocks = fetch_multiday_volume(df_db, days_selected)

if not df_raw_stocks.empty:
    if market_cap_filter != "All Caps (Large+Mid+Small)":
        df_raw_stocks = df_raw_stocks[df_raw_stocks['cap'] == market_cap_filter]
        
    # Aggregate data to generate clean industry metrics
    industry_stats = df_raw_stocks.groupby('industry').agg(
        Total_Current=('current_volume', 'sum'),
        Total_Base=('base_volume', 'sum'),
        Avg_Price_Chg=('price_change_%', 'mean')
    ).reset_index()
    
    industry_stats['Industry_Spike'] = (industry_stats['Total_Current'] / industry_stats['Total_Base']).round(2)
    
    # Sort industry from Top high volume to low volume spike automatically
    industry_stats = industry_stats.sort_values(by='Industry_Spike', ascending=False).reset_index(drop=True)
    
    st.subheader(f"📊 Live Industry Volume Heatmap ({lookback_label})")
    st.write("Sectors high-volume inflows ke basis par sorted hain. **Green** represent karta hai abnormal institutional buying.")
    
    # 3. Dynamic Colorful Heatmap Interface Render
    for idx, row in industry_stats.iterrows():
        spike = row['Industry_Spike']
        
        # HEATMAP COLOR DESIGN LOGIC
        if spike >= 2.0:
            bg_color = "#1E4620"   # Dark Forest Green
            text_color = "#2ECC71"
            status_badge = "🟢 BLOCKBUSTER ACCUMULATION"
        elif spike >= 1.3:
            bg_color = "#2D5A27"   # Olive Green
            text_color = "#A9DFBF"
            status_badge = "🟩 HEAVY BUYING"
        elif spike >= 0.9:
            bg_color = "#4A4A4A"   # Dark Grey
            text_color = "#E5E7E9"
            status_badge = "⬜ NORMAL CHURN"
        else:
            bg_color = "#641E16"   # Deep Crimson/Muted Red
            text_color = "#F5B7B1"
            status_badge = "🚨 VOLUME DRY / DRIFTING"

        custom_header = f"⚡ #{idx+1} {row['industry'].upper()}  ➔  Spike: {spike}x  |  Avg Returns: {row['Avg_Price_Chg']:.2f}%  |  [{status_badge}]"
        
        with st.expander(custom_header):
            st.markdown(
                f"<div style='background-color:{bg_color}; padding:12px; border-radius:6px; margin-bottom:10px;'>"
                f"<span style='color:{text_color}; font-weight:bold;'>Heatmap Insights:</span> "
                f"This segment processed {spike}x relative volume benchmarking baseline settings. "
                f"</div>", 
                unsafe_allow_html=True
            )
            
            constituent_stocks = df_raw_stocks[df_raw_stocks['industry'] == row['industry']].copy()
            constituent_stocks = constituent_stocks.sort_values(by='volume_spike', ascending=False)
            
            ui_table = constituent_stocks[['name', 'ticker', 'cap', 'volume_spike', 'price_change_%']].copy()
            ui_table.columns = ['Stock Name', 'Ticker Code', 'Market Cap Class', 'Volume Spike Factor', 'Price Shift Percentage']
            
            st.dataframe(
                ui_table.style.background_gradient(subset=['Volume Spike Factor'], cmap='Greens' if spike >= 1.3 else 'Reds')
                             .format({'Price Shift Percentage': '{:.2f}%', 'Volume Spike Factor': '{:.2f}x'}),
                use_container_width=True,
                hide_index=True
            )
else:
    st.warning("Filters configuration setup mismatch. Please change the Market Cap parameters to refresh calculations.")
