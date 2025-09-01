from flask import Flask, render_template_string, request, session
import random
import time
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this'  # Needed for sessions

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
        <h1>BAHAH HEJHEJ</h1>
        <p>detta var ju lätt som en plätt</p>
        <p><a href="/about" class="button">About Me</a></p>
        <p><a href="/projects" class="button">My Projects</a></p>
        <p><a href="/game" class="button">🎲 Number Game</a></p>
        <p><a href="/reaction-game" class="button">⚡ Reaction Game</a></p>
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

@app.route('/submit-score', methods=['POST'])
def submit_score():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()[:20]  # Limit name length
        score = int(data.get('score', 0))
        game = data.get('game', '')
        
        if name and score > 0:
            highscores.append({
                'name': name,
                'score': score,
                'game': game,
                'timestamp': time.time()
            })
            
            # Keep only top 10 scores for each game
            reaction_scores = [s for s in highscores if s['game'] == 'reaction']
            reaction_scores.sort(key=lambda x: x['score'])  # Lower is better for reaction time
            highscores[:] = [s for s in highscores if s['game'] != 'reaction'] + reaction_scores[:10]
            
            return {'success': True}
    except:
        pass
    
    return {'success': False}

@app.route('/highscores')
def highscores_page():
    # Get reaction time scores (sorted by best time - lowest first)
    reaction_scores = [s for s in highscores if s['game'] == 'reaction']
    reaction_scores.sort(key=lambda x: x['score'])
    
    reaction_table = ""
    if reaction_scores:
        for i, score in enumerate(reaction_scores, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            reaction_table += f"<tr><td>{medal}</td><td>{score['name']}</td><td>{score['score']}ms</td></tr>"
    else:
        reaction_table = "<tr><td colspan='3'>No scores yet! Be the first to play!</td></tr>"
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>High Scores</title>
        <style>
            body {{ font-family: Arial; margin: 50px; background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%); min-height: 100vh; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
            h1 {{ color: #333; text-align: center; margin-bottom: 40px; }}
            h2 {{ color: #666; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f8f9fa; font-weight: bold; color: #333; }}
            tr:hover {{ background-color: #f5f5f5; }}
            .medal {{ font-size: 24px; }}
            .nav-links {{ text-align: center; margin-top: 40px; }}
            .nav-links a {{ margin: 0 15px; color: #007bff; text-decoration: none; font-weight: bold; padding: 10px 20px; background: #f8f9fa; border-radius: 5px; }}
            .nav-links a:hover {{ background: #e9ecef; text-decoration: none; }}
            .no-scores {{ text-align: center; color: #666; font-style: italic; }}
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
            
            <div class="nav-links">
                <a href="/">🏠 Home</a>
                <a href="/reaction-game">⚡ Play Reaction Game</a>
                <a href="/game">🎲 Number Game</a>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
