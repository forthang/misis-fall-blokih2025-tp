"""Walker with adaptive death ray."""
import numpy as np
import math

class Walker:
    """Walker with ray that adapts to performance."""
    
    def __init__(self, ray_base_speed=0.5):
        self.ground_y = 400
        self.thigh_len = 50
        self.shin_len = 45
        self.torso_len = 60
        self.head_r = 12
        self.max_torque = 15
        
        # Faster ray
        self.ray_base_speed = ray_base_speed
        self.ray_start_delay = 20
        
        self.reset()
        
    def reset(self):
        self.x = 150
        
        # Start with slight forward lean
        self.hip_l = 0.3
        self.hip_r = -0.2
        self.knee_l = -0.3
        self.knee_r = -0.4
        
        self.hip_l_v = 0
        self.hip_r_v = 0
        self.knee_l_v = 0
        self.knee_r_v = 0
        self.vx = 0
        
        self.ray_x = -50
        self.ray_speed = self.ray_base_speed
        
        self.steps = 0
        self.start_x = self.x
        self.fallen = False
        self.caught_by_ray = False
        
        # Track leg alternation
        self.last_push_leg = None  # 'l' or 'r'
        self.alternation_count = 0
        
        return self._get_state()
    
    def set_ray_speed(self, speed):
        """Set ray speed for curriculum learning."""
        self.ray_base_speed = speed
        self.ray_speed = speed
    
    def _foot_pos(self, hip, knee):
        fx = math.sin(hip) * self.thigh_len + math.sin(hip + knee) * self.shin_len
        fy = math.cos(hip) * self.thigh_len + math.cos(hip + knee) * self.shin_len
        return fx, fy
    
    def _get_hip_y(self):
        _, ly = self._foot_pos(self.hip_l, self.knee_l)
        _, ry = self._foot_pos(self.hip_r, self.knee_r)
        return self.ground_y - max(ly, ry)
    
    def _get_state(self):
        ray_dist = max(0, (self.x - self.ray_x) / 150)
        return np.array([
            np.clip(self.vx / 5, -1, 1),
            self.hip_l / 1.5,
            self.hip_r / 1.5,
            self.knee_l / 2,
            self.knee_r / 2,
            np.clip(self.hip_l_v / 5, -1, 1),
            np.clip(self.hip_r_v / 5, -1, 1),
            np.clip(self.knee_l_v / 5, -1, 1),
            np.clip(self.knee_r_v / 5, -1, 1),
            np.clip(ray_dist, 0, 1),
        ], dtype=np.float32)
    
    @property
    def state_dim(self):
        return 10
    
    @property
    def action_dim(self):
        return 4
    
    def step(self, action):
        action = np.clip(action, -1, 1) * self.max_torque
        
        # Apply torques
        self.hip_l_v += action[0] * 0.08
        self.knee_l_v += action[1] * 0.08
        self.hip_r_v += action[2] * 0.08
        self.knee_r_v += action[3] * 0.08
        
        # Damping
        d = 0.85
        self.hip_l_v *= d
        self.hip_r_v *= d
        self.knee_l_v *= d
        self.knee_r_v *= d
        
        # Update angles
        self.hip_l += self.hip_l_v * 0.12
        self.hip_r += self.hip_r_v * 0.12
        self.knee_l += self.knee_l_v * 0.12
        self.knee_r += self.knee_r_v * 0.12
        
        # Clamp
        self.hip_l = np.clip(self.hip_l, -0.6, 1.2)
        self.hip_r = np.clip(self.hip_r, -0.6, 1.2)
        self.knee_l = np.clip(self.knee_l, -1.5, 0.05)
        self.knee_r = np.clip(self.knee_r, -1.5, 0.05)
        
        # Ground contact
        hip_y = self._get_hip_y()
        lx, ly = self._foot_pos(self.hip_l, self.knee_l)
        rx, ry = self._foot_pos(self.hip_r, self.knee_r)
        
        l_ground = (hip_y + ly) >= self.ground_y - 3
        r_ground = (hip_y + ry) >= self.ground_y - 3
        
        # Movement - reward alternating legs
        old_x = self.x
        push_force = 0.5
        pushed_leg = None
        
        if l_ground and self.hip_l_v < -0.1 and self.hip_l > 0:
            self.vx += push_force
            pushed_leg = 'l'
        if r_ground and self.hip_r_v < -0.1 and self.hip_r > 0:
            self.vx += push_force
            pushed_leg = 'r'
        
        # Track alternation
        if pushed_leg and pushed_leg != self.last_push_leg:
            self.alternation_count += 1
            self.last_push_leg = pushed_leg
        
        self.vx *= 0.88
        self.x += self.vx
        
        # Ray movement - always accelerating
        if self.steps > self.ray_start_delay:
            self.ray_x += self.ray_speed
            self.ray_speed += 0.008  # Constant acceleration
        
        self.steps += 1
        
        # Death conditions
        head_y = hip_y - self.torso_len - self.head_r
        self.fallen = head_y > self.ground_y - 40
        self.caught_by_ray = self.ray_x >= (self.x - 25)
        
        reward = self._reward(self.x - old_x)
        done = self.fallen or self.caught_by_ray or self.steps >= 800
        
        return self._get_state(), reward, done
    
    def _reward(self, dx):
        r = 0
        
        # Forward movement
        r += dx * 4
        
        # Velocity bonus
        r += max(0, self.vx) * 1.5
        
        # BIG bonus for alternating legs (real walking)
        if self.alternation_count > 0:
            r += 0.8  # Reward each step
        
        # Bonus for leg separation (not both legs together)
        leg_diff = abs(self.hip_l - self.hip_r)
        if leg_diff > 0.3:
            r += 0.5
        
        # Penalty for not moving
        if dx < 0.1:
            r -= 0.3
        
        # Penalty for crouching
        hip_y = self._get_hip_y()
        if hip_y > self.ground_y - 70:
            r -= 0.8
        
        # Penalty for legs too close (sliding)
        if leg_diff < 0.15:
            r -= 0.4
        
        # Ray distance
        ray_dist = self.x - self.ray_x
        if ray_dist < 50:
            r -= 0.3
        
        # Death
        if self.fallen:
            r -= 15
        if self.caught_by_ray:
            r -= 25
        
        return r
    
    def get_render_data(self):
        hip_y = self._get_hip_y()
        torso_top = hip_y - self.torso_len
        head_y = torso_top - self.head_r
        
        lx, ly = self._foot_pos(self.hip_l, self.knee_l)
        lk_x = self.x - 10 + math.sin(self.hip_l) * self.thigh_len
        lk_y = hip_y + math.cos(self.hip_l) * self.thigh_len
        
        rx, ry = self._foot_pos(self.hip_r, self.knee_r)
        rk_x = self.x + 10 + math.sin(self.hip_r) * self.thigh_len
        rk_y = hip_y + math.cos(self.hip_r) * self.thigh_len
        
        return {
            'x': self.x,
            'hip_y': hip_y,
            'torso_top': torso_top,
            'head_y': head_y,
            'l_hip': (self.x - 10, hip_y),
            'l_knee': (lk_x, min(lk_y, self.ground_y)),
            'l_foot': (self.x - 10 + lx, min(hip_y + ly, self.ground_y)),
            'r_hip': (self.x + 10, hip_y),
            'r_knee': (rk_x, min(rk_y, self.ground_y)),
            'r_foot': (self.x + 10 + rx, min(hip_y + ry, self.ground_y)),
            'ground_y': self.ground_y,
            'ray_x': self.ray_x,
            'fallen': self.fallen,
            'caught': self.caught_by_ray,
            'distance': self.x - self.start_x,
            'steps': self.steps
        }
