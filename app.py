from flask import Flask, render_template_string, request, session
import random

app = Flask(__name__)app.secret_key = 'your-secret-key-here-change-this'  # Needed for sessions

@app.route('/')
def home():
    return '<h1>Hello, World!</h1><p>My first Python website!</p>'

@app.route('/about')
def about():
    return '<h1>About Me</h1><p>This is my about page!</p>'
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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>My Projects 🚀</h1>
            <p>Here are some things I'm working on:</p>
            <ul>
                <li>Learning Python</li>
                <li>Building websites</li>
                <p><a href="/game" class="button">🎲 Play Game</a></p>
                <li>Getting awesome at coding</li>
            </ul>
            <p><a href="/">← Back Home</a></p>
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
if __name__ == '__main__':
    app.run(debug=True)
