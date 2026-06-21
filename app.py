import streamlit as st
import os
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.set_page_config(page_title="期末组队项目", layout="wide")

st.title("🎯 期末组队项目")
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["🌟 五行性格测试", "🌤️ 天气预报", "🤖 AI聊天机器人", "🐍 贪吃蛇游戏"])

with tab1:
    st.subheader("🌟 五行性格测试")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    q_path = os.path.join(current_dir, "data", "question.json")
    r_path = os.path.join(current_dir, "data", "result.json")
    
    def load_json(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
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
        
        if st.button("重新测试", key="restart_test"):
            st.session_state.test_score = {"木": 0, "火": 0, "土": 0, "金": 0, "水": 0}
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.session_state.test_finished = False
            st.rerun()

with tab2:
    st.subheader("🌤️ 天气预报")
    
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

with tab3:
    st.subheader("🤖 AI聊天机器人 (DeepSeek)")
    
    API_KEY = st.secrets.get("AI_API_KEY", "") or os.environ.get("AI_API_KEY", "")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    if prompt := st.chat_input("请输入你的问题..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        if API_KEY:
            try:
                import requests
                url = "https://api.deepseek.com/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                }
                data = {
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}]
                }
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                reply = response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                reply = f"AI 调用失败：{str(e)}"
        else:
            reply = f"你说的是：{prompt}（未配置 AI_API_KEY 环境变量）"
        
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

with tab4:
    st.subheader("🐍 贪吃蛇游戏")
    st.write("使用 方向键 或 WASD 控制方向，吃食物增长蛇身！支持穿墙！")
    
    game_html = """
    <style>
    #snake-container {
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
    }
    #game-canvas {
        border: 4px solid #4CAF50;
        border-radius: 10px;
        background: #2d2d2d;
        display: block;
        margin: 0 auto;
    }
    #score-board {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #333;
        margin: 20px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    #game-over {
        display: none;
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 40px 60px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        z-index: 1000;
    }
    #game-over h2 {
        color: #e74c3c;
        font-size: 36px;
        margin: 0 0 15px 0;
    }
    #game-over p {
        font-size: 24px;
        color: #333;
        margin: 10px 0;
    }
    #game-over .restart-hint {
        font-size: 18px;
        color: #666;
        margin-top: 20px;
    }
    .controls {
        text-align: center;
        margin-top: 15px;
        color: #666;
        font-size: 14px;
    }
    .controls span {
        display: inline-block;
        background: #eee;
        padding: 5px 12px;
        border-radius: 5px;
        margin: 2px;
    }
    </style>
    <div id="snake-container">
        <div id="score-board">得分: 0</div>
        <canvas id="game-canvas" width="400" height="400"></canvas>
        <div class="controls">
            <span>↑</span> <span>↓</span> <span>←</span> <span>→</span> 或 <span>W</span><span>A</span><span>S</span><span>D</span> 控制方向
        </div>
    </div>
    <div id="game-over">
        <h2>游戏结束!</h2>
        <p>最终得分: <span id="final-score">0</span></p>
        <p>蛇身长度: <span id="snake-length">3</span></p>
        <p class="restart-hint">按 空格键 或 点击屏幕 重新开始</p>
    </div>
    <script>
    const canvas = document.getElementById('game-canvas');
    const ctx = canvas.getContext('2d');
    const scoreBoard = document.getElementById('score-board');
    const gameOverScreen = document.getElementById('game-over');
    const finalScoreDisplay = document.getElementById('final-score');
    const snakeLengthDisplay = document.getElementById('snake-length');
    
    const gridSize = 20;
    const tileCount = 20;
    let snake = [];
    let food = {x: 10, y: 10};
    let dx = 0;
    let dy = 0;
    let score = 0;
    let isGameRunning = false;
    let isGameOver = false;
    let gameInterval;
    
    function initGame() {
        snake = [
            {x: 10, y: 10},
            {x: 9, y: 10},
            {x: 8, y: 10}
        ];
        score = 0;
        dx = 1;
        dy = 0;
        isGameRunning = true;
        isGameOver = false;
        scoreBoard.textContent = '得分: 0';
        gameOverScreen.style.display = 'none';
        placeFood();
        if (gameInterval) clearInterval(gameInterval);
        gameInterval = setInterval(update, 180);
    }
    
    function update() {
        if (!isGameRunning) return;
        moveSnake();
        checkCollision();
        draw();
    }
    
    function moveSnake() {
        const head = {x: snake[0].x + dx, y: snake[0].y + dy};
    
        if (head.x < 0) head.x = tileCount - 1;
        if (head.x >= tileCount) head.x = 0;
        if (head.y < 0) head.y = tileCount - 1;
        if (head.y >= tileCount) head.y = 0;
    
        snake.unshift(head);
        if (head.x === food.x && head.y === food.y) {
            score += 10;
            scoreBoard.textContent = '得分: ' + score;
            placeFood();
        } else {
            snake.pop();
        }
    }
    
    function checkCollision() {
        const head = snake[0];
        for (let i = 1; i < snake.length; i++) {
            if (head.x === snake[i].x && head.y === snake[i].y) {
                gameOver();
                return;
            }
        }
    }
    
    function placeFood() {
        let newFood;
        do {
            newFood = {
                x: Math.floor(Math.random() * tileCount),
                y: Math.floor(Math.random() * tileCount)
            };
        } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
        food = newFood;
    }
    
    function draw() {
        ctx.fillStyle = '#2d2d2d';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    
        ctx.strokeStyle = '#3d3d3d';
        ctx.lineWidth = 1;
        for (let i = 0; i <= tileCount; i++) {
            ctx.beginPath();
            ctx.moveTo(i * gridSize, 0);
            ctx.lineTo(i * gridSize, canvas.height);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(0, i * gridSize);
            ctx.lineTo(canvas.width, i * gridSize);
            ctx.stroke();
        }
    
        ctx.fillStyle = '#e74c3c';
        ctx.shadowColor = '#e74c3c';
        ctx.shadowBlur = 10;
        ctx.beginPath();
        ctx.arc(food.x * gridSize + gridSize/2, food.y * gridSize + gridSize/2, gridSize/2 - 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;
    
        snake.forEach((segment, index) => {
            const gradient = ctx.createLinearGradient(
                segment.x * gridSize, segment.y * gridSize,
                segment.x * gridSize + gridSize, segment.y * gridSize + gridSize
            );
            if (index === 0) {
                gradient.addColorStop(0, '#2ecc71');
                gradient.addColorStop(1, '#27ae60');
            } else {
                const alpha = 1 - (index / snake.length) * 0.5;
                gradient.addColorStop(0, `rgba(46, 204, 113, ${alpha})`);
                gradient.addColorStop(1, `rgba(39, 174, 96, ${alpha})`);
            }
            ctx.fillStyle = gradient;
            ctx.shadowColor = '#2ecc71';
            ctx.shadowBlur = index === 0 ? 15 : 5;
            ctx.beginPath();
            ctx.roundRect(segment.x * gridSize + 2, segment.y * gridSize + 2, gridSize - 4, gridSize - 4, 5);
            ctx.fill();
            ctx.shadowBlur = 0;
    
            if (index === 0) {
                ctx.fillStyle = '#fff';
                const eyeSize = 4;
                const eyeOffset = 5;
                if (dx === 1) {
                    ctx.beginPath();
                    ctx.arc(segment.x * gridSize + gridSize - eyeOffset, segment.y * gridSize + eyeOffset, eyeSize, 0, Math.PI * 2);
                    ctx.arc(segment.x * gridSize + gridSize - eyeOffset, segment.y * gridSize + gridSize - eyeOffset, eyeSize, 0, Math.PI * 2);
                    ctx.fill();
                } else if (dx === -1) {
                    ctx.beginPath();
                    ctx.arc(segment.x * gridSize + eyeOffset, segment.y * gridSize + eyeOffset, eyeSize, 0, Math.PI * 2);
                    ctx.arc(segment.x * gridSize + eyeOffset, segment.y * gridSize + gridSize - eyeOffset, eyeSize, 0, Math.PI * 2);
                    ctx.fill();
                } else if (dy === -1) {
                    ctx.beginPath();
                    ctx.arc(segment.x * gridSize + eyeOffset, segment.y * gridSize + eyeOffset, eyeSize, 0, Math.PI * 2);
                    ctx.arc(segment.x * gridSize + gridSize - eyeOffset, segment.y * gridSize + eyeOffset, eyeSize, 0, Math.PI * 2);
                    ctx.fill();
                } else {
                    ctx.beginPath();
                    ctx.arc(segment.x * gridSize + eyeOffset, segment.y * gridSize + gridSize - eyeOffset, eyeSize, 0, Math.PI * 2);
                    ctx.arc(segment.x * gridSize + gridSize - eyeOffset, segment.y * gridSize + gridSize - eyeOffset, eyeSize, 0, Math.PI * 2);
                    ctx.fill();
                }
            }
        });
    }
    
    function gameOver() {
        isGameRunning = false;
        isGameOver = true;
        clearInterval(gameInterval);
        finalScoreDisplay.textContent = score;
        snakeLengthDisplay.textContent = snake.length;
        gameOverScreen.style.display = 'block';
    }
    
    document.addEventListener('keydown', function(e) {
        if (isGameOver && e.code === 'Space') {
            initGame();
            return;
        }
        if (!isGameRunning) {
            initGame();
        }
    
        const key = e.key.toLowerCase();
        if ((key === 'arrowup' || key === 'w') && dy !== 1) {
            dx = 0; dy = -1;
        } else if ((key === 'arrowdown' || key === 's') && dy !== -1) {
            dx = 0; dy = 1;
        } else if ((key === 'arrowleft' || key === 'a') && dx !== 1) {
            dx = -1; dy = 0;
        } else if ((key === 'arrowright' || key === 'd') && dx !== -1) {
            dx = 1; dy = 0;
        }
        e.preventDefault();
    });
    
    canvas.addEventListener('click', function() {
        if (isGameOver) {
            initGame();
        } else if (!isGameRunning) {
            initGame();
        }
    });
    
    draw();
    </script>
    """
    
    st.components.v1.html(game_html, height=550)

st.markdown("---")
st.markdown("#### 📌 使用说明")
st.markdown("""
- 使用顶部选项卡切换不同功能模块
- 五行性格测试：通过答题了解你的五行属性
- 天气预报：查看今日天气和近7天温度变化趋势
- AI聊天机器人：与DeepSeek AI对话（需配置AI_API_KEY环境变量）
- 贪吃蛇游戏：使用方向键或WASD控制，支持穿墙效果
""")
