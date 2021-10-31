'''
Dad asked about probability of streaks
Simulating streaks per discussion in:
https://math.stackexchange.com/questions/383704/probability-of-streaks
For solitaire we just want streaks of wins
For coin flips streaks of heads or tails are fine
'''

import numpy as np
import itertools

# p is prob of winning a game
p = 0.86 
# n is number of games per trial
n = 200 
# w is desired streak length
w = 48
# k is number of trials to perform
k = 1000000

def generate_trial(n, p):
    trial = np.random.uniform(0, 1, (1, 1, n))[0][0]
    trial[trial < p] = 1
    trial[trial < 1] = 0
    return trial

def streak_of_wins(trial, w):
    '''
    Stole this code from https://stackoverflow.com/questions/53155345/count-longest-streak-of-0-in-a-python-list-python
    and modified to return after w is hit
    Returns True if there is a streak of length w
    '''
    maxvalue=0
    for game, group in itertools.groupby(trial):
        if game: #check if we won the game
            maxvalue = max(maxvalue,sum(group))
            if maxvalue >= w:
                return True
    return False
    
def streak_of_losses(trial, w):
    '''
    Stole this code from https://stackoverflow.com/questions/53155345/count-longest-streak-of-0-in-a-python-list-python
    and modified to return a streak of w losses
    Only relevant if you are trying to do this for streaks of wins OR losses
    '''
    maxvalue=0
    for game, group in itertools.groupby(trial):
        if not game: #check if we lost the game
            maxvalue = max(maxvalue, len(list(group)))
            if maxvalue >= w:
                return True
    return False

def perform_trial(n, p, w, include_losses = False):
    '''
    Returns True if you hit streak length w in n games
    False otherwise
    You can consider streaks of losses if you want by returning
    streak_of_wins OR streak_of_losses instead
    '''
    trial = generate_trial(n,p)
    if include_losses:
        return streak_of_wins(trial, w) or streak_of_losses(trial, w)
    else:
        return streak_of_wins(trial, w)

def perform_k_trials(k, n, p, w, include_losses = False):
    '''
    Out of k trials, what percentage had a streak of length w?
    '''
    count = 0
    for i in range(k):
        if perform_trial(n, p, w, include_losses):
            count += 1
    return float(count) / k

#print(perform_k_trials(k, n, p, w))
print(perform_k_trials(10000, 100, 0.5, 10, True))
print(perform_k_trials(10000, 100, 0.5, 10, False))