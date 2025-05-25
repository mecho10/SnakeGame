import pygame
import sys
import os
import random
import math
from auth import register_user, login_user, get_user_info, update_high_score, load_users

# 初始化 Pygame
pygame.init()

WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("貪食蛇遊戲系統")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
BLUE = (70, 130, 180)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
DARK_GREEN = (0, 100, 0)
BACKGROUND = (40, 44, 52)
ORANGE = (255, 165, 0)
PURPLE = (147, 112, 219)
CYAN = (0, 255, 255)

GRID_SIZE = 20
GRID_WIDTH = WINDOW_SIZE[0] // GRID_SIZE
GRID_HEIGHT = (WINDOW_SIZE[1] - 100) // GRID_SIZE

# 中文字體設定
def load_chinese_font():
    """載入中文字體"""
    chinese_fonts = [
        # Windows
        "C:/Windows/Fonts/msyh.ttc",      
        "C:/Windows/Fonts/simhei.ttf",    
        "C:/Windows/Fonts/simsun.ttc", 
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        # Linux
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]
    
    for font_path in chinese_fonts:
        if os.path.exists(font_path):
            try:
                return (pygame.font.Font(font_path, 36),  
                       pygame.font.Font(font_path, 24),  
                       pygame.font.Font(font_path, 20),  
                       pygame.font.Font(font_path, 16))
            except:
                continue
    
    # 如果找不到中文字體，使用默認字體
    print("警告: 未找到中文字體，使用默認字體")
    return (pygame.font.Font(None, 40), 
           pygame.font.Font(None, 28), 
           pygame.font.Font(None, 24), 
           pygame.font.Font(None, 20))

# 載入字體
big_title_font, title_font, normal_font, small_font = load_chinese_font()

class IntroAnimation:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()
        self.duration = 4000 
        self.finished = False
        self.logo_scale = 0
        self.text_alpha = 0
        self.snake_positions = []
        self.food_positions = []
        self.sparkles = []
        self.init_effects()
    
    def init_effects(self):
        for i in range(20):
            x = random.randint(50, WINDOW_SIZE[0] - 50)
            y = random.randint(100, WINDOW_SIZE[1] - 100)
            self.snake_positions.append([x, y, random.uniform(0, 2*math.pi)])
        
        for i in range(10):
            x = random.randint(50, WINDOW_SIZE[0] - 50)
            y = random.randint(100, WINDOW_SIZE[1] - 100)
            self.food_positions.append([x, y, random.uniform(0, 1)])
        
        for i in range(30):
            x = random.randint(0, WINDOW_SIZE[0])
            y = random.randint(0, WINDOW_SIZE[1])
            self.sparkles.append([x, y, random.uniform(0, 1), random.uniform(1, 3)])
    
    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        
        if progress >= 1.0:
            self.finished = True
            return
        
        if progress < 0.3:
            self.logo_scale = progress / 0.3
        elif progress < 0.6:
            self.logo_scale = 1.0
        else:
            self.logo_scale = 1.0
            self.text_alpha = (progress - 0.6) / 0.4 * 255
        
        for pos in self.snake_positions:
            pos[2] += 0.05
            pos[0] += math.cos(pos[2]) * 2
            pos[1] += math.sin(pos[2]) * 1
            
            if pos[0] < 0 or pos[0] > WINDOW_SIZE[0]:
                pos[0] = random.randint(50, WINDOW_SIZE[0] - 50)
            if pos[1] < 0 or pos[1] > WINDOW_SIZE[1]:
                pos[1] = random.randint(100, WINDOW_SIZE[1] - 100)
        
        for pos in self.food_positions:
            pos[2] += 0.02
            if pos[2] > 1:
                pos[2] = 0
        
        for sparkle in self.sparkles:
            sparkle[2] += 0.05
            if sparkle[2] > 1:
                sparkle[2] = 0
                sparkle[0] = random.randint(0, WINDOW_SIZE[0])
                sparkle[1] = random.randint(0, WINDOW_SIZE[1])
    
    def draw(self, screen):
        for y in range(WINDOW_SIZE[1]):
            color_value = int(40 + (y / WINDOW_SIZE[1]) * 20)
            color = (color_value, color_value + 4, color_value + 8)
            pygame.draw.line(screen, color, (0, y), (WINDOW_SIZE[0], y))
        
        for i, pos in enumerate(self.snake_positions):
            alpha = int(100 * math.sin(pos[2]) ** 2)
            if alpha > 0:
                size = 15 + int(5 * math.sin(pos[2] * 2))
                color = (*GREEN, alpha) if i % 2 == 0 else (*DARK_GREEN, alpha)
                surf = pygame.Surface((size, size))
                surf.set_alpha(alpha)
                surf.fill(GREEN if i % 2 == 0 else DARK_GREEN)
                screen.blit(surf, (int(pos[0]), int(pos[1])))
        
        for pos in self.food_positions:
            alpha = int(150 * pos[2])
            if alpha > 0:
                size = int(10 + 5 * pos[2])
                surf = pygame.Surface((size, size))
                surf.set_alpha(alpha)
                surf.fill(RED)
                screen.blit(surf, (int(pos[0]), int(pos[1])))
        
        # 繪製閃爍特效
        for sparkle in self.sparkles:
            if sparkle[2] < 0.5:
                alpha = int(255 * (sparkle[2] * 2))
                size = int(sparkle[3])
                surf = pygame.Surface((size, size))
                surf.set_alpha(alpha)
                surf.fill(WHITE)
                screen.blit(surf, (int(sparkle[0]), int(sparkle[1])))
        
        if self.logo_scale > 0:
            
            title_text = "貪食蛇遊戲"
            title_surface = big_title_font.render(title_text, True, WHITE)
            
            
            if self.logo_scale < 1.0:
                scaled_width = int(title_surface.get_width() * self.logo_scale)
                scaled_height = int(title_surface.get_height() * self.logo_scale)
                title_surface = pygame.transform.scale(title_surface, (scaled_width, scaled_height))
            
            title_rect = title_surface.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 - 50))
            screen.blit(title_surface, title_rect)
            
            
            if self.logo_scale >= 0.8:
                subtitle = "Snake Game System"
                subtitle_surface = title_font.render(subtitle, True, CYAN)
                subtitle_rect = subtitle_surface.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2 + 10))
                screen.blit(subtitle_surface, subtitle_rect)
        
        
        if self.text_alpha > 0:
            copyright_text = "Copyright by Leroy Chang"
            copyright_surface = normal_font.render(copyright_text, True, WHITE)
            copyright_surface.set_alpha(int(self.text_alpha))
            copyright_rect = copyright_surface.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1] - 100))
            screen.blit(copyright_surface, copyright_rect)
            
            
            loading_text = "Loading..."
            loading_surface = small_font.render(loading_text, True, GRAY)
            loading_surface.set_alpha(int(self.text_alpha))
            loading_rect = loading_surface.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1] - 50))
            screen.blit(loading_surface, loading_rect)

class Leaderboard:
    def __init__(self):
        self.visible = False
        self.top_players = []
        self.update_leaderboard()
    
    def update_leaderboard(self):
        """更新排行榜數據"""
        users = load_users()
        sorted_users = sorted(users.items(), 
                            key=lambda x: x[1].get('high_score', 0), 
                            reverse=True)
        self.top_players = sorted_users[:5]
    
    def toggle_visibility(self):
        """切換排行榜顯示狀態"""
        self.visible = not self.visible
        if self.visible:
            self.update_leaderboard()
    
    def draw(self, screen):
        if not self.visible:
            return

        overlay = pygame.Surface(WINDOW_SIZE)
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        board_width = 400
        board_height = 350
        board_x = (WINDOW_SIZE[0] - board_width) // 2
        board_y = (WINDOW_SIZE[1] - board_height) // 2
        
        pygame.draw.rect(screen, BACKGROUND, (board_x, board_y, board_width, board_height))
        pygame.draw.rect(screen, WHITE, (board_x, board_y, board_width, board_height), 3)
        
        title_text = title_font.render("🏆 排行榜 Top 5", True, YELLOW)
        title_rect = title_text.get_rect(center=(WINDOW_SIZE[0]//2, board_y + 40))
        screen.blit(title_text, title_rect)
        
        if not self.top_players:
            no_data_text = normal_font.render("暫無排行榜數據", True, GRAY)
            no_data_rect = no_data_text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2))
            screen.blit(no_data_text, no_data_rect)
        else:
            start_y = board_y + 80
            for i, (username, user_data) in enumerate(self.top_players):
                rank = i + 1
                score = user_data.get('high_score', 0)
                if rank == 1:
                    rank_color = YELLOW  
                elif rank == 2:
                    rank_color = LIGHT_GRAY  
                elif rank == 3:
                    rank_color = ORANGE  
                else:
                    rank_color = WHITE
            
                rank_text = normal_font.render(f"#{rank}", True, rank_color)
                screen.blit(rank_text, (board_x + 30, start_y + i * 40))
                name_text = normal_font.render(username, True, WHITE)
                screen.blit(name_text, (board_x + 80, start_y + i * 40))
                score_text = normal_font.render(f"{score} 分", True, GREEN)
                screen.blit(score_text, (board_x + 280, start_y + i * 40))

        close_text = small_font.render("按 TAB 鍵關閉", True, GRAY)
        close_rect = close_text.get_rect(center=(WINDOW_SIZE[0]//2, board_y + board_height - 30))
        screen.blit(close_text, close_rect)

class InputBox:
    def __init__(self, x, y, w, h, text='', is_password=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = LIGHT_GRAY
        self.text = text
        self.is_password = is_password
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = WHITE if self.active else LIGHT_GRAY
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return 'enter'
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 30:
                        self.text += event.unicode
        return None

    def update(self, dt):
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= 500:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        display_text = '*' * len(self.text) if self.is_password else self.text
        text_surface = normal_font.render(display_text, True, BLACK)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 8))
        
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + text_surface.get_width()
            pygame.draw.line(screen, BLACK, 
                           (cursor_x, self.rect.y + 5), 
                           (cursor_x, self.rect.y + self.rect.height - 5), 2)

class Button:
    def __init__(self, x, y, w, h, text, color=BLUE):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30))
        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        
        text_surface = normal_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.body = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
        self.direction = (1, 0)
        self.grow = False
    
    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False

        if new_head in self.body:
            return False
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        
        return True
    
    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def eat_food(self):
        self.grow = True
    
    def draw(self, screen):
        for i, (x, y) in enumerate(self.body):
            color = DARK_GREEN if i == 0 else GREEN
            pygame.draw.rect(screen, color, 
                           (x * GRID_SIZE, y * GRID_SIZE + 100, GRID_SIZE-1, GRID_SIZE-1))

class Food:
    def __init__(self):
        self.position = self.generate_position()
    
    def generate_position(self):
        return (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
    
    def respawn(self, snake_body):
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break
    
    def draw(self, screen):
        x, y = self.position
        pygame.draw.rect(screen, RED, 
                        (x * GRID_SIZE, y * GRID_SIZE + 100, GRID_SIZE-1, GRID_SIZE-1))

class GameState:
    INTRO = "intro"
    LOGIN = "login"
    GAME = "game"
    GAME_OVER = "game_over"

class Game:
    def __init__(self):
        self.state = GameState.INTRO
        self.intro_animation = IntroAnimation()
        self.current_user = None
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.high_score = 0
        self.game_speed = 10
        self.last_move_time = 0
        self.leaderboard = Leaderboard()
        
        # 登入
        self.setup_login_ui()
        self.feedback_message = "請輸入用戶名和密碼"
        self.feedback_color = BLACK
        
    def setup_login_ui(self):
        self.username_input = InputBox(275, 200, 250, 35)
        self.password_input = InputBox(275, 260, 250, 35, is_password=True)
        self.login_button = Button(220, 320, 80, 40, "登入", BLUE)
        self.register_button = Button(320, 320, 80, 40, "註冊", GREEN)
        self.clear_button = Button(420, 320, 80, 40, "清空", GRAY)
        self.leaderboard_button = Button(270, 380, 120, 40, "排行榜", PURPLE)
    
    def update_feedback(self, message, is_success=False):
        self.feedback_message = message
        self.feedback_color = GREEN if is_success else RED
    
    def handle_login(self):
        username = self.username_input.text.strip()
        password = self.password_input.text
        
        if not username or not password:
            self.update_feedback("請輸入用戶名和密碼")
            return
        
        success, message = login_user(username, password)
        
        if success:
            self.current_user = username
            user_info = get_user_info(username)
            self.high_score = user_info.get('high_score', 0) if user_info else 0
            self.start_game()
        else:
            self.update_feedback(message)
    
    def handle_register(self):
        username = self.username_input.text.strip()
        password = self.password_input.text
        
        if not username or not password:
            self.update_feedback("請輸入用戶名和密碼")
            return
        
        success, message = register_user(username, password)
        self.update_feedback(message, success)
        
        if success:
            self.username_input.text = ""
            self.password_input.text = ""
    
    def clear_inputs(self):
        self.username_input.text = ""
        self.password_input.text = ""
        self.update_feedback("輸入框已清空")
    
    def start_game(self):
        self.state = GameState.GAME
        self.snake.reset()
        self.food.respawn(self.snake.body)
        self.score = 0
        self.game_speed = 10
        self.last_move_time = pygame.time.get_ticks()
        self.leaderboard.visible = False 
    
    def game_over(self):
        self.state = GameState.GAME_OVER
        if self.score > self.high_score:
            self.high_score = self.score
            update_high_score(self.current_user, self.score)
            self.leaderboard.update_leaderboard()
    
    def restart_game(self):
        self.start_game()
    
    def logout(self):
        self.state = GameState.LOGIN
        self.current_user = None
        self.clear_inputs()
        self.update_feedback("已登出，請重新登入")
        self.leaderboard.visible = False
    
    def handle_intro_events(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            if self.intro_animation.finished:
                self.state = GameState.LOGIN
    
    def handle_login_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self.leaderboard.toggle_visibility()
            return
        if self.leaderboard.visible:
            return
        
        username_result = self.username_input.handle_event(event)
        password_result = self.password_input.handle_event(event)
        
        if username_result == 'enter' or password_result == 'enter':
            if self.username_input.text.strip() and self.password_input.text:
                self.handle_login()
        if self.login_button.handle_event(event):
            self.handle_login()
        elif self.register_button.handle_event(event):
            self.handle_register()
        elif self.clear_button.handle_event(event):
            self.clear_inputs()
        elif self.leaderboard_button.handle_event(event):
            self.leaderboard.toggle_visibility()
    
    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                self.snake.change_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                self.snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                self.snake.change_direction((1, 0))
            elif event.key == pygame.K_ESCAPE:
                self.logout()
            elif event.key == pygame.K_TAB:
                self.leaderboard.toggle_visibility()
    
    def handle_game_over_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.restart_game()
            elif event.key == pygame.K_ESCAPE:
                self.logout()
            elif event.key == pygame.K_TAB:
                self.leaderboard.toggle_visibility()
    
    def update_game(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > (1000 // self.game_speed):
            if not self.snake.move():
                self.game_over()
                return
            
            # 檢查是否吃到食物
            if self.snake.body[0] == self.food.position:
                self.snake.eat_food()
                self.food.respawn(self.snake.body)
                self.score += 10
                # 增加遊戲速度
                if self.game_speed < 20:
                    self.game_speed += 0.5
            
            self.last_move_time = current_time
    
    def draw_intro_screen(self):
        self.intro_animation.draw(screen)
        if self.intro_animation.text_alpha > 100:
            skip_text = small_font.render("按任意鍵跳過", True, WHITE)
            skip_text.set_alpha(int(self.intro_animation.text_alpha))
            skip_rect = skip_text.get_rect(topright=(WINDOW_SIZE[0] - 20, 20))
            screen.blit(skip_text, skip_rect)
    
    def draw_login_screen(self):
        screen.fill(BACKGROUND)
        title_text = title_font.render("貪食蛇遊戲系統", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_SIZE[0]//2, 80))
        screen.blit(title_text, title_rect)
        username_label = normal_font.render("用戶名:", True, WHITE)
        screen.blit(username_label, (180, 208))
        password_label = normal_font.render("密碼:", True, WHITE)
        screen.blit(password_label, (180, 268))
    
        self.username_input.draw(screen)
        self.password_input.draw(screen)
        self.login_button.draw(screen)
        self.register_button.draw(screen)
        self.clear_button.draw(screen)
        self.leaderboard_button.draw(screen)
        
        
        feedback_surface = normal_font.render(self.feedback_message, True, self.feedback_color)
        feedback_rect = feedback_surface.get_rect(center=(WINDOW_SIZE[0]//2, 450))
        screen.blit(feedback_surface, feedback_rect)
        help_text = small_font.render("提示: 按Enter鍵快速登入 | 按TAB鍵查看排行榜", True, GRAY)
        screen.blit(help_text, (50, 520))
        
        self.leaderboard.draw(screen)
    
    def draw_game_screen(self):
        screen.fill(BACKGROUND)
        pygame.draw.rect(screen, WHITE, (0, 100, WINDOW_SIZE[0], WINDOW_SIZE[1]-100), 2)
        self.snake.draw(screen)
        self.food.draw(screen)
        user_text = normal_font.render(f"玩家: {self.current_user}", True, WHITE)
        screen.blit(user_text, (20, 20))
        score_text = normal_font.render(f"分數: {self.score}", True, WHITE)
        screen.blit(score_text, (20, 50))
        high_score_text = normal_font.render(f"最高分: {self.high_score}", True, WHITE)
        screen.blit(high_score_text, (200, 20))
        speed_text = normal_font.render(f"速度: {self.game_speed:.1f}", True, WHITE)
        screen.blit(speed_text, (200, 50))
        controls = small_font.render("方向鍵控制移動 | ESC鍵登出 | TAB鍵查看排行榜", True, GRAY)
        screen.blit(controls, (350, 35))
        
        self.leaderboard.draw(screen)
    
    def draw_game_over_screen(self):
        screen.fill(BACKGROUND)
        
        # 遊戲結束標題
        game_over_text = title_font.render("遊戲結束", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_SIZE[0]//2, 200))
        screen.blit(game_over_text, game_over_rect)
        final_score_text = normal_font.render(f"最終分數: {self.score}", True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WINDOW_SIZE[0]//2, 280))
        screen.blit(final_score_text, final_score_rect)
        high_score_text = normal_font.render(f"最高分數: {self.high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(WINDOW_SIZE[0]//2, 320))
        screen.blit(high_score_text, high_score_rect)
        
        if self.score == self.high_score and self.score > 0:
            new_record_text = normal_font.render("🎉 新紀錄！", True, YELLOW)
            new_record_rect = new_record_text.get_rect(center=(WINDOW_SIZE[0]//2, 360))
            screen.blit(new_record_text, new_record_rect)
        
        restart_text = normal_font.render("按空白鍵重新開始", True, GREEN)
        restart_rect = restart_text.get_rect(center=(WINDOW_SIZE[0]//2, 420))
        screen.blit(restart_text, restart_rect)
        
        logout_text = normal_font.render("按ESC鍵登出", True, BLUE)
        logout_rect = logout_text.get_rect(center=(WINDOW_SIZE[0]//2, 460))
        screen.blit(logout_text, logout_rect)
        
        leaderboard_hint = small_font.render("按TAB鍵查看排行榜", True, GRAY)
        leaderboard_rect = leaderboard_hint.get_rect(center=(WINDOW_SIZE[0]//2, 500))
        screen.blit(leaderboard_hint, leaderboard_rect)
        
        self.leaderboard.draw(screen)
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            dt = clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if self.state == GameState.INTRO:
                    self.handle_intro_events(event)
                elif self.state == GameState.LOGIN:
                    self.handle_login_events(event)
                elif self.state == GameState.GAME:
                    self.handle_game_events(event)
                elif self.state == GameState.GAME_OVER:
                    self.handle_game_over_events(event)
            
            # 更新
            if self.state == GameState.INTRO:
                self.intro_animation.update()
                if self.intro_animation.finished:
                    self.state = GameState.LOGIN
            elif self.state == GameState.LOGIN:
                self.username_input.update(dt)
                self.password_input.update(dt)
            elif self.state == GameState.GAME:
                self.update_game()

            if self.state == GameState.INTRO:
                self.draw_intro_screen()
            elif self.state == GameState.LOGIN:
                self.draw_login_screen()
            elif self.state == GameState.GAME:
                self.draw_game_screen()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over_screen()
            
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()