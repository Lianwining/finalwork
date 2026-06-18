import streamlit as st
import os

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
    page_title="五行性格测试",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 独立的五行性格测试页面
st.title("🌟 五行性格测试")

current_dir = os.path.dirname(os.path.abspath(__file__))
q_path = os.path.join(current_dir, "data", "question.json")
r_path = os.path.join(current_dir, "data", "result.json")

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

import json
questions = load_json(q_path)
results = load_json(r_path)

if "test_score" not in st.session_state:
    st.session_state.test_score = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "test_finished" not in st.session_state:
    st.session_state.test_finished = False

if not st.session_state.test_finished:
    idx = st.session_state.current_q
    if idx < len(questions):
        q = questions[idx]
        st.progress((idx + 1) / len(questions))
        st.subheader(f"问题 {idx + 1}/{len(questions)}")
        st.write(q['q'])
        
        options = [opt['text'] for opt in q['options']]
        choice = st.radio("请选择你的答案：", options, key=f"q_{idx}")
        
        if st.button("下一题", key=f"next_{idx}"):
            selected_idx = options.index(choice)
            key = list(q['options'][selected_idx]['score'].keys())[0]
            val = list(q['options'][selected_idx]['score'].values())[0]
            st.session_state.test_score[key] += val
            st.session_state.answers.append(choice)
            st.session_state.current_q += 1
            st.rerun()
    else:
        st.session_state.test_finished = True
        st.rerun()
else:
    st.success("测试完成！")
    st.subheader("📊 你的五行得分")
    
    cols = st.columns(5)
    elements = ["木", "火", "土", "金", "水"]
    
    for i, (elem, col) in enumerate(zip(elements, cols)):
        with col:
            st.metric(elem, st.session_state.test_score[elem])
    
    max_key = max(st.session_state.test_score, key=st.session_state.test_score.get)
    st.subheader(f"🎯 你的五行属性：【{max_key}】")
    st.info(results[max_key])
    
    st.subheader("📝 答题记录")
    for i, (q, ans) in enumerate(zip(questions, st.session_state.answers), 1):
        st.write(f"{i}. {q['q']} → **{ans}**")
    
    if st.button("重新测试"):
        st.session_state.test_score = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
        st.session_state.current_q = 0
        st.session_state.answers = []
        st.session_state.test_finished = False
        st.rerun()