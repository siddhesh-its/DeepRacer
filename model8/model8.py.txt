zero_val = 0.003

def reward_function(params): 
    wp = params['closest_waypoints'][1]
    speed = params['speed'] 
    all_wheels_on_track = params['all_wheels_on_track']
    
    if all_wheels_on_track:
    
        if wp in (list(range(23, 42))) or wp in (list(range(79, 87))):
            if speed >= 2:
                return zero_val
                
        return speed
        
    else:
            return 1e-3
    
