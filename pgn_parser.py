from chess import pgn
import io
from aqt.utils import showInfo

def get_comment(node):
    # Get the first comment if any exist
    if hasattr(node, 'comments') and node.comments:
        return node.comments[0]
    return ''

def get_move_with_number(board, move, node):
    base_san = board.san(move)  # This already includes + and # where appropriate
    turn = board.turn
    fullmove_number = board.fullmove_number
    
    # Create move string (base_san already has + or # if applicable)
    if turn:
        move_str = f"{fullmove_number}.{base_san}"
    else:
        move_str = f"{fullmove_number}...{base_san}"
    
    # Add NAG symbols
    if hasattr(node, 'nags') and node.nags:
        nag_symbols = {
            1: "!",
            2: "?",
            3: "!!",
            4: "??",
            5: "!?",
            6: "?!"
        }
        for nag in node.nags:
            if nag in nag_symbols:
                move_str += nag_symbols[nag]
                break
    
    return move_str

def parse_pgn(pgn_text):
    debug_info = f"Parsing PGN:\n{pgn_text}\n\n"
    try:
        game = pgn.read_game(io.StringIO(pgn_text))
        if game is None:
            raise ValueError("Invalid PGN format")

        # Add game object debugging
        showInfo(f"Game object debug:\nType: {type(game)}\nAttributes: {dir(game)}")

        position_pairs = []
        board = game.board()
        node = game

        debug_info += "Parsing initial position...\n"
        # Handle the initial position
        if node.variations:
            next_node = node.variations[0]
            next_board = board.copy()
            next_board.push(next_node.move)
            
            # Add comment debug for initial position
            initial_comment = get_comment(next_node)
            debug_info += f"Initial position comment debug: {initial_comment}\n"
            
            initial_pair = {
                'current_fen': board.fen(),
                'last_move': None,
                'last_move_uci': None,
                'next_fen': next_board.fen(),
                'next_move': get_move_with_number(board, next_node.move, next_node),
                'next_move_uci': next_node.move.uci(),
                'comment': initial_comment
            }
            position_pairs.append(initial_pair)
            debug_info += f"Initial pair: {initial_pair}\n\n"
        
        debug_info += "Parsing rest of the game...\n"
        # Iterate through the rest of the game
        move_num = 1
        while node.variations:
            current_node = node.variations[0]
            board.push(current_node.move)
            
            if current_node.variations:
                next_node = current_node.variations[0]
                next_board = board.copy()
                next_board.push(next_node.move)
                
                # Add comment debug for each move
                move_comment = get_comment(next_node)
                debug_info += f"Move {move_num} comment debug: {move_comment}\n"
                
                pair = {
                    'current_fen': board.fen(),
                    'last_move': get_move_with_number(node.board(), current_node.move, current_node),
                    'last_move_uci': current_node.move.uci(),
                    'next_fen': next_board.fen(),
                    'next_move': get_move_with_number(board, next_node.move, next_node),
                    'next_move_uci': next_node.move.uci(),
                    'comment': move_comment
                }
                position_pairs.append(pair)
                debug_info += f"Move {move_num}: {pair}\n"
                move_num += 1
            
            node = current_node

        debug_info += f"\nTotal positions parsed: {len(position_pairs)}\n"
        showInfo(debug_info)

        return {
            'header': game.headers,
            'position_pairs': position_pairs,
        }
    except Exception as e:
        error_msg = f"Error parsing PGN: {str(e)}\n\nDebug info:\n{debug_info}"
        showInfo(error_msg)
        raise