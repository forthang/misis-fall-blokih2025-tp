"""GridWorld Environment for Reinforcement Learning."""
import numpy as np

class GridWorld:
    """Simple grid environment for RL experiments."""
    
    ACTIONS = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}  # up, down, left, right
    ACTION_NAMES = ['↑', '↓', '←', '→']
    
    def __init__(self, size=5, obstacles=None, goal=None):
        self.size = size
        self.obstacles = obstacles or [(1, 1), (2, 2), (3, 1)]
        self.goal = goal or (size - 1, size - 1)
        self.start = (0, 0)
        self.state = self.start
        
    def reset(self):
        """Reset environment to initial state."""
        self.state = self.start
        return self._state_to_idx(self.state)
    
    def step(self, action):
        """Execute action and return (next_state, reward, done)."""
        dy, dx = self.ACTIONS[action]
        new_pos = (self.state[0] + dy, self.state[1] + dx)
        
        # Check boundaries
        if not (0 <= new_pos[0] < self.size and 0 <= new_pos[1] < self.size):
            return self._state_to_idx(self.state), -1, False
        
        # Check obstacles
        if new_pos in self.obstacles:
            return self._state_to_idx(self.state), -5, False
        
        self.state = new_pos
        
        # Check goal
        if self.state == self.goal:
            return self._state_to_idx(self.state), 10, True
        
        return self._state_to_idx(self.state), -0.1, False
    
    def _state_to_idx(self, state):
        """Convert (row, col) to single index."""
        return state[0] * self.size + state[1]
    
    def _idx_to_state(self, idx):
        """Convert index to (row, col)."""
        return (idx // self.size, idx % self.size)
    
    @property
    def n_states(self):
        return self.size * self.size
    
    @property
    def n_actions(self):
        return 4
    
    def render(self):
        """Print current grid state."""
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                if (i, j) == self.state:
                    row += "A "
                elif (i, j) == self.goal:
                    row += "G "
                elif (i, j) in self.obstacles:
                    row += "X "
                else:
                    row += ". "
            print(row)
        print()
