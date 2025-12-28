"""Demo trained walker model."""
import argparse
import numpy as np
import pygame
from environments.walker import Walker
from agents.ppo import PPOAgent

BG = (25, 25, 35)
GROUND = (50, 60, 50)
GRASS = (70, 100, 55)
TORSO = (70, 130, 180)
LEG = (90, 140, 190)
JOINT = (255, 200, 100)
HEAD = (100, 160, 210)
TEXT = (220, 220, 220)
GREEN = (100, 200, 100)

def demo(model_path, delay=15):
    """Run demo with trained model."""
    env = Walker()
    agent = PPOAgent(env.state_dim, env.action_dim)
    
    try:
        agent.load(model_path)
        print(f"✓ Loaded model: {model_path}")
    except FileNotFoundError:
        print(f"✗ Model not found: {model_path}")
        print("Train first: python train_walker.py")
        return
    
    pygame.init()
    w, h = 900, 500
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("🚶 Walker Demo - Trained Model")
    font = pygame.font.SysFont('monospace', 18)
    font_big = pygame.font.SysFont('monospace', 24, bold=True)
    
    running = True
    cam_x = 0
    
    while running:
        state = env.reset()
        cam_x = 0
        
        while not env.fallen and env.steps < 1000:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        running = False
                    elif e.key == pygame.K_r:
                        state = env.reset()
                        cam_x = 0
                    elif e.key in (pygame.K_PLUS, pygame.K_EQUALS):
                        delay = max(1, delay - 3)
                    elif e.key == pygame.K_MINUS:
                        delay = min(100, delay + 3)
            
            if not running:
                break
            
            # Use trained policy (no exploration)
            action, _ = agent.choose_action(state, training=False)
            state, _, done = env.step(action)
            
            # Render
            d = env.get_render_data()
            screen.fill(BG)
            
            # Camera
            target = d['x'] - w // 3
            cam_x += (target - cam_x) * 0.1
            ox = -cam_x
            
            # Ground
            gy = d['ground_y']
            pygame.draw.rect(screen, GROUND, (0, gy, w, h - gy))
            pygame.draw.line(screen, GRASS, (0, gy), (w, gy), 3)
            
            # Markers
            for i in range(-5, 100):
                mx = i * 100 + ox
                if 0 <= mx < w:
                    pygame.draw.line(screen, (55, 65, 55), (mx, gy), (mx, gy + 10), 2)
                    if i >= 0 and i % 2 == 0:
                        screen.blit(font.render(f"{i}m", True, (80, 100, 80)), (mx - 6, gy + 12))
            
            # Walker
            x = d['x'] + ox
            
            for side in ['l', 'r']:
                hip = (d[f'{side}_hip'][0] + ox, d[f'{side}_hip'][1])
                knee = (d[f'{side}_knee'][0] + ox, d[f'{side}_knee'][1])
                foot = (d[f'{side}_foot'][0] + ox, d[f'{side}_foot'][1])
                pygame.draw.line(screen, LEG, hip, knee, 11)
                pygame.draw.line(screen, LEG, knee, foot, 9)
                pygame.draw.circle(screen, JOINT, (int(knee[0]), int(knee[1])), 6)
                pygame.draw.circle(screen, (180, 140, 100), (int(foot[0]), int(foot[1])), 5)
            
            pygame.draw.line(screen, TORSO, (x, d['torso_top']), (x, d['hip_y']), 14)
            pygame.draw.circle(screen, JOINT, (int(x), int(d['hip_y'])), 8)
            pygame.draw.circle(screen, HEAD, (int(x), int(d['head_y'])), 13)
            pygame.draw.circle(screen, (255, 255, 255), (int(x + 4), int(d['head_y'] - 2)), 3)
            pygame.draw.circle(screen, (0, 0, 0), (int(x + 5), int(d['head_y'] - 2)), 1)
            
            # Info
            screen.blit(font_big.render("TRAINED WALKER DEMO", True, GREEN), (10, 10))
            dist = d['distance'] / 100
            screen.blit(font.render(f"Distance: {dist:.2f}m  Steps: {d['steps']}", True, TEXT), (10, 40))
            screen.blit(font.render("[R] Reset  [+/-] Speed  [Q] Quit", True, (100, 100, 110)), (10, h - 25))
            
            pygame.display.flip()
            pygame.time.wait(delay)
            
            if done:
                break
        
        # Show result
        d = env.get_render_data()
        txt = f"Distance: {d['distance']/100:.2f}m - Press R to restart"
        screen.blit(font_big.render(txt, True, GREEN if d['distance'] > 500 else TEXT), (w//2 - 180, h//2))
        pygame.display.flip()
        
        # Wait for restart
        waiting = True
        while waiting and running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        running = False
                        waiting = False
                    elif e.key == pygame.K_r:
                        waiting = False
    
    pygame.quit()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--model', default='models/walker_ppo.npz')
    p.add_argument('--delay', type=int, default=15)
    demo(**vars(p.parse_args()))
