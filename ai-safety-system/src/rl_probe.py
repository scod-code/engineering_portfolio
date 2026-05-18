import random
import numpy as np

ACTIONS = ["run_static", "run_sandbox", "run_network_probe",
           "run_fs_probe", "run_process_probe"]
# The actions represent the investigative actions and probes that are available to run
# Knowing when to use what is exactly what fine-tune it


def discretise_state(static_score: float, network_seen: bool,
                     canary_hit: bool) -> tuple:
    score_bin = 0 if static_score < 4 else (1 if static_score < 8 else 2)
    return (score_bin, int(network_seen), int(canary_hit))

def epsilon_greedy(Q: dict, state: tuple, epsilon: float) -> int:
    if random.random() < epsilon or state not in Q:
        return random.randint(0, len(ACTIONS) - 1)
    return int(np.argmax(Q[state]))

def q_update(Q: dict, state: tuple, action: int, reward: float,
             next_state: tuple, alpha: float = 0.1, gamma: float = 0.9):
    if state not in Q:
        Q[state] = [0.0] * len(ACTIONS)
    if next_state not in Q:
        Q[next_state] = [0.0] * len(ACTIONS)
    best_next = max(Q[next_state])
    Q[state][action] += alpha * (reward + gamma * best_next - Q[state][action])
    '''This is the Bellman equation implemented as an incremental update. To understand each term:
reward — the immediate reward received after taking action in state. Every probe costs -1 (wall-time penalty). A confident classification earns +10.

gamma * best_next — the discounted estimated value of the best possible action from the next state. With gamma=0.9, a reward of +10 in one step is worth 9.0 now, in two steps is worth 8.1, and so on. This discount prevents the agent from placing infinite value on distant future rewards.

reward + gamma * best_next — the TD target: what the Q-value should be, based on this experience.

alpha * (target - Q[state][action]) — the update step: move the current Q-value a fraction alpha=0.1 towards the target. A learning rate of 0.1 means the agent updates cautiously, averaging over many experiences rather than overwriting previous learning with a single new observation.

A worked example: the agent is in state (1, 0, 0) (MEDIUM static score, no runtime signals yet) and takes run_network_probe. No new network activity is found, so reward = −1 (probe cost). The next state is still (1, 0, 0). The best Q-value in that next state, say, is 2.0.
The TD target is 
−1 + 0.9 × 2.0 = 0.8. If the current Q-value for this pair was 1.5, it updates to 

1.5 + 0.1 × (0.8−1.5)=1.43 — slightly downgraded, because run_network_probe gave no new information here.'''

def train_rl_agent(episodes: int = 200, epsilon: float = 0.3) -> dict:
    """
    Simulated training — reward +10 for confident classification,
    -1 per probe fired (time cost).
    """
'''How it works in practice:

The agent looks at the current "situation" — how risky does the static scan look? Has any network activity been seen? Did the code touch a canary file?
Based on that, it picks one action: which probe to run next
If the code already looks clearly benign from static analysis alone → just confirm with run_static, done quickly
If something suspicious was spotted → escalate to run_network_probe to investigate that specific channel
If it's already looking critical and a canary was hit → go straight to full run_sandbox for ground truth'''
    
    Q = {}
    for ep in range(episodes):
        # Simulate a random starting state
        static_score = random.uniform(0, 20)
        network_seen = random.random() > 0.7
        canary_hit   = random.random() > 0.9
        state        = discretise_state(static_score, network_seen, canary_hit)
        total_reward = 0

        for step in range(len(ACTIONS)):
            action  = epsilon_greedy(Q, state, epsilon)
            # Simulate outcome: higher-index probes reveal more on risky states
            revealed = (action >= 2 and static_score > 8) or canary_hit
            reward   = 10.0 if revealed else -1.0
            # Transition: more probes shift state toward certainty
            network_seen = network_seen or (action == 2 and static_score > 4)
            next_state   = discretise_state(static_score, network_seen, canary_hit)
            q_update(Q, state, action, reward, next_state)
            state        = next_state
            total_reward += reward
            if revealed:
                break  # confident classification reached

        epsilon = max(0.05, epsilon * 0.995)  # decay

    return Q

def select_probe(Q: dict, static_score: float,
                 network_seen: bool, canary_hit: bool) -> str:
    state  = discretise_state(static_score, network_seen, canary_hit)
    action = epsilon_greedy(Q, state, epsilon=0.0)  # greedy at inference
    return ACTIONS[action]