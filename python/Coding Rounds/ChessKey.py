

def get_piece_moves(piece, pos, occupied_positions):
    col, row = ord(pos[0]) - ord('A'), int(pos[1]) - 1
    moves = set()
    
    if piece == 'Q':
        moves.update(get_rook_moves(col, row, occupied_positions))
        moves.update(get_bishop_moves(col, row, occupied_positions))
    elif piece == 'R':
        moves.update(get_rook_moves(col, row, occupied_positions))
    elif piece == 'B':
        moves.update(get_bishop_moves(col, row, occupied_positions))
    
    return moves

def get_rook_moves(col, row, occupied_positions):
    moves = set()
    
    # Horizontal moves - right
    for c in range(col + 1, 8):
        pos = chr(ord('A') + c) + str(row + 1)
        if pos in occupied_positions:
            break
        moves.add(pos)
    
    # Horizontal moves - left
    for c in range(col - 1, -1, -1):
        pos = chr(ord('A') + c) + str(row + 1)
        if pos in occupied_positions:
            break
        moves.add(pos)
    
    # Vertical moves - up
    for r in range(row + 1, 8):
        pos = chr(ord('A') + col) + str(r + 1)
        if pos in occupied_positions:
            break
        moves.add(pos)
    
    # Vertical moves - down
    for r in range(row - 1, -1, -1):
        pos = chr(ord('A') + col) + str(r + 1)
        if pos in occupied_positions:
            break
        moves.add(pos)
    
    return moves

def get_bishop_moves(col, row, occupied_positions):
    moves = set()
    
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    for dc, dr in directions:
        c, r = col + dc, row + dr
        while 0 <= c < 8 and 0 <= r < 8:
            pos = chr(ord('A') + c) + str(r + 1)
            if pos not in occupied_positions:
                moves.add(pos)
                c += dc
                r += dr
            else:
                break
    
    return moves

def solve_chess_positions(initial_positions, depth):
    if depth == 0:
        return 1
    
    pieces = []
    for pos_str in initial_positions:
        piece = pos_str[0]
        position = pos_str[1:]
        pieces.append((piece, position))
    
    # Keep pieces in their original order, don't sort
    initial_state = tuple([pos for _, pos in pieces])
    piece_types = [piece for piece, _ in pieces]
    
    current_states = {initial_state}
    
    for ply in range(depth):
        next_states = set()
        
        for state in current_states:
            for i, (piece_type, current_pos) in enumerate(zip(piece_types, state)):
                occupied = set(state)
                
                valid_moves = get_piece_moves(piece_type, current_pos, occupied)
                
                for new_pos in valid_moves:
                    new_state = list(state)
                    new_state[i] = new_pos
                    next_states.add(tuple(new_state))
        
        current_states = next_states
    
    return len(current_states)

initial_positions = input().strip().split()
depth = int(input().strip())

result = solve_chess_positions(initial_positions, depth)
print(result)
