# Author: Aakief Hassiem
# Desicription: Ontology python program that handles operations performed on the food_galmat_1.9.owl ontology

#Importing the relevent libraries
from owlready2 import *

#Fetching and loading the relevent ontology
onto = get_ontology("food_galmat_1.9.owl").load()

learnerAbility_dict = {}
is_initialised = False

'''
Obtain the triples (subject|predicate|object) for a given subject and write it to a file
'''
def triples(subject, learnerAbility_dict, filename):

    import csv

    # Retreieve the class of the subject. eg Bread -> food_galmat_1.7.Bread
    subject_class = getattr(onto, subject)

    outputCSV = []

    try:
        # Loop through the properties for the class
        for prop in subject_class.get_class_properties():
            predicate = prop.python_name  # Get the name of the property
            prop_value = getattr(subject_class, predicate)  # Get the objects for a predicate eg. food_galmat_1.7.Sandwich | hasIngredient | food_galmat_1.7.Bread

            objects = list(prop_value)

            # Loop through the objects list 
            for object in objects:
                ability_subject = learnerAbility_dict.get(subject_class) # Learner ability for the subject
                ability_object = learnerAbility_dict.get(object) # Learner ability for the object
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

'''
Initialise the dictionary that stores the learner abilities to 0
'''
def initialise_learner_ability():
    global is_initialised, learnerAbility_dict
    # If the dictionary has not yet been populated
    if not is_initialised:
        allClasses = list(onto.classes()) # Retrieve all the classes in the ontology
        subjects = getSubjects(allClasses)
        # Loop through the classes in the ontology
        for items in subjects:
            # Assign 0 to all the items and add it to a dictionary
            learnerAbility_dict[items] = 0
        is_initialised = True
    return learnerAbility_dict

'''
Function that updates the learner abilities in the ontology
Updates neighbouring concepts
'''
def updateDict(values):

    initialise_learner_ability()

    updatedObjects = []

    # Loop through the list that contains the concepts and the relevant learner ability eg. [[Bread: 1.054],...]
    # Separate everything before and after ":" for each value
    for concept in values:
        key, new_ability = concept.split(":")
        key = getattr(onto, key.strip())
        new_ability = new_ability.strip() #key -> concept, new_ability-> new learner ability
        
        old_ability = learnerAbility_dict.get(key) # get the old learner ability

        updated_ability = 0.25 * float(old_ability) + 0.75 * float(new_ability)

        learnerAbility_dict[key] = round(updated_ability,3) # Update dictionary

        # Update any neighbouring concepts
        for prop in key.get_class_properties():
            predicate = prop.python_name  # Get the name of the property
            corr_objects = getattr(key, predicate)  # Get the objects for a predicate eg. food_galmat_1.7.Sandwich | hasIngredient | food_galmat_1.7.Bread
        
            objects = list(corr_objects)
        
            for object in objects:
                if object in learnerAbility_dict and object not in updatedObjects:
                    old_object_ability = learnerAbility_dict.get(object) # get the old learner ability
                    updated_object_ability = float(old_object_ability)*0.7 + float(new_ability)*0.3
                    learnerAbility_dict[object] = round(updated_object_ability,3) # Update dictionary
                    updatedObjects.append(object)
           
    return learnerAbility_dict

'''
Store all the subjects in the ontology in an array
'''
def getSubjects(allClasses):
    subjects = []
    # Loop through classes in the ontology
    for tempClass in allClasses:
        classProperties = list(tempClass.get_class_properties()) # Properties for each class in the ontology
        if (len(classProperties)>0): # If it has a properties
            # Loop through the properties
            for prop in classProperties:
                predicate = str(prop)
                if (predicate == "food_galmat_1.9.hasIngredient" or predicate == "food_galmat_1.9.hasMainIngredients"):
                    subjects.append(tempClass) # add to subjects array
                elif (predicate == "food_galmat_1.9.hasLanguage"):
                    subjects.append(tempClass)
  
    return subjects

'''
Function to the check the learner ability of a subject
'''
def getSubjectValue(subject,dict):
    subject_class = getattr(onto, subject)
    print(subject, dict.get(subject_class))

