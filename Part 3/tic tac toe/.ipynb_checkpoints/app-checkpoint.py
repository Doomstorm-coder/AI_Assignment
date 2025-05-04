from flask import Flask, render_template, request, jsonify
from game import TicTacToe

app = Flask(__name__)
game = TicTacToe()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    position = data.get('position')
    
    if game.make_move(position):
        winner, winning_combo = game.check_winner()
        
        if winner:
            update_scores(winner)
            return jsonify({
                'board': game.board,
                'currentPlayer': game.current_player,
                'gameOver': True,
                'winner': winner,
                'winningCombo': winning_combo,
                'scores': game.scores
            })
            
        if game.game_mode == "human_vs_ai":
            ai_position = game.get_best_move()
            game.make_move(ai_position)
            winner, winning_combo = game.check_winner()
            
            if winner:
                update_scores(winner)
                
            return jsonify({
                'board': game.board,
                'currentPlayer': game.current_player,
                'gameOver': winner is not None,
                'winner': winner,
                'winningCombo': winning_combo,
                'scores': game.scores
            })
    
    return jsonify({
        'board': game.board,
        'currentPlayer': game.current_player,
        'gameOver': False,
        'winner': None,
        'scores': game.scores
    })

@app.route('/ai_vs_ai', methods=['POST'])
def ai_vs_ai():
    game.reset_board()
    game.game_mode = "ai_vs_ai"
    
    moves_history = []
    
    while True:
        ai_position = game.get_best_move()
        game.make_move(ai_position)
        moves_history.append({
            'position': ai_position,
            'player': "X" if game.current_player == "O" else "O"
        })
        
        winner, winning_combo = game.check_winner()
        if winner:
            update_scores(winner)
            break
    
    return jsonify({
        'board': game.board,
        'moves': moves_history,
        'gameOver': True,
        'winner': winner,
        'winningCombo': winning_combo,
        'scores': game.scores
    })

@app.route('/set_game_options', methods=['POST'])
def set_game_options():
    data = request.get_json()
    game.game_mode = data.get('gameMode', 'human_vs_ai')
    game.difficulty = data.get('difficulty', 'impossible')
    player_choice = data.get('playerChoice', 'X')
    
    game.reset_board()
    
    if game.game_mode == "human_vs_ai" and player_choice == "O":
        game.current_player = "X"
        ai_position = game.get_best_move()
        game.make_move(ai_position)
    else:
        game.current_player = "X"
    
    return jsonify({
        'board': game.board,
        'currentPlayer': game.current_player,
        'gameOver': False,
        'winner': None,
        'scores': game.scores
    })

@app.route('/reset_game', methods=['POST'])
def reset_game():
    game.reset_board()
    return jsonify({
        'board': game.board,
        'currentPlayer': game.current_player,
        'gameOver': False,
        'winner': None,
        'scores': game.scores
    })

def update_scores(winner):
    if winner == "tie":
        game.scores["tie"] += 1
    else:
        game.scores[winner] += 1

if __name__ == '__main__':
    app.run(debug=True)
