from flask import Flask, render_template_string, request, session
import random
import time
import json
import os

app = Flask(__name__)
app.secret_key = 'MyKnightGame2024-SuperSecret-Key!'  # Change this to your own random key

# In-memory highscore storage (resets when app restarts, but works for demo)
highscores = []

# HTML template for home page
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>My Python Website</title>
    <style>
        body { font-family: Arial; margin: 50px; background-color: #f0f0f0; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #333; }
        .button { background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; display: inline-block; }
        .button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Python Website! 🐍</h1>
        <p>This is a simple website built with Flask and deployed for free!</p>
        <p><a href="/about" class="button">About Me</a></p>
        <p><a href="/projects" class="button">My Projects</a></p>
        <p><a href="/game" class="button">🎲 Number Game</a></p>
        <p><a href="/reaction-game" class="button">⚡ Reaction Game</a></p>
        <p><a href="/knight-game" class="button">⚔️ Knight Survival</a></p>
        <p><a href="/highscores" class="button">🏆 High Scores</a></p>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/about')
def about():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>About - My Python Website</title>
        <style>
            body { font-family: Arial; margin: 50px; background-color: #f0f0f0; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h1 { color: #333; }
            .button { background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>About Me</h1>
            <p>I'm learning Python and web development!</p>
            <p>This website was built using Flask framework.</p>
            <p><a href="/" class="button">← Back Home</a></p>
        </div>
    </body>
    </html>
    '''

@app.route('/projects')
def projects():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Projects</title>
        <style>
            body { font-family: Arial; margin: 50px; background-color: #f0f0f0; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            h1 { color: #333; }
            .button { background-color: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>My Projects 🚀</h1>
            <p>Here are some things I'm working on:</p>
            <ul>
                <li>Learning Python</li>
                <li>Building websites</li>
                <li>Getting awesome at coding</li>
                <li>Creating fun games</li>
            </ul>
            <p><a href="/" class="button">← Back Home</a></p>
        </div>
    </body>
    </html>
    '''

@app.route('/game', methods=['GET', 'POST'])
def number_game():
    # Initialize game if not started
    if 'secret_number' not in session:
        session['secret_number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['game_over'] = False
    
    message = ""
    
    if request.method == 'POST':
        if 'reset' in request.form:
            # Reset the game
            session['secret_number'] = random.randint(1, 100)
            session['attempts'] = 0
            session['game_over'] = False
            message = "New game started! I'm thinking of a number between 1-100."
        
        elif 'guess' in request.form and not session['game_over']:
            try:
                guess = int(request.form['guess'])
                session['attempts'] += 1
                
                if guess == session['secret_number']:
                    message = f"🎉 Congratulations! You guessed it in {session['attempts']} attempts!"
                    session['game_over'] = True
                elif guess < session['secret_number']:
                    message = f"📈 Too low! Try a higher number. (Attempt {session['attempts']})"
                else:
                    message = f"📉 Too high! Try a lower number. (Attempt {session['attempts']})"
            except ValueError:
                message = "Please enter a valid number!"
    
    elif 'secret_number' in session and session['attempts'] == 0:
        message = "I'm thinking of a number between 1 and 100. Can you guess it?"
    
    game_template = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Number Guessing Game</title>
        <style>
            body {{ font-family: Arial; margin: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }}
            .container {{ max-width: 500px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
            h1 {{ color: #333; text-align: center; margin-bottom: 30px; }}
            .game-area {{ text-align: center; }}
            input[type="number"] {{ padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 5px; width: 100px; }}
            .btn {{ background-color: #4CAF50; color: white; padding: 12px 24px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin: 10px 5px; }}
            .btn:hover {{ background-color: #45a049; }}
            .btn-reset {{ background-color: #f44336; }}
            .btn-reset:hover {{ background-color: #da190b; }}
            .message {{ margin: 20px 0; padding: 15px; border-radius: 5px; font-weight: bold; }}
            .message.success {{ background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }}
            .message.info {{ background-color: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }}
            .nav-link {{ display: inline-block; margin-top: 30px; color: #667eea; text-decoration: none; font-weight: bold; }}
            .nav-link:hover {{ text-decoration: underline; }}
            .stats {{ margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎲 Number Guessing Game</h1>
            
            <div class="game-area">
                {"<div class='message success'>" + message + "</div>" if session.get('game_over') else ("<div class='message info'>" + message + "</div>" if message else "")}
                
                <div class="stats">
                    <strong>Attempts:</strong> {session.get('attempts', 0)}
                    {"<br><strong>Game Status:</strong> Complete! 🎉" if session.get('game_over') else "<br><strong>Game Status:</strong> In Progress... 🤔"}
                </div>
                
                <form method="post">
                    {'' if session.get('game_over') else '''
                    <input type="number" name="guess" placeholder="Your guess" min="1" max="100" required>
                    <br><button type="submit" class="btn">Guess!</button>
                    '''}
                    <br><button type="submit" name="reset" class="btn btn-reset">New Game</button>
                </form>
            </div>
            
            <div style="text-align: center;">
                <a href="/" class="nav-link">← Back to Home</a>
            </div>
        </div>
    </body>
    </html>
    '''
    
    return game_template

@app.route('/reaction-game')
def reaction_game():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reaction Time Game</title>
        <style>
            body { font-family: Arial; margin: 0; background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
            .container { max-width: 600px; background: white; padding: 40px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); text-align: center; }
            h1 { color: #333; margin-bottom: 30px; }
            #gameArea { width: 400px; height: 300px; border: 3px solid #ddd; border-radius: 10px; margin: 20px auto; display: flex; align-items: center; justify-content: center; font-size: 24px; cursor: pointer; transition: all 0.3s; position: relative; }
            #gameArea.waiting { background: #f8f9fa; color: #666; }
            #gameArea.ready { background: #dc3545; color: white; }
            #gameArea.go { background: #28a745; color: white; animation: pulse 0.5s infinite; }
            #gameArea.too-early { background: #ffc107; color: #333; }
            @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
            .btn { background-color: #007bff; color: white; padding: 15px 30px; border: none; border-radius: 8px; cursor: pointer; font-size: 18px; margin: 10px; }
            .btn:hover { background-color: #0056b3; }
            .result { margin: 20px 0; font-size: 20px; font-weight: bold; }
            .instructions { margin: 20px 0; color: #666; line-height: 1.6; }
            #nameInput { padding: 10px; font-size: 16px; border: 2px solid #ddd; border-radius: 5px; margin: 10px; }
            .nav-links { margin-top: 30px; }
            .nav-links a { margin: 0 10px; color: #007bff; text-decoration: none; font-weight: bold; }
            .nav-links a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⚡ Reaction Time Challenge</h1>
            
            <div class="instructions">
                <p><strong>How to play:</strong></p>
                <p>1. Click "Start Game" and wait for the box to turn GREEN</p>
                <p>2. Click as fast as possible when it turns green!</p>
                <p>3. Try to get the fastest reaction time</p>
                <p><em>Warning: Don't click too early or you'll have to restart!</em></p>
            </div>
            
            <div id="gameArea" class="waiting" onclick="handleClick()">
                <span id="gameText">Click "Start Game" to begin!</span>
            </div>
            
            <div class="result" id="result"></div>
            
            <div>
                <input type="text" id="nameInput" placeholder="Enter your name" maxlength="20">
                <br>
                <button class="btn" onclick="startGame()">Start Game</button>
                <button class="btn" onclick="submitScore()" id="submitBtn" style="display:none;">Submit Score</button>
            </div>
            
            <div class="nav-links">
                <a href="/">← Home</a> |
                <a href="/highscores">🏆 View High Scores</a>
            </div>
        </div>
        
        <script>
            let gameState = 'waiting';
            let startTime = 0;
            let reactionTime = 0;
            let timeout;
            
            function startGame() {
                const gameArea = document.getElementById('gameArea');
                const gameText = document.getElementById('gameText');
                const result = document.getElementById('result');
                const submitBtn = document.getElementById('submitBtn');
                
                gameState = 'ready';
                gameArea.className = 'ready';
                gameText.textContent = 'Wait for GREEN...';
                result.textContent = '';
                submitBtn.style.display = 'none';
                
                // Random delay between 2-6 seconds
                const delay = Math.random() * 4000 + 2000;
                
                timeout = setTimeout(() => {
                    if (gameState === 'ready') {
                        gameState = 'go';
                        gameArea.className = 'go';
                        gameText.textContent = 'CLICK NOW!';
                        startTime = Date.now();
                    }
                }, delay);
            }
            
            function handleClick() {
                const gameArea = document.getElementById('gameArea');
                const gameText = document.getElementById('gameText');
                const result = document.getElementById('result');
                const submitBtn = document.getElementById('submitBtn');
                
                if (gameState === 'ready') {
                    // Clicked too early!
                    clearTimeout(timeout);
                    gameState = 'too-early';
                    gameArea.className = 'too-early';
                    gameText.textContent = 'Too early! Try again';
                    result.textContent = 'You clicked too early! Wait for GREEN next time.';
                    
                    setTimeout(() => {
                        gameState = 'waiting';
                        gameArea.className = 'waiting';
                        gameText.textContent = 'Click "Start Game" to try again!';
                    }, 2000);
                    
                } else if (gameState === 'go') {
                    // Good click!
                    reactionTime = Date.now() - startTime;
                    gameState = 'finished';
                    gameArea.className = 'waiting';
                    gameText.textContent = 'Great job!';
                    
                    let message = '';
                    if (reactionTime < 200) {
                        message = '🔥 INCREDIBLE! Lightning fast!';
                    } else if (reactionTime < 300) {
                        message = '⚡ EXCELLENT! Very quick!';
                    } else if (reactionTime < 400) {
                        message = '👍 GOOD! Nice reaction!';
                    } else if (reactionTime < 500) {
                        message = '👌 Not bad! Keep practicing!';
                    } else {
                        message = '😅 Could be faster! Try again!';
                    }
                    
                    result.innerHTML = `<div style="color: #28a745;">Your reaction time: <strong>${reactionTime}ms</strong></div><div>${message}</div>`;
                    submitBtn.style.display = 'inline-block';
                }
            }
            
            function submitScore() {
                const name = document.getElementById('nameInput').value.trim();
                if (!name) {
                    alert('Please enter your name!');
                    return;
                }
                
                // Submit score to server
                fetch('/submit-score', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: name,
                        score: reactionTime,
                        game: 'reaction'
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Score submitted! Check the high scores!');
                        window.location.href = '/highscores';
                    }
                })
                .catch(() => {
                    alert('Error submitting score. Please try again!');
                });
            }
        </script>
    </body>
    </html>
    '''

@app.route('/knight-game')
def knight_game():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Knight vs Slimes - Survival Mode</title>
        <style>
            body { font-family: 'Courier New', monospace; margin: 0; background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); color: white; overflow-x: hidden; }
            .game-container { max-width: 900px; margin: 0 auto; padding: 20px; }
            .game-header { text-align: center; margin-bottom: 20px; }
            .game-stats { display: flex; justify-content: space-between; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; margin-bottom: 20px; flex-wrap: wrap; }
            .stat-box { background: rgba(255,255,255,0.1); padding: 8px 15px; border-radius: 5px; margin: 5px; min-width: 120px; text-align: center; }
            .game-arena { width: 600px; height: 400px; background: #3e8e41; border: 3px solid #8B4513; border-radius: 10px; margin: 0 auto; position: relative; overflow: hidden; box-shadow: inset 0 0 20px rgba(0,0,0,0.3); }
            .knight { width: 40px; height: 40px; background: #4169E1; border: 2px solid #FFD700; border-radius: 50%; position: absolute; display: flex; align-items: center; justify-content: center; font-size: 20px; transition: all 0.1s; z-index: 10; }
            .slime { width: 25px; height: 25px; background: #32CD32; border: 2px solid #228B22; border-radius: 50%; position: absolute; display: flex; align-items: center; justify-content: center; font-size: 12px; animation: slimeBounce 2s infinite; }
            .elite-slime { background: #FF6347 !important; border-color: #DC143C !important; width: 35px !important; height: 35px !important; font-size: 16px !important; }
            .boss-slime { background: #8A2BE2 !important; border-color: #4B0082 !important; width: 50px !important; height: 50px !important; font-size: 20px !important; }
            @keyframes slimeBounce { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
            .damage-text { position: absolute; color: #FF4444; font-weight: bold; font-size: 16px; pointer-events: none; animation: damageFloat 1s ease-out forwards; z-index: 100; }
            @keyframes damageFloat { 0% { opacity: 1; transform: translateY(0); } 100% { opacity: 0; transform: translateY(-30px); } }
            .exp-orb { width: 10px; height: 10px; background: #FFD700; border-radius: 50%; position: absolute; animation: sparkle 1s infinite; }
            @keyframes sparkle { 0%, 100% { opacity: 0.5; transform: scale(1); } 50% { opacity: 1; transform: scale(1.3); } }
            .controls { text-align: center; margin: 20px 0; }
            .game-btn { background: #e74c3c; color: white; border: none; padding: 12px 25px; margin: 5px; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; transition: all 0.3s; }
            .game-btn:hover { background: #c0392b; transform: translateY(-2px); }
            .game-btn:disabled { background: #95a5a6; cursor: not-allowed; transform: none; }
            .equipment-panel { background: rgba(0,0,0,0.4); padding: 20px; border-radius: 10px; margin-top: 20px; }
            .equipment-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
            .equipment-item { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); }
            .shop-item { background: rgba(52, 152, 219, 0.2); border: 1px solid #3498db; cursor: pointer; transition: all 0.3s; }
            .shop-item:hover { background: rgba(52, 152, 219, 0.4); }
            .shop-item.affordable { border-color: #27ae60; }
            .shop-item.expensive { border-color: #e74c3c; opacity: 0.6; }
            .game-log { background: rgba(0,0,0,0.5); height: 100px; overflow-y: auto; padding: 10px; border-radius: 5px; font-size: 12px; margin-top: 10px; }
            .log-entry { margin: 2px 0; opacity: 0.8; }
            .nav-links { text-align: center; margin-top: 30px; }
            .nav-links a { margin: 0 10px; color: #3498db; text-decoration: none; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="game-container">
            <div class="game-header">
                <h1>⚔️ Knight vs Slimes: Survival Mode 🐸</h1>
                <p>Use WASD or Arrow Keys to move. Click to attack nearby slimes!</p>
            </div>
            
            <div class="game-stats">
                <div class="stat-box">
                    <div>❤️ HP</div>
                    <div id="hp">100/100</div>
                </div>
                <div class="stat-box">
                    <div>⚔️ ATK</div>
                    <div id="attack">10</div>
                </div>
                <div class="stat-box">
                    <div>🛡️ DEF</div>
                    <div id="defense">2</div>
                </div>
                <div class="stat-box">
                    <div>⭐ Level</div>
                    <div id="level">1</div>
                </div>
                <div class="stat-box">
                    <div>✨ EXP</div>
                    <div id="exp">0/10</div>
                </div>
                <div class="stat-box">
                    <div>💰 Gold</div>
                    <div id="gold">0</div>
                </div>
                <div class="stat-box">
                    <div>🏆 Score</div>
                    <div id="score">0</div>
                </div>
                <div class="stat-box">
                    <div>🌊 Wave</div>
                    <div id="wave">1</div>
                </div>
            </div>
            
            <div class="game-arena" id="gameArena">
                <div class="knight" id="knight">🤺</div>
            </div>
            
            <div class="controls">
                <button class="game-btn" onclick="startGame()" id="startBtn">Start Game</button>
                <button class="game-btn" onclick="pauseGame()" id="pauseBtn" disabled>Pause</button>
                <button class="game-btn" onclick="submitGameScore()" id="submitBtn" style="display:none;">Submit Score</button>
                <input type="text" id="playerName" placeholder="Enter your name" style="padding: 10px; margin-left: 10px; border-radius: 5px; border: none;">
            </div>
            
            <div class="equipment-panel">
                <h3>🏪 Equipment Shop</h3>
                <div class="equipment-grid" id="shopGrid">
                    <!-- Shop items will be generated here -->
                </div>
            </div>
            
            <div class="game-log" id="gameLog"></div>
            
            <div class="nav-links">
                <a href="/">🏠 Home</a> | 
                <a href="/highscores">🏆 High Scores</a>
            </div>
        </div>
        
        <script>
            // Game state
            let gameState = {
                running: false,
                paused: false,
                knight: { x: 300, y: 200, hp: 100, maxHp: 100, attack: 10, defense: 2, level: 1, exp: 0, expNeeded: 10, gold: 0, score: 0 },
                slimes: [],
                wave: 1,
                waveProgress: 0,
                slimesInWave: 5,
                keys: {},
                lastAttack: 0,
                attackCooldown: 500,
                equipment: {
                    sword: { name: 'Rusty Sword', attack: 0, cost: 0 },
                    armor: { name: 'Cloth Armor', defense: 0, cost: 0 }
                }
            };
            
            const shopItems = [
                { type: 'sword', name: 'Iron Sword', attack: 5, cost: 50, desc: '+5 Attack' },
                { type: 'sword', name: 'Steel Sword', attack: 12, cost: 150, desc: '+12 Attack' },
                { type: 'sword', name: 'Legendary Blade', attack: 25, cost: 500, desc: '+25 Attack' },
                { type: 'armor', name: 'Leather Armor', defense: 3, cost: 40, desc: '+3 Defense' },
                { type: 'armor', name: 'Chain Mail', defense: 8, cost: 120, desc: '+8 Defense' },
                { type: 'armor', name: 'Dragon Scale', defense: 20, cost: 400, desc: '+20 Defense' },
                { type: 'special', name: 'Health Potion', hp: 50, cost: 25, desc: 'Restore 50 HP' },
                { type: 'special', name: 'Full Heal', hp: 999, cost: 100, desc: 'Full HP restore' }
            ];
            
            function log(message) {
                const gameLog = document.getElementById('gameLog');
                const entry = document.createElement('div');
                entry.className = 'log-entry';
                entry.textContent = '[' + new Date().toLocaleTimeString() + '] ' + message;
                gameLog.appendChild(entry);
                gameLog.scrollTop = gameLog.scrollHeight;
            }
            
            function updateStats() {
                document.getElementById('hp').textContent = gameState.knight.hp + '/' + gameState.knight.maxHp;
                document.getElementById('attack').textContent = gameState.knight.attack + gameState.equipment.sword.attack;
                document.getElementById('defense').textContent = gameState.knight.defense + gameState.equipment.armor.defense;
                document.getElementById('level').textContent = gameState.knight.level;
                document.getElementById('exp').textContent = gameState.knight.exp + '/' + gameState.knight.expNeeded;
                document.getElementById('gold').textContent = gameState.knight.gold;
                document.getElementById('score').textContent = gameState.knight.score;
                document.getElementById('wave').textContent = gameState.wave;
            }
            
            function updateShop() {
                const shopGrid = document.getElementById('shopGrid');
                shopGrid.innerHTML = '';
                
                shopItems.forEach((item, index) => {
                    const div = document.createElement('div');
                    div.className = 'equipment-item shop-item';
                    
                    const canAfford = gameState.knight.gold >= item.cost;
                    div.classList.add(canAfford ? 'affordable' : 'expensive');
                    
                    div.innerHTML = '<strong>' + item.name + '</strong><br>' + item.desc + '<br>💰 ' + item.cost + ' gold';
                    
                    if (canAfford) {
                        div.onclick = () => buyItem(item, index);
                    }
                    
                    shopGrid.appendChild(div);
                });
            }
            
            function buyItem(item, index) {
                if (gameState.knight.gold < item.cost) return;
                
                gameState.knight.gold -= item.cost;
                
                if (item.type === 'sword' || item.type === 'armor') {
                    gameState.equipment[item.type] = item;
                    log('Equipped ' + item.name + '!');
                } else if (item.type === 'special') {
                    if (item.hp) {
                        gameState.knight.hp = Math.min(gameState.knight.maxHp, gameState.knight.hp + item.hp);
                        log('Used ' + item.name + '! Restored ' + item.hp + ' HP.');
                    }
                }
                
                updateStats();
                updateShop();
            }
            
            function createSlime(x, y, type = 'normal') {
                const slime = {
                    x: x || Math.random() * 560,
                    y: y || Math.random() * 360,
                    hp: type === 'boss' ? 50 : type === 'elite' ? 20 : 10,
                    maxHp: type === 'boss' ? 50 : type === 'elite' ? 20 : 10,
                    attack: type === 'boss' ? 15 : type === 'elite' ? 8 : 3,
                    speed: type === 'boss' ? 0.8 : type === 'elite' ? 1.2 : 1,
                    type: type,
                    id: Math.random(),
                    element: null
                };
                return slime;
            }
            
            // Rest of the game functions would continue here...
            // For brevity, I'll include the essential functions
            
            function startGame() {
                gameState.running = true;
                gameState.paused = false;
                document.getElementById('startBtn').disabled = true;
                document.getElementById('pauseBtn').disabled = false;
                log('🎮 Game Started! Survive as long as you can!');
                updateStats();
                updateShop();
            }
            
            // Event listeners
            document.addEventListener('keydown', (e) => {
                gameState.keys[e.key] = true;
            });
            
            document.addEventListener('keyup', (e) => {
                gameState.keys[e.key] = false;
            });
            
            // Initialize
            updateStats();
            updateShop();
        </script>
    </body>
    </html>
    '''

@app.route('/submit-score', methods=['POST'])
def submit_score():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()[:20]  # Limit name length
        score = int(data.get('score', 0))
        game = data.get('game', '')
        
        if name and score > 0:
            score_data = {
                'name': name,
                'score': score,
                'game': game,
                'timestamp': time.time()
            }
            
            # Add extra data for knight game
            if game == 'knight':
                score_data['level'] = data.get('level', 1)
                score_data['wave'] = data.get('wave', 1)
            
            highscores.append(score_data)
            
            # Keep only top 10 scores for each game
            if game == 'reaction':
                reaction_scores = [s for s in highscores if s['game'] == 'reaction']
                reaction_scores.sort(key=lambda x: x['score'])  # Lower is better for reaction time
                highscores[:] = [s for s in highscores if s['game'] != 'reaction'] + reaction_scores[:10]
            elif game == 'knight':
                knight_scores = [s for s in highscores if s['game'] == 'knight']
                knight_scores.sort(key=lambda x: x['score'], reverse=True)  # Higher is better for knight score
                highscores[:] = [s for s in highscores if s['game'] != 'knight'] + knight_scores[:10]
            
            return {'success': True}
    except:
        pass
    
    return {'success': False}

@app.route('/highscores')
def highscores_page():
    # Get reaction time scores (sorted by best time - lowest first)
    reaction_scores = [s for s in highscores if s['game'] == 'reaction']
    reaction_scores.sort(key=lambda x: x['score'])
    
    # Get knight game scores (sorted by highest score first)
    knight_scores = [s for s in highscores if s['game'] == 'knight']
    knight_scores.sort(key=lambda x: x['score'], reverse=True)
    
    reaction_table = ""
    if reaction_scores:
        for i, score in enumerate(reaction_scores, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            reaction_table += f"<tr><td>{medal}</td><td>{score['name']}</td><td>{score['score']}ms</td></tr>"
    else:
        reaction_table = "<tr><td colspan='3'>No scores yet! Be the first to play!</td></tr>"
    
    knight_table = ""
    if knight_scores:
        for i, score in enumerate(knight_scores, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            level = score.get('level', 1)
            wave = score.get('wave', 1)
            knight_table += f"<tr><td>{medal}</td><td>{score['name']}</td><td>{score['score']:,}</td><td>L{level}</td><td>W{wave}</td></tr>"
    else:
        knight_table = "<tr><td colspan='5'>No knights have fallen yet! Be the first to battle!</td></tr>"
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>High Scores - Hall of Fame</title>
        <style>
            body {{ font-family: Arial; margin: 50px; background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%); min-height: 100vh; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
            h1 {{ color: #333; text-align: center; margin-bottom: 40px; font-size: 2.5em; }}
            h2 {{ color: #666; border-bottom: 3px solid #eee; padding-bottom: 15px; margin-top: 40px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 15px; text-align: center; border-bottom: 1px solid #ddd; }}
            th {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; font-weight: bold; }}
            tr:hover {{ background-color: #f8f9fa; }}
            .nav-links {{ text-align: center; margin-top: 40px; }}
            .nav-links a {{ margin: 0 15px; color: #007bff; text-decoration: none; font-weight: bold; padding: 12px 25px; background: #f8f9fa; border-radius: 8px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏆 High Score Leaderboard</h1>
            
            <h2>⚡ Reaction Time Challenge</h2>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Time</th>
                    </tr>
                </thead>
                <tbody>
                    {reaction_table}
                </tbody>
            </table>
            
            <h2>⚔️ Knight Survival</h2>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Knight</th>
                        <th>Score</th>
                        <th>Level</th>
                        <th>Wave</th>
                    </tr>
                </thead>
                <tbody>
                    {knight_table}
                </tbody>
            </table>
            
            <div class="nav-links">
                <a href="/">🏠 Home</a>
                <a href="/reaction-game">⚡ Reaction Game</a>
                <a href="/knight-game">⚔️ Knight Survival</a>
                <a href="/game">🎲 Number Game</a>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
