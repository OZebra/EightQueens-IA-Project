import random
import re

POPULATION_SIZE = 100
INDIVIDUAL_SIZE = 8
CANDIDATE_AMMOUNT = 5

MAX_CROSS_ITERATIONS = 10

def arrayToString(array):
    finalstring = ''
    for item in array:
        finalstring += format(item,'b').zfill(3) 

    return finalstring

def binaryToInt(string):
    return int(string, 2)

def stringToArray(string):
    array = re.findall('...', string)
    array = list(map(binaryToInt, array))
    return array

def makeIndividual():
    individual =  [None] * INDIVIDUAL_SIZE
    #Adicionar (indSize + 1) no lugar do 9 pra fazer tabuleiros maiores
    for x in range(0,INDIVIDUAL_SIZE):
        random.seed()
        index = random.randrange(0,INDIVIDUAL_SIZE)

        while individual[index] != None:
            index = random.randrange(0,INDIVIDUAL_SIZE)
        
        individual[index] = x

    return arrayToString(individual)

def initPopulation(pop_size):
    popList = []

    for x in range(0,pop_size):
        ind = makeIndividual()
        popList.append({
            'genotype': ind,
            'fitness': 0
        })

    return popList

def calculateColisions(gen):
    genAsArray = stringToArray(gen)
    colisionCount = 0

    for index in range(len(genAsArray)):
        for searchIndex in range(1, len(genAsArray)):
            posIndex = index + searchIndex
            negIndex = index - searchIndex

            if negIndex >= 0:
                if abs(genAsArray[index] - genAsArray[negIndex]) == searchIndex:
                    colisionCount += 1
                if(abs(genAsArray[index] - genAsArray[negIndex]) == 0):
                    colisionCount += 1

            if posIndex <= 7:
                if abs(genAsArray[index] - genAsArray[posIndex]) == searchIndex:
                    colisionCount += 1 
                if abs(genAsArray[index] - genAsArray[posIndex]) == 0:
                    colisionCount += 1 

    return colisionCount/2
    

def calculateIndividualFitness(ind):
    genColisions = calculateColisions(ind['genotype'])

    ind['fitness'] = 1/(1+(0.15*genColisions))

    return ind


def calculatePopulationFitness(pop):
    for ind_index in range(0,len(pop)):
        pop[ind_index] = calculateIndividualFitness(pop[ind_index])

    return pop

def validatePopulation(pop):
    maxFitness = 0

    for individual in pop:
        if individual['fitness'] > maxFitness:
            maxFitness = individual['fitness']

    return maxFitness

def getIndividualFitness(individual):
    return individual['fitness']

def selectParents(pop):
    parents = []
    popLength = len(pop)

    for iterator in range(MAX_CROSS_ITERATIONS):
        parentsCandidates = []

        for index in range(CANDIDATE_AMMOUNT):
            random.seed()

            randIndex = random.randrange(popLength);

            parentsCandidates.append(pop[randIndex])
        
        parentsCandidates.sort(key = getIndividualFitness)
        parent_1 = parentsCandidates.pop()
        parent_2 = parentsCandidates.pop()

        parents.append({
            "firstParent": parent_1,
            "secondParent": parent_2
        })

    return parents

def cutAndCross(child_1, child_2):
    gen_1 = stringToArray(child_1['genotype']);
    gen_2 = stringToArray(child_2['genotype']);

    crossGen = []

    crossOverControl = []

    for index in range(0,3):
        crossGen.append(gen_1[index])
        crossOverControl.append(gen_1[index]);
    
    for index in range(3,11):
        if(index < 8):
            if gen_2[index] not in crossOverControl:
                crossGen.append(gen_2[index]);
                crossOverControl.append(gen_2[index]);
        
        else:
            if(gen_2[index-8] not in crossOverControl):
                crossGen.append(gen_2[index - 8]);
                crossOverControl.append(gen_2[index-8]);

    return {
        'genotype': arrayToString(crossGen),
        'fitness': 0
    }

def generateChildren(parents):
    generatedChildren = []

    for pair in parents:
        random.seed()
        shuffleChance = random.random()
        if(shuffleChance < 0.9):
            child_1 = cutAndCross(pair['firstParent'], pair['secondParent'])
            child_2 = cutAndCross(pair['secondParent'], pair['firstParent'])
        
        else:
            child_1 = pair['firstParent']
            child_2 = pair['secondParent']
        
        generatedChildren.append(child_1);
        generatedChildren.append(child_2);

    return generatedChildren

def mutate(individual):
    genAsArray = stringToArray(individual['genotype'])

    first = random.randrange(len(genAsArray))
    second = random.randrange(len(genAsArray))

    auxiliar = genAsArray[first]
    genAsArray[first] = genAsArray[second]
    genAsArray[second] = auxiliar
 
    individual['genotype'] = arrayToString(genAsArray)

    return individual


def procreatePopulation(pop):
    parentsPairs = selectParents(pop)
    children = generateChildren(parentsPairs)
    childrenAmmount = len(children)
    
    for index in range(0,childrenAmmount):
        random.seed()
        roll = random.randrange(0,10)

        if roll < 4:
            children[index] = mutate(children[index])


    return pop + children

def filterPopulation(pop):
    newPopulation = calculatePopulationFitness(pop)
    newPopulation.sort(key = getIndividualFitness, reverse = True);

    populationOverflow = len(newPopulation) - 100

    while populationOverflow > 0:
        newPopulation.pop()
        populationOverflow -= 1

    return newPopulation

def printIndividuals(individuals):
    indLength = len(individuals)
    iterator = 1;

    for index in range(0, indLength):

        iterator += 1

def runByIterations(iterationMax):
    population = initPopulation(POPULATION_SIZE)
    population = calculatePopulationFitness(population)

    iterations = 0

    while(iterations <= iterationMax):
        population = procreatePopulation(population)
        population = filterPopulation(population)

        iterations += 1

    return {
        'population': population,
        'iterationCount': iterations
    }

def runByFitness():

    population = initPopulation(100)

    population = calculatePopulationFitness(population)

    iterator = 0
    while(validatePopulation(population) < 1 and iterator < 10000):
        population = procreatePopulation(population)
        population = filterPopulation(population)
        iterator += 1

    return {
        'population': population,
        'iterationCount': iterator
    }