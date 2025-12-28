"""Visual training with real-time pygame display."""
import argparse
import json
import numpy as np
import pygame
from environments.gridworld import GridWorld
from agents.qlearning import QLearningAgent

# Colors
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GREEN = (50, 205, 50)
RED = (220, 60, 60)
BLUE = (70, 130, 180)
GRAY = (60, 60, 60)
YELLOW = (255, 215, 0)

CELL_SIZE = 100
INFO_HEIGHT = 150

class VisualTrainer:
    def __init__(self, env, agent, episodes, delay=50):
        self.env = env
        self.agent = agent
        self.episodes = episodes
        self.delay = delay
        
        pygame.init()
        self.width = env.size * CELL_SIZE
        self.height = env.size * CELL_SIZE + INFO_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Q-Learning GridWorld Training")
        self.font = pygame.font.SysFont('monospace', 20)
        self.font_big = pygame.font.SysFont('monospace', 28, bold=True)
        self.clock = pygame.time.Clock()
        
        self.metrics = {'rewards': [], 'lengths': [], 'successes': []}
        self.running = True
        
    def draw_grid(self, state_idx):
        """Draw the grid world."""
        self.screen.fill(BLACK)
        state = self.env._idx_to_state(state_idx)
        
        for i in range(self.env.size):
            for j in range(self.env.size):
                x, y = j * CELL_SIZE, i * CELL_SIZE
                rect = pygame.Rect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
                
                if (i, j) == state:
                    pygame.draw.rect(self.screen, BLUE, rect, border_radius=10)
                    pygame.draw.circle(self.screen, WHITE, (x + CELL_SIZE//2, y + CELL_SIZE//2), 30)
                elif (i, j) == self.env.goal:
                    pygame.draw.rect(self.screen, GREEN, rect, border_radius=10)
                    txt = self.font_big.render("GOAL", True, WHITE)
                    self.screen.blit(txt, (x + 15, y + 35))
                elif (i, j) in self.env.obstacles:
                    pygame.draw.rect(self.screen, RED, rect, border_radius=10)
                    txt = self.font_big.render("X", True, WHITE)
                    self.screen.blit(txt, (x + 40, y + 35))
                else:
                    pygame.draw.rect(self.screen, GRAY, rect, border_radius=10)
                    q_idx = i * self.env.size + j
                    max_q = np.max(self.agent.q_table[q_idx])
                    if max_q != 0:
                        txt = self.font.render(f"{max_q:.1f}", True, YELLOW)
                        self.screen.blit(txt, (x + 30, y + 40))
    
    def draw_info(self, episode, step, reward, total_reward):
        """Draw training info panel."""
        y = self.env.size * CELL_SIZE + 10
        
        success_rate = np.mean(self.metrics['successes'][-100:]) * 100 if self.metrics['successes'] else 0
        avg_reward = np.mean(self.metrics['rewards'][-100:]) if self.metrics['rewards'] else 0
        
        texts = [
            f"Episode: {episode}/{self.episodes}  Step: {step}",
            f"Reward: {reward:+.1f}  Total: {total_reward:.1f}",
            f"Success Rate: {success_rate:.1f}%  Avg Reward: {avg_reward:.1f}",
            f"[SPACE] Pause  [+/-] Speed  [Q] Quit"
        ]
        
        for i, text in enumerate(texts):
            color = WHITE if i < 3 else (150, 150, 150)
            txt = self.font.render(text, True, color)
            self.screen.blit(txt, (10, y + i * 30))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.pause()
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    self.delay = max(10, self.delay - 20)
                elif event.key == pygame.K_MINUS:
                    self.delay = min(500, self.delay + 20)
    
    def pause(self):
        paused = True
        while paused and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    paused = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = False
                    elif event.key == pygame.K_q:
                        self.running = False
                        paused = False
    
    def train(self):
        for ep in range(self.episodes):
            if not self.running:
                break
                
            state = self.env.reset()
            total_reward = 0
            steps = 0
            
            for step in range(100):
                if not self.running:
                    break
                    
                self.handle_events()
                
                action = self.agent.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.agent.learn(state, action, reward, next_state, done)
                
                state = next_state
                total_reward += reward
                steps += 1
                
                self.draw_grid(state)
                self.draw_info(ep + 1, steps, reward, total_reward)
                pygame.display.flip()
                pygame.time.wait(self.delay)
                
                if done:
                    pygame.time.wait(300)
                    break
            
            self.metrics['rewards'].append(total_reward)
            self.metrics['lengths'].append(steps)
            self.metrics['successes'].append(1 if done and reward == 10 else 0)
        
        self.save_results()
        pygame.quit()
    
    def save_results(self):
        self.agent.save('models/gridworld_q.npy')
        with open('logs/gridworld_metrics.json', 'w') as f:
            json.dump(self.metrics, f)
        print("Saved models/gridworld_q.npy and logs/gridworld_metrics.json")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--episodes', type=int, default=500)
    parser.add_argument('--alpha', type=float, default=0.1)
    parser.add_argument('--gamma', type=float, default=0.99)
    parser.add_argument('--epsilon', type=float, default=0.1)
    parser.add_argument('--delay', type=int, default=50)
    args = parser.parse_args()
    
    env = GridWorld()
    agent = QLearningAgent(env.n_states, env.n_actions, args.alpha, args.gamma, args.epsilon)
    
    trainer = VisualTrainer(env, agent, args.episodes, args.delay)
    trainer.train()

if __name__ == '__main__':
    main()
