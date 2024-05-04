# Going from 13 to 9 sec in AWS DeepRacer re:Invent 2018 Track
## _AWS DeepRacer competition @Humber College 2024_

[![logo](https://d1.awsstatic.com/deepracer/DRL%20Logo%20web%20500px.2b6ea0add11b4cf83314b39d3d7d6ab63d7fdff9.png)](https://d1.awsstatic.com/deepracer/DRL%20Logo%20web%20500px.2b6ea0add11b4cf83314b39d3d7d6ab63d7fdff9.png)

## What is DeepRacer?
The AWS DeepRacer provides an engaging and rapid method for individuals to delve into machine learning programming. Its objective is to deploy reinforcement learning models for instructing a robotic car, to complete three laps on a designated track.

Diverging from conventional remote or programmable cars, participants can solely employ descriptive codes to "guide" the car toward making autonomous decisions, rather than directly issuing commands to manipulate its movements. Consequently, directives such as "move straight for 2 meters and then turn right" are non-existent in this context. Instead, instructions follow a structure of "if you move straight for 1 meters and then turn left, you receive a reward of 1 point."

Hence, the car, striving to amass the highest possible score, undergoes multiple random attempts to determine the sequence of actions that yield the greatest reward. This iterative process, known as training, embodies the essence of how machines acquire knowledge.

## Tech
- 1:18 4WD scale car
- Intel Atom processor
- Intel distribution of OpenVINO toolkit
- Front-facing camera (4 megapixels)
- System memory: 4GB RAM
- 802.11ac Wi-Fi
- Ubuntu 20.04 Focal Fossa
- ROS 2 Foxy Fitzroy

## Model Creation

DeepRacer requires a [model](https://docs.aws.amazon.com/deepracer/latest/developerguide/deepracer-get-started-training-model.html) to be created, trained and evaluated before it can be used on an actual car. To train a reinforcement learning model, you can use the AWS DeepRacer console. In the console, create a training job, choose a supported framework and an available algorithm, add a reward function, and configure training settings. You can also watch training proceed in a simulator.

After starting your training job, you can examine the training metrics of rewards and track completion per episode to ascertain the training job's performance of your model. On the AWS DeepRacer console, the metrics are displayed in the Reward graph, as shown in the following illustration

After your training job is complete, you should evaluate the trained model to assess its convergency behavior. The evaluation proceeds by completing a number of trials on a chosen track and having the agent move on the track according to likely actions inferred by the trained model. The performance metrics include a percentage of track completion and the time running on each track from start to finish or going off-track

### My models
All of theses models are trained for Time trail race on re:Invent 2018 track in counterclockwise direction.

#### model3
After some trial and error my first working model was model3. It used [PPO](https://huggingface.co/blog/deep-rl-ppo) algorithm. It used continuous action space.
This reward function is designed to guide an agent in a simulated track environment by providing rewards and penalties based on its behavior. It takes into account parameters like the distance from the center line, steering angle, progress, track adherence, and speed. The agent is rewarded for staying close to the center line, with higher rewards for closer distances. It's penalized for excessive steering and rewarded for making progress and staying on the track. Additionally, maintaining a high speed is incentivized. By balancing these factors, the function aims to encourage the agent to navigate the track effectively, avoiding collisions and completing laps efficiently.

![(model3/model3Eval.png)]

After Evaluation this model was completeing the 3 laps in 14 sec without going off tack
()



#### model4
This model is a good example is not setting the speed too high and it taught me more about [hyperparameters.](https://dev.to/aws-builders/fine-tuning-the-performance-of-the-model-4pjo)
It used modified reward function of model 3. As evident by the graph the model was not completing the track without going off track because speed was too high.

()

#### model5
Model 5 used modified reward function from model3 and thanks to model4, I set the speed more appropriately and finetuned the hyperparameters. As evident in the graphs, the model was completing the track without issue.

()

After Evaluation this model was completeing the 3 laps arround 11 sec without going off tack
()

#### model7
The new reward function is notably simpler and more streamlined compared to the old function. It emphasizes specific aspects of the agent's behavior, particularly focusing on track adherence and progress. This function rewards the agent for staying on the track and making progress towards the goal, as indicated by the progress parameter. It also encourages acceleration by providing rewards for increasing speed over time. While it still penalizes excessive steering, this penalty is straightforward and less nuanced compared to the previous function, which had varying levels of penalties based on the steering angle. Moreover, the new function incorporates an initialization step to track the previous speed of the agent, allowing for the determination of speed increases. Overall, the new reward function is designed for simplicity and clarity, prioritizing key aspects of agent behavior to guide it effectively along the track.

```sh
if (speed > self.prev_speed) and (self.prev_speed > 0):
                reward += 5
            self.prev_speed = speed  # update the previous speed
```

As clearly seen in this graph, the model is over converged.
()

It is evident in the evaluation that the model is over converged.
()


#### model8
This reward function is structured to guide the behavior of an agent navigating a track environment. Initially, a minimum value, represented by `zero_val = 0.003`, is defined. This value likely serves as a baseline reward or penalty threshold against which the agent's actions are evaluated.

Within the `reward_function` definition, the function extracts relevant parameters from the provided `params` dictionary. These parameters include the index of the closest waypoint (`wp`), the agent's current speed (`speed`), and a boolean indicating whether all of the agent's wheels are on the track (`all_wheels_on_track`).

()

The core logic of the function revolves around the agent's behavior relative to specific sections of the track. If the agent is determined to be on the track (`all_wheels_on_track` is true), the function further examines its position based on the closest waypoint index (`wp`). It checks if the waypoint index falls within predefined ranges (`23-42 or 79-86`), which likely correspond to critical sections of the track. In these sections, if the agent's speed exceeds or equals 2 units, it is rewarded with the `zero_val` minimum reward. This implies that maintaining a minimum speed threshold in these critical sections is crucial for optimizing performance.

However, if the agent is not within these specific sections of the track, the function returns the agent's current speed as the reward. This suggests that outside of these critical sections, the agent's reward is directly proportional to its speed. 

Lastly, the function handles off-track scenarios by providing a very small reward (`1e-3`). This serves as a penalty for leaving the track and encourages the agent to stay within the defined boundaries.

````
if wp in (list(range(23, 42))) or wp in (list(range(79, 87))):
    if speed >= 2:
        return zero_val
return speed
````

In summary, this reward function incentivizes the agent to maintain a minimum speed in critical sections of the track while also rewarding it proportionally to its speed elsewhere. It also penalizes off-track behavior to ensure the agent stays within the designated track boundaries.

##### It is also designed in discreet action space with min and max speed pre defined for each angle.

##### Also this model is not over converged.
()
()

After Evaluation this model was completeing the 3 laps 9 sec.

()


## Source
[https://docs.aws.amazon.com/deepracer](https://docs.aws.amazon.com/deepracer)
