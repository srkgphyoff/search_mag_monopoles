import random
import ROOT
from ROOT import TMVA

#Define search space
param_ranges = {
    "NTrees": (100, 800),
    "MaxDepth": (2, 6),
    "MinNodeSize": (1.0, 10.0)
}

#Function to convert dictionary(individual to tmva option)
def indTMVAOpt(individual, float_prec):
    """
    Inputs:
    individual (dict)
    float_prec (int) : precision of float values required
    Outputs:
    TMVA BDT option string
    """
    formatted = []

    for key, value in individual.items():
        if isinstance(value, float):
            val_str = f"{value:.{float_prec}f}"
        else:
            val_str = f"{value}"

        formatted.append(f"{key}={val_str}")
    
    #Adding fixedoptions
    formatted.append("BoostType=AdaBoost")
    formatted.append("UseBaggedBoost=True")

    return "!H:!V:" + ":".join(formatted)   #prepending


#Function which creates a random individual using a random set of hyperparameters

def createIndividual(param_ranges):
    """
    Inputs:
    param_ranges (dict) : keys are parameters and values are tuples (min, max)
    Output:
    A single individual 
    """
    ind = {}
    for key, values in param_ranges.items():
        if isinstance(values[0], float):      #since values is a tuple, here if a float
            ind[key] = random.uniform(values[0], values[1])
        else:                       #Here an integer
            ind[key] = random.randint(values[0], values[1])
    
    return ind





#Function for creating Cross Over between two parents
def crossOver(parent1, parent2, crossover_rate):
    """
    Inputs:
    parent1, parent2 : individuals between which cross over takes place
    co_rate          : the rate of cross over (between 0 and 1)
    """
    chance = random.uniform(0, 1)
    if chance > crossover_rate:
        if random.uniform(0,1) > 0.5:
            return parent1.copy()
        else:
            return parent2.copy()
    
    child = {}
    for key in parent1:
        if random.random()<0.5:
            child[key] = parent1[key]
        else:
            child[key] = parent2[key]
    
    return child




#Function for mutation
def mutate(individual, mutation_rate, param_ranges):
    for key, val in param_ranges.items():
        if random.random() < mutation_rate:
            if isinstance(val[0], float):
                individual[key] = round(random.uniform(val[0], val[1]), 2)
            else:
                individual[key] = random.randint(*val)
    
    return individual


