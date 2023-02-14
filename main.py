import pygame
import time
import random 

pygame.init()

# Initiallizing the screen
WIDTH = 1000
HEIGHT = 800
SCREEN_COLOR = (250, 250, 170, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(SCREEN_COLOR)

# End game screen
def end_screen(score):
    # Text Font
    my_font = "arial"
    
    # Update screen background
    screen.fill(SCREEN_COLOR)
    
    # Display the end game screen
    font = pygame.font.SysFont(my_font, 50)
    text = font.render("Game Over", True, (0, 0, 0))
    screen.blit(text, (WIDTH/2 - 100, HEIGHT/2 - 200))
    
    # Display the final score
    font = pygame.font.SysFont(my_font, 32)
    text = font.render("Final Score: " + str(score), True, (0, 0, 0))
    screen.blit(text, (WIDTH/2 - 100, HEIGHT/2 - 120))
    
    # Display the button to restart the game
    pygame.draw.rect(screen, (0, 75, 150,100), (WIDTH/2 - 100, HEIGHT/2 - 25, 200, 150))
    font = pygame.font.SysFont(my_font, 50)
    text = font.render("Restart", True, (0, 0, 0))
    screen.blit(text, (WIDTH/2 - 90, HEIGHT/2))

# Board rectangles size
size = 100
# Border size
border_size= 1

# Range of numbers on the board
nums_range = 250
# Board numbers
board_nums = [random.randint(0, nums_range) for i in range(1, 37)]
board_nums.sort()
# Board number highights (0 = not highlighted, 1 = highlighted)
board_nums_highlight = [0 for i in range(36)]

# Board offsets
board_width = 5 * (size + border_size) + border_size + size + border_size
board_x = WIDTH / 2 - board_width / 2
board_y = 60

# Highlight color
highlight_color = (0, 125, 255,100)

# Text Font
my_font = "comicsansms"

# Current Score
current_score = 0

# Board cover 
board_cover = True

# Calculating the dice
dice = [random.randint(2, 10), random.randint(2, 10), random.randint(1, 20)]
dice_string = str(dice[0]) + " " + str(dice[1]) + " " + str(dice[2]) 

# Game start time
game_start_time = time.time()
game_time = 60

end_game = False
        
while True:
    
    # Update screen background
    screen.fill(SCREEN_COLOR)
    
    # Update events
    event_list = pygame.event.get()
    
    current_score = 0
    
    # Create the black background for just the board
    pygame.draw.rect(screen, (0, 0, 0), (board_x, board_y, board_width, board_width))
    
    # Drawing the rectangles for the board
    for i in range(6):
        for j in range(6):
            
            x = board_x + i * (size + border_size) + border_size
            y = board_y + j * (size + border_size) + border_size
            
            if board_nums_highlight[i + 6 * j] == 1:
                pygame.draw.rect(screen, highlight_color, (x, y, size, size))
            else:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, size, size))
            
    # Draw the board numbers
    for i in range(6):
        for j in range(6):
            
            x = board_x + i * (size + border_size) + border_size
            y = board_y + j * (size + border_size) + border_size
            
            font = pygame.font.SysFont(my_font, 50)
            
            current_num = i + 6 * j
            text = font.render(str(board_nums[current_num]), True, (0, 0, 0))
            
            # Format the numbers as centered
            if board_nums[current_num] < 10:
                screen.blit(text, (x + 20, y + 8))
            elif board_nums[current_num] < 100:
                screen.blit(text, (x + 12, y + 8))
            else:
                screen.blit(text, (x + 4, y + 8))
            
    # Check if the user clicks on any of the numbers on the board
    for i in range(6):
        for j in range(6):
            
            x = board_x + i * (size + border_size) + border_size
            y = board_y + j * (size + border_size) + border_size           
            
            # Check if the user clicks on the current rectangle and highlight accirdingly
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 \
                                 and pygame.Rect(x, y, size, size).collidepoint(pygame.mouse.get_pos())\
                                 and not board_cover:
                    if board_nums_highlight[i + 6 * j] == 1:
                        board_nums_highlight[i + 6 * j] = 0
                    else:
                        board_nums_highlight[i + 6 * j] = 1             
                
    # Board cover
    if board_cover:
        pygame.draw.rect(screen, (0, 125, 255,100), (board_x, board_y, board_width, board_width))
        
    # Make a button to start the game that is located in the middle of the board 
    # This button will remove the board cover
    if board_cover:       
        # Draw the button 
        pygame.draw.rect(screen, (0, 75, 150,100), (WIDTH/2 - 100, board_y + 225, 200, 150))
        font = pygame.font.SysFont(my_font, 50)
        text = font.render("Begin", True, (0, 0, 0))
        screen.blit(text, (WIDTH/2 - 70, board_y + 250))
        
        # Check if the user clicks on the button
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 \
                            and pygame.Rect(WIDTH/2 - 100, board_y + 225, 200, 150).collidepoint(pygame.mouse.get_pos()):
                board_cover = False
                game_start_time = time.time()
                time.sleep(0.2)
                
    # Update the current score
    for index, val in enumerate(board_nums_highlight):
        if val == 1:
            current_score += board_nums[index]
    
    # Display the current score
    font = pygame.font.SysFont(my_font, 32)
    text = font.render("Current Score: " + str(current_score), True, (0, 0, 0))
    screen.blit(text, (board_x + 180, board_y - 50))
    
    # Display the dice
    text = font.render("Dice: " + dice_string, True, (0, 0, 0))
    screen.blit(text, (WIDTH/2 -100, board_y + 625))
    
    # Add a one minute timer that starts when the game begins
    if not board_cover:
        text = font.render("Time left: " + str(int(game_time - (time.time() - game_start_time))), True, (0, 0, 0))
        screen.blit(text, (WIDTH/2 - 100, board_y + 675))
        
        # Check if the time is up
        if int(game_time - (time.time() - game_start_time)) <= 0:
            end_game = True
    
    if end_game:
        # Put the board cover back on so the user can't click on the board
        board_cover = True
        end_screen(current_score)
        
        # Check if the user clicks on the restart button
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 \
                            and pygame.Rect(WIDTH/2 - 100, HEIGHT/2 - 25, 200, 150).collidepoint(pygame.mouse.get_pos()):
                game_start_time = time.time()
                end_game = False
                # Board numbers
                board_nums = [random.randint(0, nums_range) for i in range(1, 37)]
                board_nums.sort()
                # Board number highights (0 = not highlighted, 1 = highlighted)
                board_nums_highlight = [0 for i in range(36)]
                # Dice
                dice = [random.randint(2, 10), random.randint(2, 10), random.randint(1, 20)]
                dice_string = str(dice[0]) + " " + str(dice[1]) + " " + str(dice[2]) 
    
    # Update the screen
    pygame.display.update()
        
    for event in event_list:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()