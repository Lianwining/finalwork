import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# 隐藏Streamlit默认元素，实现完全独立的页面
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
.stAppHeader {display: none !important;}
.stAppToolbar {display: none !important;}
.css-1d391kg {padding-top: 0rem;}
.css-18e3ste {padding-top: 0rem;}
.block-container {padding-top: 0rem !important;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 设置独立的页面配置
st.set_page_config(
    page_title="天气预报",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🌤️ 天气预报")

today = datetime.now()
dates = []
for i in range(7):
    date = today + timedelta(days=i)
    if i == 0:
        dates.append(f"{date.month}月{date.day}日 (今天)")
    elif i == 1:
        dates.append(f"{date.month}月{date.day}日 (明天)")
    else:
        dates.append(f"{date.month}月{date.day}日")

weather_data = {
    "日期": dates,
    "最高温度": [32, 33, 30, 28, 29, 31, 32],
    "最低温度": [24, 25, 23, 22, 23, 24, 25],
    "天气状况": ["☀️ 晴", "⛅ 多云", "🌧️ 小雨", "☁️ 阴", "⛅ 多云", "☀️ 晴", "☀️ 晴"],
    "湿度": [65, 70, 80, 75, 68, 60, 58],
    "风速": ["微风", "轻风", "和风", "轻风", "微风", "微风", "轻风"]
}

weather_df = pd.DataFrame(weather_data)

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("🌡️ 今日天气")
    st.metric(label="当前温度", value="32°C", delta="+2°C")
    st.markdown(f"**日期:** {today.month}月{today.day}日")
    st.markdown("**天气状况:** ☀️ 晴")
    st.markdown("**湿度:** 65%")
    st.markdown("**风速:** 微风")
    st.markdown("**紫外线:** 强")
    st.markdown("**穿衣建议:** 短袖、短裤")

with col2:
    st.subheader("📈 近7天温度变化")
    fig = px.line(weather_df, x="日期", y=["最高温度", "最低温度"], 
                  markers=True, 
                  labels={"value": "温度 (°C)", "variable": "类型"},
                  title="温度趋势")
    fig.update_layout(yaxis_title="温度 (°C)")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 7天天气预报详情")
st.dataframe(weather_df, use_container_width=True)