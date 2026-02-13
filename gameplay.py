import pygame 
import os
import random
from loading import show_loading
from os import path

pygame.init()

def load_highscore():
    with open("save.txt", "r") as f:
        return int(f.read())

def save_highscore(score):
    with open("save.txt", "w") as f:
        f.write(str(score))

def load_time():
    with open("time.txt", "r") as f:
        return int(f.read())

def save_time(time):
    with open("time.txt", "w") as f:
        f.write(str(time))

def run_game(difficulty):    
    
    playing_state = 1 
    gameover_state = 2 
    pause_state = 3

    large_font = pygame.font.Font(None, 72)
    font = pygame.font.Font(None, 36)
    answer_font = pygame.font.Font(None, 30)

    class Platform(pygame.Rect):
        def __init__(self, x, y, w, h, value, correct):
            super().__init__(x, y, w, h)
            self.value = value 
            self.correct = correct

    class MathManager:
        def __init__(self, max_number=10):
            self.max_number = max_number
            self.current_problem = ""
            self.correct_answer = 0
            self.generate_problem()

        def generate_problem(self):
            operation = random.choice(["+", "-", "*", "/"])
            num1 = random.randint(1, self.max_number)
            num2 = random.randint(1, self.max_number)

            if operation == "+":
                self.correct_answer = num1 + num2
                self.current_problem = f"What is {num1} + {num2}?"
            elif operation == "-":
                num1 = max(num1, num2)
                num2 = min(num1, num2)
                self.correct_answer = num1 - num2
                self.current_problem = f"What is {num1} - {num2}?"
            elif operation == "*":
                self.correct_answer = num1 * num2
                self.current_problem = f"What is {num1} x {num2}?"
            elif operation == "/":
                self.correct_answer = num1
                num1 = num1 * num2
                self.current_problem = f"What is {num1} ÷ {num2}?"

        def generate_distractors(self, num_distractors=2):
            distractors = set()
            while len(distractors) < num_distractors:
                d = self.correct_answer + random.choice([-3, -2, -1, 1, 2, 3])
                if d > 0 and d != self.correct_answer:
                    distractors.add(d)
            return list(distractors)
        
        def answers_list(self, num_platforms=3):
            distractors = self.generate_distractors(num_platforms - 1)
            answers = [self.correct_answer] + distractors
            random.shuffle(answers)
            return answers

    width = 600 
    height = 800
    white = (255, 255, 255)
    black = (0, 0, 0)
    overlay = (black)
    panel_color = (white)

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Math Mania")

    show_loading(screen, width, height)
    pygame.time.delay(1000)

    start_time = pygame.time.get_ticks()

    font = pygame.font.Font(None, 36)
    answer_font = pygame.font.Font(None, 30)

    time_limit = 5
    question_timer = pygame.time.get_ticks()
    paused_time = 0
    pause_start_time = 0


    image = pygame.image.load(os.path.join('assets/helicopter.png'))
    helicopter_image = pygame.transform.scale(image, (100, 100))
    background = pygame.image.load(os.path.join('assets/background.jpg'))

    jump_sound = pygame.mixer.Sound(os.path.join("assets/this.mp3"))
    this_sound = pygame.mixer.Sound(os.path.join("assets/fahhh.wav"))
   
    pause_button = pygame.image.load(os.path.join('assets/pause.png'))
    pause_button = pygame.transform.scale(pause_button, (50, 50))

    pause_rect = pause_button.get_rect()
    pause_rect.top = 10
    pause_rect.right = width - 10

    player_rect = helicopter_image.get_rect()
    player_rect.x = 150
    floor_height = 750
    player_rect.y = 500
    player_rect.bottom = 550
    player_vel_y = 0
    GRAVITY = 0.4
    player_vel_x = 0
    speed = 5
    visual_offset = 15
    resisting_bottom = floor_height + visual_offset
    buffer = 2


    player_rect.bottom = resisting_bottom - visual_offset
    grounded = True

    def generate_platforms(math_manager, num_platforms=3):
        platform_list = []
        platform_y = 550
        platforms_specs = [(450, 100, 20), (250, 100, 20), (50, 100, 20)]
        answers = math_manager.answers_list(num_platforms)

        platform_data = list(zip(platforms_specs, answers))
        #combines platforms with answers and it is shuffled in math manager answers list function
        
        for (x, w, h), answer_val in platform_data:
            correct = (answer_val == math_manager.correct_answer)

            platform_list.append(Platform(x, platform_y, w, h, answer_val, correct))

        return platform_list

    def game_over_screen(screen, score, time_survived, large_font, font, width, height):
        nonlocal highscore, best_time
        screen.fill(black)

        game_over_text = large_font.render("Game Over", True, white)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))

        score_text = large_font.render(f"Final Score: {score}", True, white)
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 4 + 80))

        time_text = large_font.render(f"Time Survived: {time_survived:.2f}s", True, white)
        screen.blit(time_text, (width // 2 - time_text.get_width() // 2, height // 4 + 120))

        # Check for new highscore
        if score > highscore:
            highscore = score
            save_highscore(highscore)
            highscore_text = large_font.render(f"New Highscore: {highscore}!", True, (255, 255, 0))  # Yellow for new highscore
        else:
            highscore_text = large_font.render(f"Highscore: {highscore}", True, white)
        
        screen.blit(highscore_text, (width // 2 - highscore_text.get_width() // 2, height // 4 + 160))

        # Check for new best time
        if time_survived > best_time:
            best_time = time_survived
            save_time(int(best_time))
            best_time_text = large_font.render(f"New Best Time: {best_time:.2f}s!", True, (255, 255, 0))
        else:
            best_time_text = large_font.render(f"Best Time: {best_time:.2f}s", True, white)
        
        screen.blit(best_time_text, (width // 2 - best_time_text.get_width() // 2, height // 4 + 200))

        restart_text = font.render("Press SPACE to Try Again", True, white)
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 100))

        menu_text = font.render("Press M for Main Menu", True, white)
        screen.blit(menu_text, (width // 2 - menu_text.get_width() // 2, height // 2 + 150))

        pygame.display.flip()
    

    def next_level():
        nonlocal math_manager, platforms, question_timer
        nonlocal player_vel_x, player_vel_y, grounded
        
        math_manager.generate_problem()
        platforms = generate_platforms(math_manager)

        question_timer = pygame.time.get_ticks()

        player_rect.x = 150
        player_rect.bottom = floor_height
        player_vel_y = 0
        player_vel_x = 0
        grounded = True
        paused_time = 0

    def reset_game():
        nonlocal score, game_state, question_timer
        nonlocal player_vel_y, player_vel_x, grounded

        score = 0 
        game_state = playing_state
        question_timer = pygame.time.get_ticks()
        
        next_level()

    def pause_menu():
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(50, 200, width - 100, 300)
        pygame.draw.rect(screen, panel_color, panel, border_radius=25)
        pygame.draw.rect(screen, black, panel, 2, border_radius=25)

        title = large_font.render("Paused", True, black)
        screen.blit(title, title.get_rect(center=(width // 2, panel.y + 60)))

        resume_btn = pygame.Rect(panel.x + 40, panel.y + 140, panel.width - 80, 50)
        menu_btn = pygame.Rect(panel.x + 40, panel.y + 210, panel.width - 80, 50)

        mouse_pos = pygame.mouse.get_pos()

        for btn, text in [(resume_btn, "Resume", ), (menu_btn, 'Main Menu')]:
            pygame.draw.rect(screen, panel_color, btn, border_radius=12)
            pygame.draw.rect(screen, panel_color, btn, border_radius=12)
            txt = font.render(text, True, black)
            screen.blit(txt, txt.get_rect(center=btn.center))

        return menu_btn, resume_btn

    def update_timer(survival_time):
        nonlocal question_timer
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - question_timer - paused_time) / 1000
        return elapsed_time


    score = 0
    highscore = load_highscore()
    best_time = load_time()
    time_survived = 0
    math_manager = MathManager(max_number=10)
    platforms = generate_platforms(math_manager)
    game_state = playing_state

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            
            if event.type == pygame.KEYDOWN:
                if game_state == playing_state:
                    if event.key == pygame.K_SPACE and grounded:
                        player_vel_y = -15
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player_vel_x = -speed
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player_vel_x = speed

                elif game_state == gameover_state:
                    if event.key == pygame.K_SPACE:
                        reset_game()
                    if event.key == pygame.K_m:
                        return 'menu'

            if event.type == pygame.KEYUP and game_state == playing_state:   
                # Prevents continuous movement when key is released
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if player_vel_x < 0:
                        player_vel_x = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if player_vel_x > 0:
                        player_vel_x = 0
            
            if event.type == pygame.MOUSEBUTTONDOWN:
            # Pause button click handling
                if game_state == playing_state and pause_rect.collidepoint(event.pos):
                    game_state = pause_state
                    pause_start_time = pygame.time.get_ticks()
                    # start tracking paused time when game is paused
            # Resume or Menu button click handling
                elif game_state == pause_state:
                    menu_btn, resume_btn = pause_menu()
            #   Resume button   
                    if resume_btn.collidepoint(event.pos):
                        game_state = playing_state
                        paused_time += pygame.time.get_ticks() - pause_start_time
                         # update paused time so timer continues from where it left off
                    # Menu button
                    elif menu_btn.collidepoint(event.pos):
                        return 'menu'

        if game_state == playing_state:
            prev_player_bottom = player_rect.bottom
            grounded = False

            player_vel_y += GRAVITY
            player_rect.y += player_vel_y
            player_rect.x += player_vel_x

            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - question_timer - paused_time) / 1000
            elapsed_time = max(0, min(elapsed_time, time_limit))  # Cap elapsed time at time limit
            

            if elapsed_time >= time_limit:
                time_survived = (pygame.time.get_ticks() - start_time) / 1000
                game_state = gameover_state

            for platform in platforms:
              # Check collision with platforms
                if player_rect.colliderect(platform) and player_vel_y >= 0:
                    if prev_player_bottom <= platform.top:
                        if platform.correct:
                            pygame.mixer.Sound.play(this_sound)
                            pygame.mixer.music.stop()
                            score += 10    # Increase score
                            next_level()   # Go to next level
                            player_vel_y = -8  # Makes the player bounce slightly
                            grounded = False
                            break 
                        else:
                            time_survived = (pygame.time.get_ticks() - start_time) / 1000 
                            # time_survived calculation
                            # Wrong answer - Game Over
                            game_state = gameover_state
                            # game state changes to game over
                            pygame.mixer.Sound.play(jump_sound)
                            # play wrong answer sound
                            pygame.mixer.music.stop()
                            break # exit platform loop
                    if prev_player_bottom <= platform.top: 
                        # Check that the player landed on top
                        player_rect.bottom = platform.top 
                        player_vel_y = 0 
                        # Stop vertical movement
                        grounded = True 
                        # Player is on the platform
            
        
            
            if player_rect.bottom > floor_height:
                # Ensure player doesn't fall below floor
                player_rect.bottom = floor_height
                # Aligns player with floor
                player_vel_y = 0 
                # Vertical velocity reset
                grounded = True
        
            
            if player_rect.left < 0:
                player_rect.left = 0
                player_vel_x = 0
            if player_rect.right > width:
                player_rect.right = width
                player_vel_x = 0
        
            # Drawing all on screen elements 
            screen.fill(black) # Clear the screen before redrawing
            screen.blit(background, (0, 0)) # Draw background
            screen.blit(pause_button, pause_rect) # Draw pause button
            problem_text = font.render(math_manager.current_problem, True, white) # Render problem text 
            screen.blit(problem_text, (width // 2 - problem_text.get_width() // 2, 50)) 
            score_text = font.render(f"Score: {score}", True, white)  # Render score text
            screen.blit(score_text, (10, 10))
            highscore_text = font.render(f"Highscore: {highscore}", True, white) # render highscore text
            screen.blit(highscore_text, (10, 40))
           
           # Calculate remaining time, ensure it doesn't go negative
            time_left = max(0, time_limit - elapsed_time)
            # Render timer text
            timer_text = font.render(f"Time:{int(time_left)}", True, black)
            # Centre the timer at the top
            timer_rect = timer_text.get_rect(center=(width // 2, 15))
            screen.blit(timer_text, timer_rect)

            for platform in platforms:
                # Added visual difference for correct platform
                pygame.draw.rect(screen, white, platform)

                answer_val_text = answer_font.render(str(platform.value), True, black)
                screen.blit(answer_val_text, (platform.centerx - answer_val_text.get_width() // 2, 
                platform.centery - answer_val_text.get_height() // 2))

            blit_rect = player_rect.copy()
            blit_rect.y += visual_offset
            screen.blit(helicopter_image, blit_rect)

            pygame.draw.line(screen, (white), (0, floor_height), (width, floor_height), 5)
        
            pygame.display.flip()

        elif game_state == gameover_state: 
            game_over_screen(screen, score, time_survived, large_font, font, width, height)

        elif game_state == pause_state:

            screen.blit(background, (0, 0))
            screen.blit(pause_button, pause_rect)

            problem_text = font.render(math_manager.current_problem, True, white)
            screen.blit(problem_text, (width // 2 - problem_text.get_width() // 2, 50))

            score_text = font.render(f"Score: {score}", True, white)
            screen.blit(score_text, (10, 10))

            highscore_text = font.render(f"Highscore: {highscore}", True, white)
            screen.blit(highscore_text, (10, 40))

            for platform in platforms:
                # Added visual difference for correct platform
                pygame.draw.rect(screen, white, platform)

                answer_val_text = answer_font.render(str(platform.value), True, black)
                screen.blit(answer_val_text, (platform.centerx - answer_val_text.get_width() // 2, platform.centery - answer_val_text.get_height() // 2))

            blit_rect = player_rect.copy()
            blit_rect.y += visual_offset
            screen.blit(helicopter_image, blit_rect)

            pause_menu()
            pygame.display.flip()

    pygame.quit()