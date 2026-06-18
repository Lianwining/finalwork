import streamlit as st

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
    page_title="贪吃蛇游戏",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🐍 贪吃蛇游戏")
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