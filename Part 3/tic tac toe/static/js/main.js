document.addEventListener('DOMContentLoaded', function() {
    const cells = document.querySelectorAll('.cell');
    const statusMessage = document.getElementById('status-message');
    const resetButton = document.getElementById('reset-game');
    const applyOptionsButton = document.getElementById('apply-options');
    const aiPlayButton = document.getElementById('ai-play');
    const gameModeSelect = document.getElementById('game-mode');
    const difficultySelect = document.getElementById('difficulty');
    const playerChoiceSelect = document.getElementById('player-choice');
    const scoreX = document.getElementById('score-x');
    const scoreO = document.getElementById('score-o');
    const scoreTie = document.getElementById('score-tie');
    
    let board = Array(9).fill(' ');
    let gameOver = false;
    
    resetGame();
    
    cells.forEach(cell => {
        cell.addEventListener('click', () => {
            const index = cell.dataset.index;
            
            if (!gameOver && board[index] === ' ') {
                makeMove(index);
            }
        });
    });
    
    resetButton.addEventListener('click', () => {
        fetch('/reset_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            updateStatus(data.currentPlayer, data.winner, data.winningCombo);
            gameOver = data.gameOver;
        });
    });
    
    applyOptionsButton.addEventListener('click', () => {
        const gameMode = gameModeSelect.value;
        const difficulty = difficultySelect.value;
        const playerChoice = playerChoiceSelect.value;
        
        fetch('/set_game_options', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                gameMode,
                difficulty,
                playerChoice
            })
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            updateStatus(data.currentPlayer, data.winner, data.winningCombo);
            gameOver = data.gameOver;
            updateScores(data.scores);
        });
    });
    
    aiPlayButton.addEventListener('click', () => {
        fetch('/ai_vs_ai', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            animateAIMoves(data.moves, () => {
                updateBoard(data.board);
                updateStatus(null, data.winner, data.winningCombo);
                gameOver = data.gameOver;
                updateScores(data.scores);
            });
        });
    });
    
    function makeMove(position) {
        fetch('/make_move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                position: parseInt(position)
            })
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            updateStatus(data.currentPlayer, data.winner, data.winningCombo);
            gameOver = data.gameOver;
            updateScores(data.scores);
        });
    }
    
    function updateBoard(newBoard) {
        board = newBoard;
        cells.forEach((cell, index) => {
            cell.className = 'cell';
            if (newBoard[index] === 'X') {
                cell.classList.add('x');
            } else if (newBoard[index] === 'O') {
                cell.classList.add('o');
            }
        });
    }
    
    function updateStatus(currentPlayer, winner, winningCombo) {
        if (winner === 'X') {
            statusMessage.textContent = 'Player X wins!';
            highlightWinningCells(winningCombo);
        } else if (winner === 'O') {
            statusMessage.textContent = 'Player O wins!';
            highlightWinningCells(winningCombo);
        } else if (winner === 'tie') {
            statusMessage.textContent = 'It\'s a tie!';
        } else {
            statusMessage.textContent = `Player ${currentPlayer}'s turn`;
        }
    }
    
    function highlightWinningCells(winningCombo) {
        if (winningCombo) {
            winningCombo.forEach(index => {
                cells[index].classList.add('winning');
            });
        }
    }
    
    function updateScores(scores) {
        scoreX.textContent = scores.X;
        scoreO.textContent = scores.O;
        scoreTie.textContent = scores.tie;
    }
    
    function animateAIMoves(moves, callback) {
        resetGame();
        
        moves.forEach((move, index) => {
            setTimeout(() => {
                const cell = cells[move.position];
                cell.classList.add(move.player.toLowerCase());
                
                if (index === moves.length - 1 && callback) {
                    callback();
                }
            }, index * 500);
        });
    }
    
    function resetGame() {
        fetch('/reset_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data.board);
            updateStatus(data.currentPlayer, null, null);
            gameOver = false;
        });
    }
});
