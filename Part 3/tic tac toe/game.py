class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        self.difficulty = "impossible"  
        self.game_mode = "human_vs_ai"  
        self.scores = {"X": 0, "O": 0, "tie": 0}
        
    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]
        
    def make_move(self, position):
        if self.board[position] == " ":
            self.board[position] = self.current_player
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False
    
    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]              
        ]
        
        for combo in winning_combinations:
            if self.board[combo[0]] != " " and self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]:
                return self.board[combo[0]], combo
        
        if " " not in self.board:
            return "tie", None
            
        return None, None
    
    def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        result, _ = self.check_winner()
        
        if result == "X":
            return 10 - depth
        elif result == "O":
            return -10 + depth
        elif result == "tie":
            return 0
            
        if self.difficulty != "impossible" and depth == 0:
            import random
            if self.difficulty == "easy" and random.random() < 0.7:
                return random.randint(-5, 5)
            elif self.difficulty == "medium" and random.random() < 0.4:
                return random.randint(-5, 5)
        
        if is_maximizing:
            best_score = float('-inf')
            for move in self.available_moves():
                self.board[move] = "X"
                score = self.minimax(depth + 1, False, alpha, beta)
                self.board[move] = " "
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in self.available_moves():
                self.board[move] = "O"
                score = self.minimax(depth + 1, True, alpha, beta)
                self.board[move] = " "
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
    
    def get_best_move(self):
        best_score = float('-inf') if self.current_player == "X" else float('inf')
        best_move = None
        
        for move in self.available_moves():
            self.board[move] = self.current_player
            if self.current_player == "X":
                score = self.minimax(0, False)
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                score = self.minimax(0, True)
                if score < best_score:
                    best_score = score
                    best_move = move
            self.board[move] = " "
            
        return best_move
    
    def reset_board(self):
        self.board = [" " for _ in range(9)]
