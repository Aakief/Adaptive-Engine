# Author: Aakief Hassiem
# Desicription: Adaptive system that uses IRT to calculate learners ability and updates a knowledge graph weights

# Command to run program and write output to text file
# python3 AdaptiveSystem.py | tee outputAdaptiveSystem.txt

from pyirt import irt
import Ontology
import contextlib
import sys
import os
import time

learnerAbility_ontology = None

# Function to hide output from imported modules  
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

# Calculates the learner ability using pyirt module which does IRT calculations
def IRT_calc(items):
    
    src_fp = [] # list of tuples in the format of [(user_id, item_id, ans_boolean)]

    # populate src_fp
    for i in range(len(items)):
        temp_tuple = (1,i+1,items[i])
        src_fp.append(temp_tuple)

    # Block that supresses the output
    with suppress_output():

        # 2 parameter irt model
        item_param, user_param = irt(src_fp, theta_bnds = [-2,2], alpha_bnds=[0.1,3], beta_bnds = [-3,3])

    # return the learner ability
    #print(item_param)
    learnerAbility = str(round(user_param[1], 3))
    return learnerAbility

# Function that performs irt calculations on each of the concepts
def IRT_unit(testResults):
    
    output = []

    for i in testResults:
        concept = i[0] # concept of question
        items = i[1:] # results to responses [1,0,1,0,..]
        learnerAbility = IRT_calc(items)  # calculating learner ability
        output.append(concept + ": " + learnerAbility)

    return output

# Function to check if the answer is correct and groups answers per concept
def assessment_unit(outputAQG):

    testResults = []

    for i in range(len(outputAQG)):

        if i == 0 or outputAQG[i][0] != outputAQG[i-1][0]: 
            if i != 0:
                testResults.append(tempArray)
            tempArray = []
            concept = outputAQG[i][0]
            tempArray.append(concept)
            
        # assessing
        if outputAQG[i][1] == outputAQG[i][2]:
            tempArray.append(1)
        else:
            tempArray.append(0)

        if i == len(outputAQG)-1:
            testResults.append(tempArray)

    return testResults

# Loop through all concepts and get triples and writes to a csv file
def getTriples(outputAQG):

    # Create a set to store the unique first items
    unique_concepts = set()

    # Iterate over the nested arrays and extract the first items
    for item in outputAQG:
        first_concept = item[0]
        unique_concepts.add(first_concept)

    # Convert the set back to a list
    unique_concepts = list(unique_concepts)

    filename = "outputAdaptiveSystem.csv"  # Specify the filename or path
    # Open the file in write mode, which will delete the contents of the file or create a new empty file
    with open(filename, "w") as file:
        pass
    
    triples = ""
    # Loop through the concepts and get the triples
    for concept in unique_concepts:
        triples = triples + Ontology.triples(concept, learnerAbility_ontology,filename)+"\n"
    
    return triples

# Calculate the change per unit from the intial learning abolity to the current
def calculateImprovment(learnerAbility_ontology):

    output=""
    for key in learnerAbility_ontology:
        value = learnerAbility_ontology.get(key)
        change_per_unit = (value+2)/4 # change per unit = (current - initial)/(range end - range start)
        output = output+str(key) + ": " + str(change_per_unit)+"\n"
    
    return output

def getLearnerAbilityOntology():
    # Initialise dictionary set all subjects/objects to -2
    global learnerAbility_ontology
    if learnerAbility_ontology is None:
        learnerAbility_ontology = Ontology.initialise_learner_ability()
    return learnerAbility_ontology

# Function that runs the Adaptive System
def AdaptiveSystem(outputAQG):
    
    start_time = time.time() # start timer

    testResults = assessment_unit(outputAQG)
    learnerAbilities = IRT_unit(testResults)

    print("-"*10 + " RESULTS " + "-"*10)
    print("Learning ability {-2,2} of student for concepts: " + str(learnerAbilities))   

    # Initialise dictionary set all subjects/objects to -2
    global learnerAbility_ontology
    if learnerAbility_ontology is None:
        learnerAbility_ontology = Ontology.initialise_learner_ability()

    # Update the dictionary by calling the method in UpdateOntology
    Ontology.updateDict(learnerAbilities)

    # Get triples for all the concepts
    print(getTriples(outputAQG))

    # Find the improvement
    calculateImprovment(learnerAbility_ontology)

    end_time = time.time() # end timer
    execution_time = end_time - start_time

    print(f"Executed in {round(execution_time,3)}s")

# How the Adaptive System would be called
def main():

    print("Adaptive System Running...")

    import ast

    command = input("Enter (T) TERMINATE to quit the system, else press enter filename to continue: ")

    while command.lower() != "t":
        try:
            # Read input from the file
            with open(command, "r") as file:
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