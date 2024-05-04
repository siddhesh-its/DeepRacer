class Reward:
    def __init__(self, verbose=False, track_time=False):
        self.prev_speed = 0
        
    def reward_fun(self, params):
        
        
        track_width = params['track_width']
        distance_from_center = params['distance_from_center']
        abs_steering = abs(params['steering_angle'])
        all_wheels_on_track = params['all_wheels_on_track']
        progress = params['progress']
        speed = params['speed']
        
        reward = 0
        
        if all_wheels_on_track and progress > 0:
        
            marker_3 = 0.3 * track_width
            if distance_from_center <= marker_3:
                reward = 1
            else:
                reward = 0.3  # likely crashed/ close to off track
            
            ABS_STEERING_THRESHOLD = 25
            if abs_steering > ABS_STEERING_THRESHOLD:
                reward *= 0.8
        
            if (speed > self.prev_speed) and (self.prev_speed > 0):
                reward += 5
            self.prev_speed = speed  # update the previous speed
            
            return reward  # return the calculated reward
        
        else:
            return 1e-3

reward_obj = Reward()

def reward_function(params):
    reward = reward_obj.reward_fun(params)
    return float(reward)
