"""Visualization for training metrics."""
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt

def plot_walker_metrics(path='logs/walker_metrics.json'):
    """Plot Walker training metrics."""
    try:
        with open(path) as f:
            m = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {path}")
        print("Train first: python train_walker.py")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle('Walker RL Training Metrics', fontsize=14, fontweight='bold')
    
    # Best distance per episode
    ax = axes[0, 0]
    best = np.array(m['best_dist']) / 100  # to meters
    ax.plot(best, alpha=0.4, color='blue')
    if len(best) > 10:
        smooth = np.convolve(best, np.ones(10)/10, mode='valid')
        ax.plot(range(9, len(best)), smooth, color='blue', linewidth=2, label='MA-10')
    ax.set_title('Best Distance per Episode')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Distance (m)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Average distance
    ax = axes[0, 1]
    avg = np.array(m['avg_dist']) / 100
    ax.plot(avg, alpha=0.4, color='green')
    if len(avg) > 10:
        smooth = np.convolve(avg, np.ones(10)/10, mode='valid')
        ax.plot(range(9, len(avg)), smooth, color='green', linewidth=2, label='MA-10')
    ax.set_title('Average Distance per Episode')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Distance (m)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Rewards
    ax = axes[1, 0]
    rewards = np.array(m['rewards'])
    ax.plot(rewards, alpha=0.4, color='orange')
    if len(rewards) > 10:
        smooth = np.convolve(rewards, np.ones(10)/10, mode='valid')
        ax.plot(range(9, len(rewards)), smooth, color='orange', linewidth=2, label='MA-10')
    ax.set_title('Average Reward per Episode')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Reward')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Ray speed (if available)
    ax = axes[1, 1]
    if 'ray_speeds' in m and m['ray_speeds']:
        ray = np.array(m['ray_speeds'])
        ax.plot(ray, color='red', linewidth=2)
        ax.set_title('Ray Speed per Episode')
        ax.set_xlabel('Episode')
        ax.set_ylabel('Speed')
        ax.grid(True, alpha=0.3)
    else:
        # Show cumulative best
        ax.plot(np.maximum.accumulate(best), color='purple', linewidth=2)
        ax.set_title('Record Distance Over Time')
        ax.set_xlabel('Episode')
        ax.set_ylabel('Record (m)')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('walker_metrics.png', dpi=150)
    print(f"Saved walker_metrics.png")
    print(f"Episodes: {len(best)}")
    print(f"Best distance: {max(best):.2f}m")
    print(f"Final avg (last 10): {np.mean(best[-10:]):.2f}m")
    plt.show()


def plot_gridworld_metrics(path='logs/gridworld_metrics.json'):
    """Plot GridWorld training metrics."""
    try:
        with open(path) as f:
            m = json.load(f)
    except FileNotFoundError:
        print(f"File not found: {path}")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle('GridWorld Q-Learning Metrics', fontsize=14, fontweight='bold')
    
    # Rewards
    ax = axes[0, 0]
    ax.plot(m['rewards'], alpha=0.3)
    if len(m['rewards']) > 20:
        smooth = np.convolve(m['rewards'], np.ones(20)/20, mode='valid')
        ax.plot(range(19, len(m['rewards'])), smooth, 'r-', linewidth=2)
    ax.set_title('Episode Reward')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Reward')
    ax.grid(True, alpha=0.3)
    
    # Episode length
    ax = axes[0, 1]
    ax.plot(m['lengths'], alpha=0.3)
    if len(m['lengths']) > 20:
        smooth = np.convolve(m['lengths'], np.ones(20)/20, mode='valid')
        ax.plot(range(19, len(m['lengths'])), smooth, 'r-', linewidth=2)
    ax.set_title('Episode Length')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Steps')
    ax.grid(True, alpha=0.3)
    
    # Success rate
    ax = axes[1, 0]
    window = 50
    if len(m['successes']) > window:
        success_ma = np.convolve(m['successes'], np.ones(window)/window, mode='valid')
        ax.plot(success_ma * 100, color='green', linewidth=2)
    ax.set_title(f'Success Rate (MA-{window})')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Success %')
    ax.set_ylim([0, 105])
    ax.grid(True, alpha=0.3)
    
    # Cumulative success
    ax = axes[1, 1]
    ax.plot(np.cumsum(m['successes']), color='purple', linewidth=2)
    ax.set_title('Cumulative Successes')
    ax.set_xlabel('Episode')
    ax.set_ylabel('Total')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('gridworld_metrics.png', dpi=150)
    print("Saved gridworld_metrics.png")
    plt.show()


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--type', choices=['walker', 'gridworld'], default='walker')
    p.add_argument('--path', default=None)
    args = p.parse_args()
    
    if args.type == 'walker':
        path = args.path or 'logs/walker_metrics.json'
        plot_walker_metrics(path)
    else:
        path = args.path or 'logs/gridworld_metrics.json'
        plot_gridworld_metrics(path)
