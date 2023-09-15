# Author: Aakief Hassiem
# Desicription: Adaptive system that uses IRT to calculate learners ability for concepts in a test

# Command to run program and write output to text file
# python3 AdaptiveSystem.py | tee outputAdaptiveSystem.txt

from pyirt import irt
import Ontology
import contextlib
import sys
import os
import time

learnerAbility_dict = None

'''
Function to hide output from imported modules
''' 
@contextlib.contextmanager
def suppress_output():
    # Redirect stdout and stderr to a dummy file
    dummy_file = open(os.devnull, 'w')
    original_stdout, original_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = dummy_file, dummy_file

    try:
        yield
    finally:
        # Restore the original stdout and stderr
        sys.stdout, sys.stderr = original_stdout, original_stderr
        dummy_file.close()

'''
Calculates the learner ability using pyirt module which does IRT calculations
Uses a 2 parameter IRT model
'''
def IRT_calc(items):
    
    src_fp = [] # list of tuples in the format of [(user_id, item_id, ans_boolean)]

    # populate src_fp
    for i in range(len(items)):
        temp_tuple = (1,i+1,items[i])
        src_fp.append(temp_tuple)

    # Block that supresses the output
    with suppress_output():

        # 2 parameter irt model
        item_param, user_param = irt(src_fp, theta_bnds = [-4,4], alpha_bnds=[0.1,3], beta_bnds = [-3,3])

    # return the learner ability

    learnerAbility = str(round(user_param[1], 3))
    return learnerAbility

'''
Function that performs irt calculations on each of the concepts in the test
Returns an array with the concept and the corresponding learner ability
'''
def IRT_unit(testResults):
    
    output = []

    for i in testResults:
        concept = i[0] # concept of question
        items = i[2:] # results to responses [1,0,1,0,...]
        difficulty_factor = i[1]
        learnerAbility = round(float(IRT_calc(items)) + difficulty_factor,3) # calculating learner ability
        output.append(concept + ": " + str(learnerAbility))

    return output

'''
Function to check if the answer is correct and groups answers per concept
Calculates difficulty factor for each concept
Returns a nested array
'''
def assessment_unit(outputAQG):

    testResults = []

    for i in range(len(outputAQG)):

            if i == 0 or outputAQG[i][0] != outputAQG[i-1][0]: 
                if i != 0:
                    if num_diff == 0:
                        difficultyFactor = 0
                    else:
                        # Calculate difficulty factor
                        difficultyFactor = round(num_correct/num_diff * 0.1,3)
                    tempArray.insert(1, difficultyFactor)
                    testResults.append(tempArray)
                num_correct = 0 
                num_diff = 0
                tempArray = []
                concept = outputAQG[i][0]
                tempArray.append(concept)

            if outputAQG[i][3] == 1:
                num_diff += 1
            # assessing
            if outputAQG[i][1] == outputAQG[i][2]:
                tempArray.append(1)
                if outputAQG[i][3] == 1:
                    num_correct += 1
            else:
                tempArray.append(0)
            if i == len(outputAQG)-1:
                if num_diff == 0:
                    difficultyFactor = 0
                else:
                    difficultyFactor = round(num_correct/num_diff * 0.1,3)
                tempArray.insert(1, difficultyFactor)
                testResults.append(tempArray)

    return testResults

'''
Obtain triples for each concept and write to a csv file
'''
def getTriples(outputAQG):

    print("\n" + " "*10 + "#" * 10 + " Triples " + "#"*10)  

    # Create a set to store the unique first items
    unique_concepts = set()

    # Iterate over the nested arrays and extract the first items
    for item in outputAQG:
        first_concept = item[0]
        unique_concepts.add(first_concept)

    # Convert the set back to a list
    unique_concepts = list(unique_concepts)

    filename = "SystemOutput/outputAdaptiveSystem.csv"  # Specify the filename or path
    # Open the file in write mode, which will delete the contents of the file or create a new empty file
    with open(filename, "w") as file:
        pass
    
    # Loop through the concepts and get the triples
    for concept in unique_concepts:
        Ontology.triples(concept, learnerAbility_dict,filename)
        print(" ")

'''
Function that runs the process of the Adaptive System
'''
def AdaptiveSystem(outputAQG):
    
    start_time = time.time() # start timer

    testResults = assessment_unit(outputAQG)
    learnerAbilities = IRT_unit(testResults)

    print("-"*10 + " RESULTS " + "-"*10)
    print("Learning ability {-4,4} of student for concepts: " + str(learnerAbilities))   

    # Initialise dictionary set all subjects/objects to -2
    global learnerAbility_dict
    if learnerAbility_dict is None:
        learnerAbility_dict = Ontology.initialise_learner_ability()

    # Update the dictionary by calling the method in UpdateOntology
    Ontology.updateDict(learnerAbilities)

    # Get triples for all the concepts
    getTriples(outputAQG)

    # Write learner abilities to a file
    Ontology.writeLearnerAbilitydict(learnerAbility_dict)

    end_time = time.time() # end timer
    execution_time = end_time - start_time

    print(f"Executed in {round(execution_time,3)}s")

def main():

    print("Adaptive System Running...")

    import ast

    command = input("Enter (T) TERMINATE to quit the system, else press enter filename to continue: ")

    while command.lower() != "t":
        try:
            # Read input from the file
            with open("SystemInput/"+command, "r") as file:
                input_str = file.read()

            # Use ast.literal_eval() to safely parse the input string into a list of lists
            try:
                outputAQG = ast.literal_eval(input_str)
            except (ValueError, SyntaxError):
                print("Error: Invalid input format.")
                outputAQG = None

            if outputAQG is not None:
                AdaptiveSystem(outputAQG)

            print("-"*20)
            command = input("Enter (T) TERMINATE to quit the system, else press enter filename to continue: ")
        
        except FileNotFoundError:
            print(f"Error: File '{command}' not found.")
            break

if __name__ == "__main__":
    main()