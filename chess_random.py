import chess
import chess.pgn
import time
import random
import pickle
from collections import Counter

chess.pgn.Game.from_board

def play_random_games(ngames):
    results = Counter()
    move_counts = Counter()
    checkmate_games = []
    for _ in range(ngames):
        board = chess.Board()
        while True:
            if board.is_game_over(): # can pass claim_draw=True which will take 3 fold or 50 move when available
                if board.is_stalemate():
                    results['Stalemate'] += 1
                elif board.is_insufficient_material(): 
                    results['Insufficient material'] += 1
                elif board.is_seventyfive_moves():
                    results['75 move rule'] += 1
                elif board.is_checkmate():
                    checkmate_games.append(chess.pgn.Game().from_board(board))
                    if board.result() == '1-0':
                        results['White checkmate'] += 1
                    else:
                        results['Black checkmate'] += 1
                break
            board.push(random.choice([i for i in board.legal_moves]))
        move_counts[board.fullmove_number] += 1
    return results, move_counts, checkmate_games
    

def main(ngames):
    start_time = time.time()
    results, move_counts, checkmate_games = play_random_games(ngames)

    print(results)

    with open('random_chess_results.pickle', 'wb') as handle:
        pickle.dump(results, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('random_move_counts.pickle', 'wb') as handle:
        pickle.dump(move_counts, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('random_checkmates.txt', 'w') as f:
        for item in checkmate_games:
            f.write("%s\n" % item)
    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main(100000)

# play random moves and count results