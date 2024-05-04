def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    abs_steering = abs(params['steering_angle']) 
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    
    # Define markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Define rewards and penalties
    reward, max_reward = 0.0, 1.0
    steering_penalty = 0.8
    speed_reward = 0.5
    
    # Reward for staying close to the center line
    if distance_from_center <= marker_1:
        reward += max_reward
    elif distance_from_center <= marker_2:
        reward += max_reward * 0.5
    elif distance_from_center <= marker_3:
        reward += max_reward * 0.1
    else:
        reward += 1e-3  # likely crashed or close to off track
        
    # Penalize reward if the car is steering too much
    if abs_steering > 10:
        reward *= steering_penalty
    
    # Reward for staying on track and making progress
    if all_wheels_on_track and progress > 0:
        reward += max_reward * progress
    
    # Reward for maintaining a high speed
    reward += speed * speed_reward
    
    return float(reward)
