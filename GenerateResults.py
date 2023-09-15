# Author: Aakief Hassiem
# Description: Creates dummy input for an adaptive system

import random

'''
Function to find the category at which a certain learner ability is in 
'''
def findLevel(learnerAbility):
    if learnerAbility >= -4 and learnerAbility <= -1.6:
        level = "novice"
    elif learnerAbility >= -1.59999 and learnerAbility <= 1.59999:
        level = "mid"
    elif learnerAbility >= 1.6 and learnerAbility <= 4:
        level = "high"
    
    return level

# Update learner abilities according to triples
learnerAbilities = [0,0,0]
# Arrays for each key indicates question difficulty
# 1 -> Difficult question
# 0 -> Not difficult
# Adjust accordingly to the learner abilities 
concepts = {"Ajoblanco": [0,0,0,1,1], "BaconExplosion":[0,0,0,1,1], "Bhajji":[0,0,0,1,1]}

# Outcomes indicates whether the question is answered correctly
# 1 -> Correct
# 0 -> Incorrect 
outcomes = [0, 1] 

simulated_data = [] # Array to store the input

# Open a file in write mode ('w')
file_name = "SystemInput/sim.txt"

i = 0

for key in concepts:
    questionsArray = concepts[key] 
    
    level = findLevel(learnerAbilities[i])
    
    for question in questionsArray:
        # Assign probabilities of a correct and incorrect response based on learner level and question difficulty 
        if question == 0 and level == "novice": probabilities = [0.4, 0.6]
            
        elif question == 0 and level == "mid": probabilities = [0.3, 0.7]
            
        elif question == 0 and level == "high": probabilities = [0.1, 0.9]
            
        elif question == 1 and level == "novice": probabilities = [0.8, 0.2]
            
        elif question == 1 and level == "mid": probabilities = [0.6, 0.4]
            
        elif question == 1 and level == "high": probabilities = [0.4, 0.6]
    
        outcome = random.choices(outcomes, weights=probabilities, k=1)[0] # Make a choice

        # Construct response vector for the question
        if outcome == 1: answerArray = [key,True,True,question]
        elif outcome == 0: answerArray = [key,True,False,question]
        
        # Add the array to the dummy input
        simulated_data.append(answerArray)
    
    i += 1

# Write the input into a file
with open(file_name, 'w') as file:
    file.write(str(simulated_data))