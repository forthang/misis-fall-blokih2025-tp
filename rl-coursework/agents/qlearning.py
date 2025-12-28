"""Q-Learning Agent implementation."""
import numpy as np

class QLearningAgent:
    """Tabular Q-Learning agent with epsilon-greedy exploration."""
    
    def __init__(self, n_states, n_actions, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.n_states = n_states
        self.n_actions = n_actions
        self.alpha = alpha      # learning rate
        self.gamma = gamma      # discount factor
        self.epsilon = epsilon  # exploration rate
        self.q_table = np.zeros((n_states, n_actions))
        
    def choose_action(self, state, training=True):
        """Select action using epsilon-greedy policy."""
        if training and np.random.random() < self.epsilon:
            return np.random.randint(self.n_actions)
        return np.argmax(self.q_table[state])
    
    def learn(self, state, action, reward, next_state, done):
        """Update Q-table using Q-learning update rule."""
        current_q = self.q_table[state, action]
        next_max_q = 0 if done else np.max(self.q_table[next_state])
        target = reward + self.gamma * next_max_q
        self.q_table[state, action] += self.alpha * (target - current_q)
        
    def save(self, path):
        """Save Q-table to file."""
        np.save(path, self.q_table)
        
    def load(self, path):
        """Load Q-table from file."""
        self.q_table = np.load(path)
