import numpy as np

square_state = np.zeros((4, 6, 6))

print(square_state)
print("empty")
states = {}

states[21] = 1
states[14] = 2
states[16] = 1
states[26] = 2
states[16] = 1
states[26] = 2
states[9] = 1
states[20] = 2
states[8] = 1
#states[32] = 2

last_move = 8
current_player = 2

moves, players = np.array(list(zip(*states.items())))
move_curr = moves[players == current_player]
move_oppo = moves[players != current_player]
square_state[0][move_curr // 6, move_curr % 6] = 1.0
square_state[1][move_oppo // 6, move_oppo % 6] = 1.0
square_state[2][last_move // 6, last_move % 6] = 1.0
if len(states)%2 == 0:
    square_state[3][:,:] = 1.0
print(square_state[:,::-1,:])
print("_____________________________")
print(square_state)
