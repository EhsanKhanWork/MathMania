import pygame 
import os
import random
import json
from loading import show_loading
from os import path

pygame.init()

def load_highscore():
    try:
        with open("highscores.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_highscore(scores):
    with open("highscores.json", "w") as f:
        json.dump(scores, f)

def run_game():    
    
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
        
        for (x, w, h), answer_val in platform_data:
            correct = (answer_val == math_manager.correct_answer)

            platform_list.append(Platform(x, platform_y, w, h, answer_val, correct))

        return platform_list

    def game_over_screen(screen, score, large_font, font, width, height):
        nonlocal highscore
        screen.fill(black)

        game_over_text = large_font.render("Game Over", True, white)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))

        score_text = large_font.render(f"Final Score: {score}", True, white)
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 4 + 80))

        # Check for new highscore
        if not highscore or len(highscore) < 5 or score > min(highscore):
            highscore.append(score)
            highscore.sort(reverse=True)
            highscore = highscore[:5]
            save_highscore(highscore)
            highscore_text = large_font.render(f"New Highscore: {score}!", True, (255, 255, 0))  # Yellow for new highscore
        else:
            highscore_text = large_font.render(f"Highscore: {highscore[0] if highscore else 0}", True, white)
        
        screen.blit(highscore_text, (width // 2 - highscore_text.get_width() // 2, height // 4 + 160))

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

    score = 0
    highscore = load_highscore()
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
                    paused_time += pygame.time.get_ticks() - pause_start_time
            # Resume or Menu button click handling
                elif game_state == pause_state:
                    menu_btn, resume_btn = pause_menu()
            #   Resume button   
                    if resume_btn.collidepoint(event.pos):
                        game_state = playing_state
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

            if elapsed_time >= time_limit:
                game_state = gameover_state

            for platform in platforms:
              
                if player_rect.colliderect(platform) and player_vel_y >= 0:
                    if prev_player_bottom <= platform.top:
                        
                        if platform.correct:

                            pygame.mixer.Sound.play(this_sound)
                            pygame.mixer.music.stop()

                            score += 10
                            print(f"Correct! Score {score}")
                            
                            next_level() # Move to next level
                            
                            player_vel_y = -8
                            grounded = False
                        
                            break 
                        
                        else:
                            print("Game Over.")
                            game_state = gameover_state
                            pygame.mixer.Sound.play(jump_sound)
                            pygame.mixer.music.stop()
                            continue

                    
                    if prev_player_bottom <= platform.top:
                        player_rect.bottom = platform.top 
                        player_vel_y = 0
                        grounded = True 
            
        
            # Ground collision
            if player_rect.bottom > floor_height:
                player_rect.bottom = floor_height
                player_vel_y = 0 
                grounded = True
        
            # Screen bounds checks
            if player_rect.left < 0:
                player_rect.left = 0
                player_vel_x = 0
            if player_rect.right > width:
                player_rect.right = width
                player_vel_x = 0
        
            screen.fill(black)

            # Draw elements
            screen.blit(background, (0, 0))
            screen.blit(pause_button, pause_rect)
            
            problem_text = font.render(math_manager.current_problem, True, white)
            screen.blit(problem_text, (width // 2 - problem_text.get_width() // 2, 50))
            
            score_text = font.render(f"Score: {score}", True, white)
            screen.blit(score_text, (10, 10))
           
            highscore_text = font.render(f"Highscore: {highscore[0] if highscore else 0}", True, white)
            screen.blit(highscore_text, (10, 40))
           
            time_left = max(0, time_limit - elapsed_time)
            timer_text = font.render(f"Time:{int(time_left)}", True, black)
            timer_rect = timer_text.get_rect(center=(width // 2, 15))
            screen.blit(timer_text, timer_rect)

            for platform in platforms:
                # Added visual difference for correct platform
                pygame.draw.rect(screen, white, platform)

                answer_val_text = answer_font.render(str(platform.value), True, black)
                screen.blit(answer_val_text, (platform.centerx - answer_val_text.get_width() // 2, platform.centery - answer_val_text.get_height() // 2))

            blit_rect = player_rect.copy()
            blit_rect.y += visual_offset
            screen.blit(helicopter_image, blit_rect)

            pygame.draw.line(screen, (white), (0, floor_height), (width, floor_height), 5)
        
            pygame.display.flip()

        elif game_state == gameover_state: 
            game_over_screen(screen, score, large_font, font, width, height)

        elif game_state == pause_state:

            screen.blit(background, (0, 0))
            screen.blit(pause_button, pause_rect)

            problem_text = font.render(math_manager.current_problem, True, white)
            screen.blit(problem_text, (width // 2 - problem_text.get_width() // 2, 50))

            score_text = font.render(f"Score: {score}", True, white)
            screen.blit(score_text, (10, 10))

            highscore_text = font.render(f"Highscore: {highscore[0] if highscore else 0}", True, white)
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