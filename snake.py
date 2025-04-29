import tty, sys, time, select
from random import randrange
from itertools import product

letter_to_change_vector = {'a':(-1,0),'d':(1,0),'s':(0,1),'w':(0,-1)}

# game settings
board_width = 16
board_length = 16
snake_len = 3

motif_selector = randrange(0,10)
avatar = '🐍' if motif_selector > 1 else '👱🏻‍♀️'
food_emoji_list = ['🐥','🐣','🪺','🍄','🐁','🐭','🐀','🐸','🦎'] if motif_selector > 1 else ['🍦', '💯', '💞', '💆🏻‍♀️','🥥','💄','👗','💅🏼','💋','👸🏼'] 
food_emoji = food_emoji_list[randrange(0,len(food_emoji_list))]
wall_emoji_1 = '🔥' if motif_selector > 1 else '🌸'
wall_emoji_2 = '👹' if motif_selector > 1 else '🎀'

# starting settings
full_snake_pos = [(5,5)]
free_positions = set([ele for ele in product(range(1,board_width), range(1,board_length))])
snake_head = [5,5]
direction = (1,0)
food_position = (randrange(1,board_width-1), randrange(1,board_length-1))


def read_input(cur_direction, seconds=.2):
    tty.setcbreak(sys.stdin)
    
    st = time.time()
    user_input, _, __ = select.select( [sys.stdin], [], [], seconds)

    if user_input:
        user_input = sys.stdin.read(1)[0]
        if user_input in letter_to_change_vector:
            direction = letter_to_change_vector[user_input]
            
            elapsed_time = time.time() - st
            time.sleep(abs(seconds-(elapsed_time))) # keep movement of snake constant
            
            if cur_direction != (direction[0] * -1, direction[1] * -1): # can't double back
                return direction
                
                
def update_position(direction, positions, head, snake_len):
    head = [sum(z) for z in zip(head,direction)]
        
    if head[0] == 0 or head[0] >= board_width or head[1] == 0 or head[1] >= board_length:
        print("Out of Bounds!")
        check_high_score(snake_len)
        exit(0)
        
    positions.append((head[0],head[1]))
    
    if (head[0],head[1]) not in free_positions:
        print("OUROBOROS") # game over
        check_high_score(snake_len)
        exit(0)
        
    free_positions.remove((head[0],head[1]))
    
    if len(positions) > snake_len:
        free_positions.add(positions[0])
        positions = positions[1:]
    
    return (head, positions)
    

# could change to dictionary from (i,j) entry to correct emoji instead of maintaining lists
def print_board(full_snake_pos, food_position):
    for i in range(10):
        print()
    with open ("aux/title_card.txt", 'r') as title_card:
        content = title_card.read()
        print(content)
        print()
        print()
        for i in range(board_width + 1):
            for j in range(board_length + 1):
                if (j,i) in full_snake_pos:
                    print(avatar, end='')
                    continue
                if (j,i) == food_position:
                    print(food_emoji, end='')
                    continue
                if i == board_width or i == 0 or j == board_length or j == 0:
                    if i % 2 == 0 and j % 2 == 0:
                        print(wall_emoji_1, end='')
                    else:
                        print(wall_emoji_2, end='')
                else:
                    print('  ', end='')
            print()
        
def check_high_score(snake_len):
     snake_len = snake_len - 1
     with open ("aux/high_scores.txt", 'r+') as high_scores_file:
        high_score = int(high_scores_file.read())
        new_high_score = snake_len > high_score
        copulative_verb = "was" if new_high_score else "is"
        print(f"You scored {snake_len}. The high score {copulative_verb} {high_score}.") 
        if snake_len > high_score: 
            print("Congratulations! You have a new high score!")    
            # high_score_animation()
            high_scores_file.seek(0)
            high_scores_file.write(str(snake_len))
            high_scores_file.truncate()
            exit()
        else:
            special_insult = ", LOSER" if randrange(0,100) == 42 else ""
            print(f"You were {high_score - snake_len} away from the high score. Try again{special_insult}.")

        
while True:
    print_board(full_snake_pos, food_position)
    direction = read_input(direction) or direction
    snake_head, full_snake_pos = update_position(direction, full_snake_pos, snake_head, snake_len)
    if tuple(snake_head) == food_position:
        snake_len += 1
        food_position = free_positions.pop()
        free_positions.add(food_position) # don't die if you hit the food
        food_emoji = food_emoji_list[randrange(0,len(food_emoji_list))]
        
# make a dictionary from pixels to whether they're free or not for checking if you ate yourself
# then have the inverse of that. Dictionary from free/not free to list of all the free/not free
# cells, so you can randomly choose from the list. O(2n) memory but only
# O(n) time.    