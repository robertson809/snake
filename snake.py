import tty, sys, time, select
from random import randrange
from itertools import product
from flask import Flask, request

letter_to_change_vector = {'a':(-1,0),'d':(1,0),'s':(0,1),'w':(0,-1)}
app = Flask(__name__)

class game:
    board_width = 16
    board_length = 16
    snake_len = 3
    motif_selector = randrange(2)
    cutoff = 0
    
    avatar_counter = 0
    barbie_avatars = ['👩🏼‍⚕️','👱🏻‍♀️','👩🏼‍🎓','👩🏼‍🏫','👩🏼‍🍳','👩🏻‍🔬','👩🏻‍✈️','👮🏼‍♀️']
    food_emoji_list = ['🐥','🐣','🪺','🍄','🐁','🐭','🐀','🐸','🦎'] if motif_selector > cutoff else ['🍦', '💯', '💞', '💆🏻‍♀️','🥥','💄','👗','💅🏼','💋','👸🏼'] 
    food_emoji = food_emoji_list[randrange(0,len(food_emoji_list))]
    wall_emoji_1 = '🔥' if motif_selector > cutoff else '🌸'
    wall_emoji_2 = '👹' if motif_selector > cutoff else '🎀'
    title_card_file_name = 'snake_title_card.txt' if motif_selector > cutoff else 'barbie_title_card.txt'
    title_card_content = ''
    with open (f"aux/{title_card_file_name}", 'r') as title_card:
        title_card_content = title_card.read()
    seconds_to_move = 0.2
    pause_enabled = True
    high_score_enabled = True
    toggle = 0

    print(title_card_content)
    print("\n"*5)
    dev_mode = True if input("Welcome to the game! Press enter to start") == "robertson809" else False

    if dev_mode:
        print("\n"*3)
        print("Welcome Sir...It's so nice to see you")
        high_score_enabled = False
        print("\n"*3)
        board_length = int(input("Choose the length (enter a number)"))
        print("")
        board_width = int(input("Choose the length (enter a number)"))
        print("")
        if input("Enable pausing? (y/n)") == 'y': pause_enabled = True
        print("")
        seconds_to_move = float(input("Select Speed (default 0.2s per movement):"))
        print("")
        snake_len = int(input("Select starting length"))
    
    current_snake_emojis = ['🐍'] * snake_len if motif_selector > cutoff else barbie_avatars[:snake_len]
    full_avatar_list = ['🐍'] if motif_selector > cutoff else barbie_avatars
    next_avatar_position = snake_len % len(full_avatar_list)

    full_snake_pos = [(5,5)]
    free_positions = set([ele for ele in product(range(1,board_width), range(1,board_length))])
    snake_head = [5,5]

    direction = (1,0)
    food_position = (randrange(1,board_width-1), randrange(1,board_length-1))


    def read_input(self, cur_direction, seconds=.2):
        tty.setcbreak(sys.stdin)
        st = time.time()
        user_input, _, __ = select.select( [sys.stdin], [], [], seconds)
        
        if user_input:
            user_input = sys.stdin.read(1)[0]
            if user_input == 'p' and self.pause_enabled:
                unpause_character = '_'
                while unpause_character != 'p':
                    unpause_character = sys.stdin.read(1)[0]
                    return self.read_input(cur_direction)
            if user_input in letter_to_change_vector:
                direction = letter_to_change_vector[user_input]
                
                elapsed_time = time.time() - st
                time.sleep(abs(seconds-(elapsed_time))) # keep movement of snake constant
                
                if cur_direction != (direction[0] * -1, direction[1] * -1): # can't double back
                    return direction
                    
                    
    def update_position(self, direction, snake_occupied_positions, potential_new_head, snake_len):
        potential_new_head = [sum(z) for z in zip(potential_new_head,direction)] # clever, perhaps too clever, way to see where we're going next
            
        if potential_new_head[0] == 0 or potential_new_head[0] >= self.board_width or potential_new_head[1] == 0 or potential_new_head[1] >= self.board_length:
            print("Out of Bounds!")
            self.check_high_score(snake_len)
            exit(0)
            
        snake_occupied_positions.append((potential_new_head[0],potential_new_head[1]))

        if len(snake_occupied_positions) > snake_len: # check if snake has unfurled entirely
            self.free_positions.add(snake_occupied_positions[0])
            snake_occupied_positions = snake_occupied_positions[1:]
        
        if (potential_new_head[0],potential_new_head[1]) not in self.free_positions:
            print("OUROBOROS") # game over
            self.check_high_score(snake_len)
            exit(0)
            
        self.free_positions.remove((potential_new_head[0],potential_new_head[1]))
        
        return (potential_new_head, snake_occupied_positions)
        

    # could change to dictionary from (i,j) entry to correct emoji instead of maintaining lists
    def print_board(self, snake_pos_list, food_position):
        self.toggle = not self.toggle
        full_text_string = ''
        for i in range(10):
            print()
            full_text_string += '\n'
            print(self.title_card_content)
            full_text_string += self.title_card_content
            print()
            full_text_string += '\n'
            print()
            full_text_string += '\n'
            snake_len_counter = 0
            for i in range(self.board_width + 1):
                for j in range(self.board_length + 1):
                    if (j,i) in snake_pos_list:
                        print(self.current_snake_emojis[snake_len_counter], end='')
                        snake_len_counter += 1
                        self.avatar_counter = (self.avatar_counter + 1) % len(self.barbie_avatars)
                        # full_text_string += self.avatar
                        continue
                    if (j,i) == food_position:
                        print(self.food_emoji, end='')
                        full_text_string += self.food_emoji
                        continue
                    if i == self.board_width or i == 0 or j == self.board_length or j == 0:
                        if i % 2 == 0 and j % 2 == 0:
                            wall = self.wall_emoji_1 if self.toggle else self.wall_emoji_2
                            print(wall, end='')
                            full_text_string += wall
                        else:
                            wall = self.wall_emoji_2 if self.toggle else self.wall_emoji_1
                            print(wall, end='')
                            full_text_string += wall
                    else:
                        print('  ', end='')
                        full_text_string += '  '
                print()
                full_text_string += '\n'
        return full_text_string        
            
    def check_high_score(self, snake_len):
     if not self.high_score_enabled: exit()
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

# @app.route("/snake")
def run_game(): 
    g = game()  
    while True:
        preliminary_snake_text = g.print_board(g.full_snake_pos, g.food_position)
        # with open("aux/greeting_card.txt",'r') as greeting:
        #     greeting_msg = greeting.read()
        #     return f"<pre>{greeting_msg + preliminary_snake_text}</pre>", 200, {'Content-Type': 'text/html; charset=utf-8'}
        # return preliminary_snake_text
        g.direction = g.read_input(g.direction, seconds=g.seconds_to_move) or g.direction
        g.snake_head, g.full_snake_pos = g.update_position(g.direction, g.full_snake_pos, g.snake_head, g.snake_len)
        if tuple(g.snake_head) == g.food_position:
            next_avatar = g.full_avatar_list[g.next_avatar_position]
            g.current_snake_emojis.append(next_avatar)
            g.next_avatar_position = (g.next_avatar_position + 1) % len(g.full_avatar_list)
            g.snake_len += 1
            g.food_position = g.free_positions.pop()
            g.free_positions.add(g.food_position) # don't die if you hit the food
            g.food_emoji = g.food_emoji_list[randrange(0,len(g.food_emoji_list))]

@app.route("/")
def splash():
     with open("aux/greeting_card.txt",'r') as greeting:
            text_to_return = greeting.read()
            print(text_to_return)
            return f"<pre>{text_to_return}</pre>", 200, {'Content-Type': 'text/html'}

@app.route("/hello",methods=['GET', 'POST']) 
def hello(): 
	print("This sucks")
	return "Hello, Welcome to GeeksForGeekszzz"

if __name__ == "__main__":  
    # app.run(debug=True, host="0.0.0.0")
    run_game()
        
# make a dictionary from pixels to whether they're free or not for checking if you ate yourself
# then have the inverse of that. Dictionary from free/not free to list of all the free/not free
# cells, so you can randomly choose from the list. O(2n) memory but only
# O(n) time.    

# potential updates -- handle user I/O, choosing theme, in separate files. 
# give more than two themes
# make snake multi-emoji, at least with barbie
# make boarder move
# high score animation
# put on a web server
# can't start out of bounds even in god mode
# updated out of bounds and ourorbous animations - mention benzine
# make it mostly standard barbies, make the other barbies rare. 