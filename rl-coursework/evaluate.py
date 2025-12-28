"""Evaluation script for trained Q-Learning agent."""
import argparse
import numpy as np
from gridworld import GridWorld
from agent import QLearningAgent

def evaluate(model_path, episodes=100, render=False):
    """Evaluate trained agent."""
    env = GridWorld()
    agent = QLearningAgent(env.n_states, env.n_actions)
    agent.load(model_path)
    
    total_rewards = []
    successes = []
    
    for ep in range(episodes):
        state = env.reset()
        total_reward = 0
        
        for _ in range(100):
            if render:
                env.render()
            action = agent.choose_action(state, training=False)
            state, reward, done = env.step(action)
            total_reward += reward
            if done:
                break
        
        total_rewards.append(total_reward)
        successes.append(1 if done and reward == 10 else 0)
    
    print(f"\n=== Evaluation Results ({episodes} episodes) ===")
    print(f"Average Reward: {np.mean(total_rewards):.2f} ± {np.std(total_rewards):.2f}")
    print(f"Success Rate: {np.mean(successes)*100:.1f}%")
    print(f"Max Reward: {np.max(total_rewards):.2f}")
    print(f"Min Reward: {np.min(total_rewards):.2f}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='q_table.npy')
    parser.add_argument('--episodes', type=int, default=100)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    
    evaluate(args.model, args.episodes, args.render)
