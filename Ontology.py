# Author: Aakief Hassiem
# Desicription: Ontology python program that handles operations performed on the food_galmat_1.7.owl ontology

#Importing the relevent libraries
from owlready2 import *

#Fetching and loading the relevent ontology
onto = get_ontology("food_galmat_1.7.owl").load()

learnerAbility_ontology = {}
is_initialised = False

# Get the triples (subject|predicate|object) for a given subject and write it to a file
def triples(subject, learnerAbility_ontology, filename):

    import csv

    # Retreieve the class of the subject. eg Bread -> food_galmat_1.7.Bread
    subject_class = getattr(onto, subject)

    outputCSV = []

    try:
        # Loop through the properties for the class
        for prop in subject_class.get_class_properties():
            predicate = prop.python_name  # Get the name of the property
            prop_value = getattr(subject_class, predicate)  # Get the objects for a predicate eg. food_galmat_1.7.Sandwich | hasIngredient | food_galmat_1.7.Bread
            #print(predicate, prop_value)

            objects = list(prop_value)

            # Loop through the objects list 
            for object in objects:
                ability_subject = learnerAbility_ontology.get(subject_class) # Learner ability for the subject
                ability_object = learnerAbility_ontology.get(object) # Learner ability for the object
                output = "{:^20s} | {:^20s} | {:^50s} | {:<4s} | {:^4s}".format(
                        str(subject_class), str(predicate), str(object), str(ability_subject), str(ability_object))
                print(output)
                #P Put output in a list and append it to outputCSV
                outputCSV.append([str(subject_class), str(predicate), str(object), str(ability_subject), str(ability_object)])

    except AttributeError:
        # Handle the case when the class is not found in the ontology
        print(f"Class '{subject}' not found in the ontology.")

    # Write data to the CSV file
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)

        # Write each row in the data list to the CSV file
        for row in outputCSV:
            writer.writerow(row)

# Initialise the "ontology" that stores the learner abilities in a dictionary 
def initialise_learner_ability():
    global is_initialised, learnerAbility_ontology
    # If the dictionary has not yet been populated
    if not is_initialised:
        allClasses = list(onto.classes()) # Retrieve all the classes in the ontology
        # Loop through the classes in the ontology
        for items in allClasses:
            # Assign -2 to all the items and add it to a dictionary
            learnerAbility_ontology[items] = -2
        is_initialised = True
    return learnerAbility_ontology

# Function that updates the learner abilities in the ontology
def updateDict(values):

    initialise_learner_ability()

    # Loop through the list that contains the concepts and the relevant learner ability eg. [[Bread: 1.054],...]
    # Separate everything before and after ":" for each value
    for value in values:
        key, new_ability = value.split(":")
        key = getattr(onto, key.strip())
        new_ability = new_ability.strip() #key -> concept, new_ability-> new learner ability
        
        old_ability = learnerAbility_ontology.get(key) # get the old learner ability

        updated_ability = float(old_ability)*0.25 + float(new_ability)*0.75 # Make a weighted sum

        learnerAbility_ontology[key] = round(updated_ability,3) # Update dictionary

    return learnerAbility_ontology

# Function to the check the learner ability of a subject
def checkSubjectValue(subject, dict):
    subject_class = getattr(onto, subject)
    print(subject, dict.get(subject_class))