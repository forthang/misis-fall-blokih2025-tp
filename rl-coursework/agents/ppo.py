"""Fixed PPO Agent."""
import numpy as np

class PPOAgent:
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99, clip_eps=0.2):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.lr = lr
        self.gamma = gamma
        self.clip_eps = clip_eps
        self.lam = 0.95
        
        h1, h2 = 128, 64
        
        # Policy
        self.w1 = np.random.randn(state_dim, h1) * np.sqrt(2/state_dim)
        self.b1 = np.zeros(h1)
        self.w2 = np.random.randn(h1, h2) * np.sqrt(2/h1)
        self.b2 = np.zeros(h2)
        self.w_mu = np.random.randn(h2, action_dim) * 0.01
        self.b_mu = np.zeros(action_dim)
        self.log_std = np.zeros(action_dim) - 0.5
        
        # Value
        self.vw1 = np.random.randn(state_dim, h1) * np.sqrt(2/state_dim)
        self.vb1 = np.zeros(h1)
        self.vw2 = np.random.randn(h1, h2) * np.sqrt(2/h1)
        self.vb2 = np.zeros(h2)
        self.vw3 = np.random.randn(h2, 1) * 0.01
        self.vb3 = np.zeros(1)
        
        self.clear_buffer()
        
    def clear_buffer(self):
        self.states = []
        self.actions = []
        self.rewards = []
        self.log_probs = []
        self.values = []
        self.dones = []
    
    def _tanh(self, x):
        return np.tanh(np.clip(x, -20, 20))
    
    def _policy_forward(self, s):
        h1 = self._tanh(s @ self.w1 + self.b1)
        h2 = self._tanh(h1 @ self.w2 + self.b2)
        mu = self._tanh(h2 @ self.w_mu + self.b_mu)
        std = np.exp(np.clip(self.log_std, -2, 0.5))
        return mu, std, h1, h2
    
    def _value_forward(self, s):
        h1 = self._tanh(s @ self.vw1 + self.vb1)
        h2 = self._tanh(h1 @ self.vw2 + self.vb2)
        return (h2 @ self.vw3 + self.vb3)[0], h1, h2
    
    def choose_action(self, state, training=True):
        mu, std, _, _ = self._policy_forward(state)
        if training:
            action = mu + np.random.randn(self.action_dim) * std
        else:
            action = mu
        action = np.clip(action, -1, 1)
        log_prob = -0.5 * np.sum(((action - mu) / (std + 1e-8))**2 + 2*np.log(std + 1e-8))
        return action, log_prob
    
    def get_value(self, state):
        v, _, _ = self._value_forward(state)
        return v
    
    def store(self, state, action, reward, log_prob, value, done):
        self.states.append(state.copy())
        self.actions.append(action.copy())
        self.rewards.append(reward)
        self.log_probs.append(log_prob)
        self.values.append(value)
        self.dones.append(done)
    
    def learn(self):
        if len(self.states) < 32:
            self.clear_buffer()
            return
        
        states = np.array(self.states)
        actions = np.array(self.actions)
        old_log_probs = np.array(self.log_probs)
        values = np.array(self.values)
        rewards = np.array(self.rewards)
        dones = np.array(self.dones)
        
        # GAE
        n = len(rewards)
        advantages = np.zeros(n)
        returns = np.zeros(n)
        gae = 0
        next_val = 0
        
        for t in reversed(range(n)):
            if dones[t]:
                next_val = 0
                gae = 0
            delta = rewards[t] + self.gamma * next_val - values[t]
            gae = delta + self.gamma * self.lam * gae
            advantages[t] = gae
            returns[t] = gae + values[t]
            next_val = values[t]
        
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        
        # Update
        for _ in range(3):
            idx = np.random.permutation(n)
            for i in idx:
                s, a, adv, ret = states[i], actions[i], advantages[i], returns[i]
                old_lp = old_log_probs[i]
                
                mu, std, h1, h2 = self._policy_forward(s)
                new_lp = -0.5 * np.sum(((a - mu) / (std + 1e-8))**2 + 2*np.log(std + 1e-8))
                
                ratio = np.exp(np.clip(new_lp - old_lp, -10, 10))
                surr1 = ratio * adv
                surr2 = np.clip(ratio, 1-self.clip_eps, 1+self.clip_eps) * adv
                
                # Policy gradient
                if surr1 <= surr2 and adv != 0:
                    grad = adv * (a - mu) / (std**2 + 1e-8)
                    lr = self.lr * 0.1
                    
                    self.w_mu += lr * np.outer(h2, grad)
                    self.b_mu += lr * grad
                    
                    dh2 = (1 - h2**2) * (self.w_mu @ grad)
                    self.w2 += lr * np.outer(h1, dh2)
                    self.b2 += lr * dh2
                    
                    dh1 = (1 - h1**2) * (self.w2 @ dh2)
                    self.w1 += lr * np.outer(s, dh1)
                    self.b1 += lr * dh1
                
                # Value update
                v, vh1, vh2 = self._value_forward(s)
                v_err = ret - v
                lr_v = self.lr
                
                self.vw3 += lr_v * vh2.reshape(-1, 1) * v_err
                self.vb3 += lr_v * v_err
                
                dvh2 = (1 - vh2**2) * (v_err * self.vw3.flatten())
                self.vw2 += lr_v * np.outer(vh1, dvh2)
                self.vb2 += lr_v * dvh2
                
                dvh1 = (1 - vh1**2) * (self.vw2 @ dvh2)
                self.vw1 += lr_v * np.outer(s, dvh1)
                self.vb1 += lr_v * dvh1
        
        self.clear_buffer()
    
    def save(self, path):
        np.savez(path, w1=self.w1, b1=self.b1, w2=self.w2, b2=self.b2,
                 w_mu=self.w_mu, b_mu=self.b_mu, log_std=self.log_std,
                 vw1=self.vw1, vb1=self.vb1, vw2=self.vw2, vb2=self.vb2,
                 vw3=self.vw3, vb3=self.vb3)
    
    def load(self, path):
        d = np.load(path)
        self.w1, self.b1 = d['w1'], d['b1']
        self.w2, self.b2 = d['w2'], d['b2']
        self.w_mu, self.b_mu = d['w_mu'], d['b_mu']
        self.log_std = d['log_std']
        self.vw1, self.vb1 = d['vw1'], d['vb1']
        self.vw2, self.vb2 = d['vw2'], d['vb2']
        self.vw3, self.vb3 = d['vw3'], d['vb3']
