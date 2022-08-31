import tty, sys, termios, time, select
from random import randrange
from itertools import product

letter_to_change_vector = {'a':(-1,0),'d':(1,0),'s':(0,1),'w':(0,-1)}

# game settings
board_width = 16
board_length = 16
snake_len = 3

# starting settings
full_snake_pos = [(5,5)]
free_positions = set([ele for ele in product(range(1,board_width), range(1,board_length))])
snake_head = [5,5]
direction = (1,0)
food = (randrange(1,board_width-1), randrange(1,board_length-1))


def read_input(cur_direction, seconds=.2):
    filedescriptors = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    
    st = time.time()
    input, _, __ = select.select( [sys.stdin], [], [], seconds)
    if input:
        input = sys.stdin.read(1)[0]
        if input in letter_to_change_vector:
            direction = letter_to_change_vector[input]
            
            elapsed_time = time.time() - st
            time.sleep(abs(seconds-(elapsed_time))) # keep movement of snake constant
            
            if cur_direction != (direction[0] * -1, direction[1] * -1): # can't double back
                return direction
                
                
def update_position(direction, positions, head, snake_len):
    head = [sum(z) for z in zip(head,direction)]
        
    if head[0] == 0 or head[0] >= board_width or head[1] == 0 or head[1] >= board_length:
        print("Out of Bounds!")
        exit(0)
        
    positions.append((head[0],head[1]))
    
    if (head[0],head[1]) not in free_positions:
        print("OUROBOROS") # game over
        exit()
        
    free_positions.remove((head[0],head[1]))
    
    if len(positions) > snake_len:
        free_positions.add(positions[0])
        positions = positions[1:]
    
    return (head, positions)
    

# could change to dictionary from (i,j) entry to correct emoji instead of maintaining lists
def print_board(full_snake_pos, food):
    for i in range(10):
        print()
    print("----------SNAKE----------")
    print()
    for i in range(board_width + 1):
        for j in range(board_length + 1):
            if (j,i) in full_snake_pos:
                print('🐍', end='')
                continue
            if (j,i) == food:
                print('🐥', end='')
                continue
            if i == board_width or i == 0 or j == board_length or j == 0:
                if i % 2 == 0 and j % 2 == 0:
                    print('🔥' ,end='')
                else:
                    print('👹',end='')
            else:
                print('  ', end='')
        print()
        
while True:
    print_board(full_snake_pos, food)
    direction = read_input(direction) or direction
    snake_head, full_snake_pos = update_position(direction, full_snake_pos, snake_head, snake_len)
    if tuple(snake_head) == food:
        snake_len += 1
        food = free_positions.pop()
        free_positions.add(food) # don't die if you hit the food 
        
# make a dictionary from pixels to whether they're free or not for checking if you ate yourself
# then have the inverse of that. Dictionary from free/not free to list of all the free/not free
# cells, so you can randomly choose from the list. O(2n) memory but only
# O(n) time.    