from flask import Flask, render_template_string, request, session
import random
import time
import json
import os

app = Flask(__name__)
app.secret_key = 'MyKnightGame2024-SuperSecret-Key!'

# In-memory highscore storage
highscores = []

# HTML template for home page
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Knight Survival Game</title>
    <style>
        body { font-family: Arial; margin: 50px; background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); color: white; }
        .container { max-width: 600px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 40px; border-radius: 15px; box-shadow: 0 15px 35px rgba(0,0,0,0.3); text-align: center; }
        h1 { color: #ecf0f1; font-size: 2.5em; margin-bottom: 20px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); }
        p { font-size: 1.2em; margin-bottom: 30px; }
        .button { background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; margin: 10px; display: inline-block; font-weight: bold; transition: all 0.3s; }
        .button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(231,76,60,0.4); }
        .features { text-align: left; margin: 30px 0; background: rgba(0,0,0,0.3); padding: 20px; border-radius: 10px; }
        .features h3 { color: #f39c12; margin-bottom: 15px; }
        .features ul { list-style: none; padding: 0; }
        .features li { margin: 8px 0; padding-left: 20px; position: relative; }
        .features li:before { content: "⚔️"; position: absolute; left: 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>⚔️ Knight Survival</h1>
        <p>Test your skills in the ultimate medieval survival challenge!</p>
        
        <div class="features">
            <h3>🎮 Game Features:</h3>
            <ul>
                <li>Keyboard sword combat with SPACE key</li>
                <li>Tactical cooldown system</li>
                <li>Animated sword attacks</li>
                <li>RPG progression system</li>
                <li>Equipment shop with upgrades</li>
                <li>Endless wave survival</li>
                <li>Boss battles</li>
            </ul>
        </div>
        
        <p><a href="/knight-game" class="button">⚔️ Start Battle</a></p>
        <p><a href="/highscores" class="button">🏆 Hall of Fame</a></p>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route('/knight-game')
def knight_game():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Knight vs Slimes - Survival Mode</title>
        <style>
            body { font-family: 'Courier New', monospace; margin: 0; background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); color: white; overflow-x: hidden; user-select: none; }
            .game-container { max-width: 1000px; margin: 0 auto; padding: 20px; }
            .game-header { text-align: center; margin-bottom: 20px; }
            .game-stats { display: flex; justify-content: space-between; background: rgba(0,0,0,0.4); padding: 15px; border-radius: 10px; margin-bottom: 20px; flex-wrap: wrap; }
            .stat-box { background: rgba(255,255,255,0.1); padding: 8px 15px; border-radius: 5px; margin: 5px; min-width: 120px; text-align: center; border: 1px solid rgba(255,255,255,0.2); }
            .game-arena { width: 700px; height: 500px; background: #3e8e41; border: 3px solid #8B4513; border-radius: 10px; margin: 0 auto; position: relative; overflow: hidden; box-shadow: inset 0 0 30px rgba(0,0,0,0.4); }
            
            /* Knight styling with sword */
            .knight { width: 50px; height: 50px; position: absolute; display: flex; align-items: center; justify-content: center; font-size: 24px; transition: all 0.1s; z-index: 20; }
            .knight-body { width: 40px; height: 40px; background: #4169E1; border: 2px solid #FFD700; border-radius: 50%; display: flex; align-items: center; justify-content: center; transition: all 0.2s; }
            .knight.attacking .knight-body { transform: scale(1.2); background: #1E90FF; }
            
            /* Sword styling */
            .sword { position: absolute; width: 60px; height: 8px; background: linear-gradient(90deg, #C0C0C0 0%, #FFFFFF 50%, #C0C0C0 100%); border: 1px solid #A0A0A0; border-radius: 4px; transform-origin: 10px center; transition: all 0.2s; opacity: 0; z-index: 15; }
            .sword::before { content: ''; position: absolute; left: -8px; top: -4px; width: 16px; height: 16px; background: #8B4513; border-radius: 2px; }
            .knight.attacking .sword { opacity: 1; }
            .knight.attack-right .sword { transform: rotate(0deg) translateX(25px); }
            .knight.attack-left .sword { transform: rotate(180deg) translateX(25px); }
            .knight.attack-up .sword { transform: rotate(-90deg) translateX(25px); }
            .knight.attack-down .sword { transform: rotate(90deg) translateX(25px); }
            
            /* Attack cooldown indicator */
            .cooldown-bar { position: absolute; bottom: -8px; left: 50%; transform: translateX(-50%); width: 50px; height: 4px; background: rgba(0,0,0,0.3); border-radius: 2px; }
            .cooldown-fill { height: 100%; background: linear-gradient(90deg, #e74c3c, #f39c12); border-radius: 2px; transition: width 0.1s linear; }
            
            .slime { width: 30px; height: 30px; background: #32CD32; border: 2px solid #228B22; border-radius: 50%; position: absolute; display: flex; align-items: center; justify-content: center; font-size: 14px; animation: slimeBounce 2s infinite; transition: all 0.2s; }
            .elite-slime { background: #FF6347 !important; border-color: #DC143C !important; width: 40px !important; height: 40px !important; font-size: 18px !important; }
            .boss-slime { background: #8A2BE2 !important; border-color: #4B0082 !important; width: 60px !important; height: 60px !important; font-size: 24px !important; }
            
            @keyframes slimeBounce { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.1); } }
            @keyframes slimeHit { 0% { transform: scale(1); } 50% { transform: scale(0.8); background-color: #FF4444; } 100% { transform: scale(1); } }
            .slime.hit { animation: slimeHit 0.3s ease; }
            
            .damage-text { position: absolute; color: #FF4444; font-weight: bold; font-size: 18px; pointer-events: none; animation: damageFloat 1.2s ease-out forwards; z-index: 100; text-shadow: 1px 1px 2px rgba(0,0,0,0.7); }
            @keyframes damageFloat { 0% { opacity: 1; transform: translateY(0) scale(0.8); } 20% { transform: translateY(-10px) scale(1.2); } 100% { opacity: 0; transform: translateY(-40px) scale(0.6); } }
            
            .exp-orb { width: 12px; height: 12px; background: radial-gradient(circle, #FFD700, #FFA500); border: 1px solid #FF8C00; border-radius: 50%; position: absolute; animation: sparkle 1.5s infinite; box-shadow: 0 0 10px #FFD700; }
            @keyframes sparkle { 0%, 100% { opacity: 0.6; transform: scale(1); } 50% { opacity: 1; transform: scale(1.4); } }
            
            .controls { text-align: center; margin: 20px 0; }
            .game-btn { background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; border: none; padding: 12px 25px; margin: 5px; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; transition: all 0.3s; }
            .game-btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(231,76,60,0.4); }
            .game-btn:disabled { background: #95a5a6; cursor: not-allowed; transform: none; box-shadow: none; }
            
            .equipment-panel { background: rgba(0,0,0,0.5); padding: 20px; border-radius: 10px; margin-top: 20px; }
            .equipment-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 15px; }
            .equipment-item { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3s; }
            .shop-item { background: rgba(52, 152, 219, 0.2); border: 1px solid #3498db; cursor: pointer; }
            .shop-item:hover { background: rgba(52, 152, 219, 0.4); transform: translateY(-2px); }
            .shop-item.affordable { border-color: #27ae60; box-shadow: 0 0 10px rgba(39,174,96,0.3); }
            .shop-item.expensive { border-color: #e74c3c; opacity: 0.6; }
            
            .game-log { background: rgba(0,0,0,0.6); height: 120px; overflow-y: auto; padding: 15px; border-radius: 8px; font-size: 13px; margin-top: 15px; border: 1px solid rgba(255,255,255,0.1); }
            .log-entry { margin: 3px 0; opacity: 0.9; line-height: 1.4; }
            .log-entry.important { color: #f39c12; font-weight: bold; }
            
            .controls-info { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center; }
            .key { background: #34495e; color: white; padding: 3px 8px; border-radius: 4px; font-weight: bold; margin: 0 2px; border: 1px solid #2c3e50; }
            
            .nav-links { text-align: center; margin-top: 30px; }
            .nav-links a { margin: 0 15px; color: #3498db; text-decoration: none; font-weight: bold; padding: 8px 15px; border-radius: 5px; transition: all 0.3s; }
            .nav-links a:hover { background: rgba(52,152,219,0.2); }
        </style>
    </head>
    <body>
        <div class="game-container">
            <div class="game-header">
                <h1>⚔️ Knight vs Slimes: Survival Mode 🐸</h1>
            </div>
            
            <div class="controls-info">
                <p><strong>🎮 Controls:</strong> Move with <span class="key">WASD</span> or Arrow Keys | Attack with <span class="key">SPACE</span></p>
                <p><em>Watch your attack cooldown! Time your strikes wisely!</em></p>
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
                <div class="knight" id="knight">
                    <div class="knight-body">🤺</div>
                    <div class="sword"></div>
                    <div class="cooldown-bar">
                        <div class="cooldown-fill" id="cooldownFill"></div>
                    </div>
                </div>
            </div>
            
            <div class="controls">
                <button class="game-btn" onclick="startGame()" id="startBtn">Start Battle</button>
                <button class="game-btn" onclick="pauseGame()" id="pauseBtn" disabled>Pause</button>
                <button class="game-btn" onclick="submitGameScore()" id="submitBtn" style="display:none;">Submit Score</button>
                <input type="text" id="playerName" placeholder="Enter your name for leaderboard" style="padding: 10px; margin-left: 10px; border-radius: 5px; border: none; width: 200px;">
            </div>
            
            <div class="equipment-panel">
                <h3>🏪 Equipment Shop & Upgrades</h3>
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
                knight: { 
                    x: 350, y: 250, 
                    hp: 100, maxHp: 100, 
                    attack: 10, defense: 2, 
                    level: 1, exp: 0, expNeeded: 10, 
                    gold: 0, score: 0,
                    lastDirection: 'right'
                },
                slimes: [],
                wave: 1,
                keys: {},
                lastAttack: 0,
                attackCooldown: 800, // 800ms cooldown
                attacking: false,
                equipment: {
                    sword: { name: 'Rusty Sword', attack: 0, cost: 0 },
                    armor: { name: 'Cloth Armor', defense: 0, cost: 0 }
                }
            };
            
            const shopItems = [
                { type: 'sword', name: 'Iron Sword', attack: 8, cost: 50, desc: '+8 Attack' },
                { type: 'sword', name: 'Steel Sword', attack: 18, cost: 180, desc: '+18 Attack' },
                { type: 'sword', name: 'Legendary Blade', attack: 35, cost: 600, desc: '+35 Attack' },
                { type: 'armor', name: 'Leather Armor', defense: 5, cost: 60, desc: '+5 Defense' },
                { type: 'armor', name: 'Chain Mail', defense: 12, cost: 160, desc: '+12 Defense' },
                { type: 'armor', name: 'Dragon Scale Armor', defense: 25, cost: 500, desc: '+25 Defense' },
                { type: 'special', name: 'Health Potion', hp: 50, cost: 30, desc: 'Restore 50 HP' },
                { type: 'special', name: 'Greater Heal', hp: 9999, cost: 120, desc: 'Full HP restore' }
            ];
            
            function log(message, important = false) {
                const gameLog = document.getElementById('gameLog');
                const entry = document.createElement('div');
                entry.className = 'log-entry' + (important ? ' important' : '');
                entry.textContent = '[' + new Date().toLocaleTimeString() + '] ' + message;
                gameLog.appendChild(entry);
                gameLog.scrollTop = gameLog.scrollHeight;
                
                // Keep log from getting too long
                if (gameLog.children.length > 50) {
                    gameLog.removeChild(gameLog.firstChild);
                }
            }
            
            function updateStats() {
                document.getElementById('hp').textContent = gameState.knight.hp + '/' + gameState.knight.maxHp;
                document.getElementById('attack').textContent = gameState.knight.attack + gameState.equipment.sword.attack;
                document.getElementById('defense').textContent = gameState.knight.defense + gameState.equipment.armor.defense;
                document.getElementById('level').textContent = gameState.knight.level;
                document.getElementById('exp').textContent = gameState.knight.exp + '/' + gameState.knight.expNeeded;
                document.getElementById('gold').textContent = gameState.knight.gold;
                document.getElementById('score').textContent = gameState.knight.score.toLocaleString();
                document.getElementById('wave').textContent = gameState.wave;
                
                // Update HP bar color based on health percentage
                const hpPercent = gameState.knight.hp / gameState.knight.maxHp;
                const hpElement = document.getElementById('hp').parentElement;
                if (hpPercent < 0.3) {
                    hpElement.style.background = 'rgba(231,76,60,0.3)';
                } else if (hpPercent < 0.6) {
                    hpElement.style.background = 'rgba(241,196,15,0.3)';
                } else {
                    hpElement.style.background = 'rgba(255,255,255,0.1)';
                }
            }
            
            function updateCooldown() {
                const now = Date.now();
                const timeSinceAttack = now - gameState.lastAttack;
                const cooldownProgress = Math.min(timeSinceAttack / gameState.attackCooldown, 1);
                
                const cooldownFill = document.getElementById('cooldownFill');
                cooldownFill.style.width = (cooldownProgress * 100) + '%';
                
                if (cooldownProgress < 1) {
                    cooldownFill.style.background = 'linear-gradient(90deg, #e74c3c, #c0392b)';
                } else {
                    cooldownFill.style.background = 'linear-gradient(90deg, #27ae60, #2ecc71)';
                }
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
                        div.onclick = () => buyItem(item);
                    }
                    
                    shopGrid.appendChild(div);
                });
                
                // Show current equipment
                const currentDiv = document.createElement('div');
                currentDiv.className = 'equipment-item';
                currentDiv.style.background = 'rgba(39,174,96,0.2)';
                currentDiv.innerHTML = '<strong>Current Equipment:</strong><br>⚔️ ' + gameState.equipment.sword.name + '<br>🛡️ ' + gameState.equipment.armor.name;
                shopGrid.appendChild(currentDiv);
            }
            
            function buyItem(item) {
                if (gameState.knight.gold < item.cost) return;
                
                gameState.knight.gold -= item.cost;
                
                if (item.type === 'sword' || item.type === 'armor') {
                    gameState.equipment[item.type] = item;
                    log('Equipped ' + item.name + '! Stats increased!', true);
                } else if (item.type === 'special') {
                    if (item.hp) {
                        const healAmount = Math.min(item.hp, gameState.knight.maxHp - gameState.knight.hp);
                        gameState.knight.hp = Math.min(gameState.knight.maxHp, gameState.knight.hp + item.hp);
                        log('Used ' + item.name + '! Restored ' + healAmount + ' HP.', true);
                        showDamageText(gameState.knight.x + 350, gameState.knight.y + 250, '+' + healAmount, '#27ae60');
                    }
                }
                
                updateStats();
                updateShop();
            }
            
            function createSlime(x, y, type = 'normal') {
                const slime = {
                    x: x !== undefined ? x : Math.random() * 650,
                    y: y !== undefined ? y : Math.random() * 450,
                    hp: type === 'boss' ? 80 : type === 'elite' ? 25 : 12,
                    maxHp: type === 'boss' ? 80 : type === 'elite' ? 25 : 12,
                    attack: type === 'boss' ? 18 : type === 'elite' ? 10 : 4,
                    speed: type === 'boss' ? 1.0 : type === 'elite' ? 1.4 : 1.1,
                    type: type,
                    id: Math.random(),
                    element: null,
                    lastAttack: 0
                };
                return slime;
            }
            
            function spawnSlime(slime) {
                const arena = document.getElementById('gameArena');
                const slimeEl = document.createElement('div');
                slimeEl.className = 'slime ' + slime.type + '-slime';
                slimeEl.id = 'slime-' + slime.id;
                slimeEl.textContent = slime.type === 'boss' ? '👑' : slime.type === 'elite' ? '💀' : '🟢';
                slimeEl.style.left = slime.x + 'px';
                slimeEl.style.top = slime.y + 'px';
                arena.appendChild(slimeEl);
                slime.element = slimeEl;
                gameState.slimes.push(slime);
            }
            
            function startWave() {
                log('🌊 Wave ' + gameState.wave + ' begins! Prepare for battle!', true);
                
                const baseSlimes = Math.min(4 + Math.floor(gameState.wave * 1.2), 15);
                const eliteSlimes = Math.floor(gameState.wave / 3);
                const bossSlimes = Math.floor(gameState.wave / 8);
                
                // Spawn slimes from edges with staggered timing
                for (let i = 0; i < baseSlimes; i++) {
                    setTimeout(() => {
                        const edge = Math.floor(Math.random() * 4);
                        let x, y;
                        switch(edge) {
                            case 0: x = -20; y = Math.random() * 450; break;
                            case 1: x = 720; y = Math.random() * 450; break;
                            case 2: x = Math.random() * 700; y = -20; break;
                            case 3: x = Math.random() * 700; y = 520; break;
                        }
                        spawnSlime(createSlime(x, y, 'normal'));
                    }, i * 800);
                }
                
                // Spawn elite slimes
                for (let i = 0; i < eliteSlimes; i++) {
                    setTimeout(() => {
                        spawnSlime(createSlime(Math.random() * 650, Math.random() * 450, 'elite'));
                        log('💀 Elite Slime has appeared!', true);
                    }, (baseSlimes + i) * 1200);
                }
                
                // Spawn boss slimes
                for (let i = 0; i < bossSlimes; i++) {
                    setTimeout(() => {
                        spawnSlime(createSlime(350, 250, 'boss'));
                        log('👑 BOSS SLIME EMERGES! DANGER!', true);
                    }, (baseSlimes + eliteSlimes + i) * 2000);
                }
            }
            
            function moveSlimes() {
                gameState.slimes.forEach((slime, index) => {
                    if (!slime.element) return;
                    
                    // Move towards knight
                    const dx = gameState.knight.x - slime.x;
                    const dy = gameState.knight.y - slime.y;
                    const distance = Math.sqrt(dx*dx + dy*dy);
                    
                    if (distance > 8) {
                        slime.x += (dx/distance) * slime.speed;
                        slime.y += (dy/distance) * slime.speed;
                        
                        // Keep slimes in bounds
                        slime.x = Math.max(-10, Math.min(710, slime.x));
                        slime.y = Math.max(-10, Math.min(510, slime.y));
                        
                        slime.element.style.left = slime.x + 'px';
                        slime.element.style.top = slime.y + 'px';
                        
                        // Attack knight if close enough and cooldown is ready
                        const now = Date.now();
                        if (distance < 50 && now - slime.lastAttack > 1500) {
                            attackKnight(slime);
                            slime.lastAttack = now;
                        }
                    }
                });
            }
            
            function attackKnight(slime) {
                const totalDefense = gameState.knight.defense + gameState.equipment.armor.defense;
                const damage = Math.max(1, slime.attack - totalDefense + Math.floor(Math.random() * 3));
                gameState.knight.hp -= damage;
                
                showDamageText(gameState.knight.x + 350, gameState.knight.y + 250, '-' + damage, '#e74c3c');
                log(slime.type.charAt(0).toUpperCase() + slime.type.slice(1) + ' slime attacks for ' + damage + ' damage!');
                
                // Screen shake effect
                const arena = document.getElementById('gameArena');
                arena.style.transform = 'translateX(' + (Math.random() * 6 - 3) + 'px)';
                setTimeout(() => { arena.style.transform = 'translateX(0)'; }, 100);
                
                if (gameState.knight.hp <= 0) {
                    gameState.knight.hp = 0;
                    gameOver();
                }
                
                updateStats();
            }
            
            function performAttack() {
                const now = Date.now();
                if (now - gameState.lastAttack < gameState.attackCooldown || gameState.attacking) return;
                
                gameState.lastAttack = now;
                gameState.attacking = true;
                
                const knight = document.getElementById('knight');
                const attackRange = 80;
                const totalAttack = gameState.knight.attack + gameState.equipment.sword.attack;
                
                // Determine attack direction based on last movement or random
                const directions = ['right', 'left', 'up', 'down'];
                const attackDirection = gameState.knight.lastDirection || 'right';
                
                // Add attack animation
                knight.classList.add('attacking', 'attack-' + attackDirection);
                
                let hitCount = 0;
                gameState.slimes.forEach((slime, index) => {
                    const dx = gameState.knight.x - slime.x;
                    const dy
