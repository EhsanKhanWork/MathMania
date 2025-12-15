import pygame 
import os
import random

pygame.init()

def new_run_game():
    width = 1000 
    height = 1200
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Maths Mania")

    start_game()

def start_game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def run_game():    
    
    playing_state = 1 
    gameover_state = 2 

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
            self.generate_new_problem()

        def generate_new_problem(self):
            num1 = random.randint(1, self.max_number)
            num2 = random.randint(1, self.max_number)
            self.correct_answer = num1 + num2
            self.current_problem = f"What is {num1} + {num2}?"

        def generate_distractors(self, num_distractors=2):
            distractors = set()
            while len(distractors) < num_distractors:
                d = self.correct_answer + random.choice([-3, -2, -1, 1, 2, 3])
                if d > 0 and d != self.correct_answer:
                    distractors.add(d)
            return list(distractors)
        
        def generate_answers_list(self, num_platforms=3):
            distractors = self.generate_distractors(num_platforms - 1)
            answers = [self.correct_answer] + distractors
            random.shuffle(answers)
            return answers

    # List of Variables ------------------------------------
    width = 600 
    height = 800
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0) # Added color for correct answer

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Math Mania")

    font = pygame.font.Font(None, 36)
    answer_font = pygame.font.Font(None, 30)


    image = pygame.image.load(os.path.join('assets/helicopter.png'))
    helicopter_image = pygame.transform.scale(image, (100, 100))

    background = pygame.image.load(os.path.join('assets/background.jpg'))

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
        answers = math_manager.generate_answers_list(num_platforms)

        platform_data = list(zip(platforms_specs, answers))
        
        for (x, w, h), answer_val in platform_data:
            correct = (answer_val == math_manager.correct_answer)

            platform_list.append(Platform(x, platform_y, w, h, answer_val, correct))

        return platform_list
    # ----------------------------------------------------

    def draw_game_over_screen(screen, score, large_font, font, width, height):
        screen.fill(black)

        game_over_text = large_font.render("Game Over", True, white)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))

        score_text = large_font.render(f"Final Score: {score}", True, white)
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 4 + 80))

        restart_text = font.render("Press SPACE to Try Again", True, white)
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 100))

        pygame.display.flip()

    def next_level():
        global math_manager, platforms
        
        math_manager.generate_new_problem()
        platforms = generate_platforms(math_manager)

        player_rect.x = 150
        player_rect.bottom = floor_height
        player_vel_y = 0
        player_vel_x = 0
        grounded = True

    def reset_game():
        global score, game_state, player_rect, player_vel_y, player_vel_x, grounded

        score = 0 
        game_state = playing_state
        
        next_level()


    score = 0
    math_manager = MathManager(max_number=10)
    platforms = generate_platforms(math_manager)
    game_state = playing_state

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
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

            if event.type == pygame.KEYUP and game_state == playing_state:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if player_vel_x < 0:
                        player_vel_x = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if player_vel_x > 0:
                        player_vel_x = 0
        
        if game_state == playing_state:
            prev_player_bottom = player_rect.bottom
            grounded = False

            player_vel_y += GRAVITY
            player_rect.y += player_vel_y
            player_rect.x += player_vel_x


            for platform in platforms:
                # Collision check: Landing on top of a platform
                if player_rect.colliderect(platform) and player_vel_y >= 0:
                    if prev_player_bottom <= platform.top:
                        
                        if platform.correct:

                            score += 10
                            print(f"Correct! Score {score}")
                            
                            next_level() # Generate new platforms
                            
                            player_vel_y = -8
                            grounded = False
                            
                            # Crucial Fix: Exit the platform loop immediately
                            # to prevent collision with the new platforms in this frame.
                            break 
                            # -------------------------
                        else:
                            print("Incorrect! Game Over.")
                            game_state = gameover_state
                            continue

                    # Normal landing logic (applies only if not transitioning to next level)
                    # Note: This block is now skipped if 'break' is executed above.
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
            problem_text = font.render(math_manager.current_problem, True, white)
            screen.blit(problem_text, (width // 2 - problem_text.get_width() // 2, 50))
            score_text = font.render(f"Score: {score}", True, white)
            screen.blit(score_text, (10, 10))

            for platform in platforms:
                # Added visual difference for correct platform
                platform_color = green if platform.correct else white 
                pygame.draw.rect(screen, platform_color, platform)

                answer_val_text = answer_font.render(str(platform.value), True, black)
                screen.blit(answer_val_text, (platform.centerx - answer_val_text.get_width() // 2, platform.centery - answer_val_text.get_height() // 2))

            blit_rect = player_rect.copy()
            blit_rect.y += visual_offset
            screen.blit(helicopter_image, blit_rect)

            pygame.draw.line(screen, (white), (0, floor_height), (width, floor_height), 5)
        
            pygame.display.flip()

        elif game_state == gameover_state: 
            draw_game_over_screen(screen, score, large_font, font, width, height)

    pygame.quit()