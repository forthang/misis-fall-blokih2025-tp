"""Training with curriculum learning - ray speeds up as agent improves."""
import argparse
import json
import numpy as np
import pygame
from environments.walker import Walker
from agents.ppo import PPOAgent

# Colors
BG = (25, 25, 35)
GROUND = (50, 60, 50)
GRASS = (70, 100, 55)
TORSO = (70, 130, 180)
LEG = (90, 140, 190)
JOINT = (255, 200, 100)
HEAD = (100, 160, 210)
TEXT = (220, 220, 220)
GREEN = (100, 200, 100)
RED = (200, 80, 80)
YELLOW = (255, 220, 100)

NUM_WALKERS = 6

class Visualizer:
    def __init__(self, w=1000, h=500):
        pygame.init()
        self.w, self.h = w, h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption("🚶 Walker RL - Curriculum Learning")
        self.font = pygame.font.SysFont('monospace', 16)
        self.font_big = pygame.font.SysFont('monospace', 22, bold=True)
        self.cam_x = 0
        
    def draw(self, walkers, best_idx, ep, metrics, ray_speed, paused=False):
        self.screen.fill(BG)
        
        best = walkers[best_idx]
        target = best['x'] - self.w // 3
        self.cam_x += (target - self.cam_x) * 0.1
        ox = -self.cam_x
        
        gy = best['ground_y']
        
        # Death ray
        ray_x = best['ray_x'] + ox
        if ray_x > -100:
            for i in range(4):
                alpha = 80 - i * 18
                glow_w = 25 + i * 12
                s = pygame.Surface((glow_w, self.h), pygame.SRCALPHA)
                s.fill((255, 50, 50, alpha))
                self.screen.blit(s, (ray_x - glow_w, 0))
            pygame.draw.rect(self.screen, (255, 60, 60), (ray_x - 8, 0, 12, self.h))
            pygame.draw.rect(self.screen, (255, 200, 200), (ray_x - 2, 0, 4, self.h))
        
        # Ground
        pygame.draw.rect(self.screen, GROUND, (0, gy, self.w, self.h - gy))
        pygame.draw.line(self.screen, GRASS, (0, gy), (self.w, gy), 3)
        
        # Markers
        for i in range(-5, 60):
            mx = i * 100 + ox
            if 0 <= mx < self.w:
                pygame.draw.line(self.screen, (55, 65, 55), (mx, gy), (mx, gy + 10), 2)
                if i >= 0 and i % 2 == 0:
                    self.screen.blit(self.font.render(f"{i}m", True, (80, 100, 80)), (mx - 6, gy + 12))
        
        # Walkers
        for i, d in enumerate(walkers):
            if i != best_idx and not d['fallen'] and not d['caught']:
                self._draw_walker(d, ox, ghost=True)
        self._draw_walker(best, ox, ghost=False)
        
        self._draw_info(ep, walkers, best_idx, metrics, ray_speed, paused)
        pygame.display.flip()
    
    def _draw_walker(self, d, ox, ghost=False):
        x = d['x'] + ox
        
        leg_color = (60, 90, 120) if ghost else LEG
        torso_color = (50, 80, 120) if ghost else TORSO
        head_color = (60, 100, 140) if ghost else HEAD
        joint_color = (160, 140, 80) if ghost else JOINT
        
        if d['caught']:
            head_color = (255, 80, 80)
            torso_color = (200, 60, 60)
        
        for side in ['l', 'r']:
            hip = (d[f'{side}_hip'][0] + ox, d[f'{side}_hip'][1])
            knee = (d[f'{side}_knee'][0] + ox, d[f'{side}_knee'][1])
            foot = (d[f'{side}_foot'][0] + ox, d[f'{side}_foot'][1])
            
            w = 7 if ghost else 11
            pygame.draw.line(self.screen, leg_color, hip, knee, w)
            pygame.draw.line(self.screen, leg_color, knee, foot, w - 2)
            if not ghost:
                pygame.draw.circle(self.screen, joint_color, (int(knee[0]), int(knee[1])), 6)
                pygame.draw.circle(self.screen, (180, 140, 100), (int(foot[0]), int(foot[1])), 5)
        
        w = 9 if ghost else 14
        pygame.draw.line(self.screen, torso_color, (x, d['torso_top']), (x, d['hip_y']), w)
        if not ghost:
            pygame.draw.circle(self.screen, joint_color, (int(x), int(d['hip_y'])), 8)
        
        r = 9 if ghost else 13
        pygame.draw.circle(self.screen, head_color, (int(x), int(d['head_y'])), r)
        if not ghost and not d['caught']:
            pygame.draw.circle(self.screen, (255, 255, 255), (int(x + 4), int(d['head_y'] - 2)), 3)
            pygame.draw.circle(self.screen, (0, 0, 0), (int(x + 5), int(d['head_y'] - 2)), 1)
    
    def _draw_info(self, ep, walkers, best_idx, metrics, ray_speed, paused):
        title = "CURRICULUM LEARNING" + (" [PAUSED]" if paused else "")
        self.screen.blit(self.font_big.render(title, True, TEXT), (10, 8))
        
        alive = sum(1 for w in walkers if not w['fallen'] and not w['caught'])
        best_d = walkers[best_idx]['distance'] / 100
        record = max(metrics['best_dist']) / 100 if metrics['best_dist'] else 0
        avg = np.mean(metrics['best_dist'][-20:]) / 100 if len(metrics['best_dist']) > 0 else 0
        
        lines = [
            f"Ep: {ep}  Alive: {alive}/{NUM_WALKERS}  Ray: {ray_speed:.2f}",
            f"Dist: {best_d:.1f}m  Avg20: {avg:.1f}m  Record: {record:.1f}m",
        ]
        for i, line in enumerate(lines):
            self.screen.blit(self.font.render(line, True, TEXT), (10, 35 + i * 20))
        
        # Ray warning
        best = walkers[best_idx]
        ray_dist = best['x'] - best['ray_x']
        if 0 < ray_dist < 80 and not best['caught']:
            self.screen.blit(self.font_big.render("⚠ RAY CLOSE!", True, RED), (self.w // 2 - 60, 8))
        
        # Level indicator
        level = int(ray_speed * 10)
        level_txt = f"Level {level}"
        color = GREEN if level < 10 else YELLOW if level < 15 else RED
        self.screen.blit(self.font_big.render(level_txt, True, color), (self.w - 100, 8))
        
        ctrl = "[SPACE] Pause  [+/-] Speed  [S] Save  [Q] Quit"
        self.screen.blit(self.font.render(ctrl, True, (100, 100, 110)), (10, self.h - 22))


def train(episodes=300, delay=5):
    # Fast ray, no adaptation
    ray_speed = 1.0
    
    envs = [Walker(ray_base_speed=ray_speed) for _ in range(NUM_WALKERS)]
    agent = PPOAgent(envs[0].state_dim, envs[0].action_dim, lr=5e-4)
    viz = Visualizer()
    
    metrics = {'rewards': [], 'best_dist': [], 'avg_dist': [], 'ray_speeds': []}
    running = True
    paused = False
    
    for ep in range(episodes):
        if not running:
            break
        
        # Ray gets faster each episode
        ray_speed = 1.0 + ep * 0.01
        for env in envs:
            env.set_ray_speed(ray_speed)
        
        states = [e.reset() for e in envs]
        total_rewards = [0] * NUM_WALKERS
        viz.cam_x = 0
        
        while any(not e.fallen and not e.caught_by_ray and e.steps < 800 for e in envs):
            if not running:
                break
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        paused = not paused
                    elif event.key == pygame.K_s:
                        save_model(agent, metrics)
                    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                        delay = max(1, delay - 1)
                    elif event.key == pygame.K_MINUS:
                        delay = min(30, delay + 1)
            
            if paused:
                render_data = [e.get_render_data() for e in envs]
                best_idx = max(range(NUM_WALKERS), key=lambda i: envs[i].x)
                viz.draw(render_data, best_idx, ep + 1, metrics, ray_speed, True)
                pygame.time.wait(50)
                continue
            
            for i, (env, state) in enumerate(zip(envs, states)):
                if env.fallen or env.caught_by_ray or env.steps >= 800:
                    continue
                
                action, log_p = agent.choose_action(state)
                val = agent.get_value(state)
                next_state, reward, done = env.step(action)
                agent.store(state, action, reward, log_p, val, done)
                
                states[i] = next_state
                total_rewards[i] += reward
            
            render_data = [e.get_render_data() for e in envs]
            best_idx = max(range(NUM_WALKERS), 
                          key=lambda i: envs[i].x if not envs[i].fallen and not envs[i].caught_by_ray else -1000)
            viz.draw(render_data, best_idx, ep + 1, metrics, ray_speed)
            pygame.time.wait(delay)
        
        agent.learn()
        
        distances = [e.x - e.start_x for e in envs]
        metrics['rewards'].append(sum(total_rewards) / NUM_WALKERS)
        metrics['best_dist'].append(max(distances))
        metrics['avg_dist'].append(sum(distances) / NUM_WALKERS)
        metrics['ray_speeds'].append(ray_speed)
        
        best_d = max(distances) / 100
        avg_d = sum(distances) / NUM_WALKERS / 100
        color = GREEN if best_d > 4 else YELLOW if best_d > 2 else RED
        txt = f"Ep {ep+1}: Best {best_d:.1f}m  Avg {avg_d:.1f}m"
        t = viz.font_big.render(txt, True, color)
        viz.screen.blit(t, (viz.w // 2 - 110, viz.h // 2))
        pygame.display.flip()
        pygame.time.wait(60)
        
        if (ep + 1) % 5 == 0:
            record = max(metrics['best_dist']) / 100
            print(f"Ep {ep+1}: Best={best_d:.1f}m, Avg={avg_d:.1f}m, Record={record:.1f}m, Ray={ray_speed:.2f}")
    
    save_model(agent, metrics)
    pygame.quit()


def save_model(agent, metrics):
    agent.save('models/walker_ppo.npz')
    with open('logs/walker_metrics.json', 'w') as f:
        json.dump(metrics, f)
    record = max(metrics['best_dist']) / 100 if metrics['best_dist'] else 0
    print(f"✓ Saved! Record: {record:.1f}m")


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--episodes', type=int, default=300)
    p.add_argument('--delay', type=int, default=5)
    train(**vars(p.parse_args()))
