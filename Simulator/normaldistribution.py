from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np


def plotND():
    ndPossibleAxisValues = norm.rvs(5, 2, 10)
    chancesForEachPossibleAxisValue = []
    chance = 0
    valueForCycleByChance = 0
    counter = 0
    sum = 0
    i = -10
    y = 0

    val = []
    cha = []
    cha2 = []

    while i < 20:
        while y < 10:
            x = i + y / 10
            ch = norm.pdf(x, 5, 2)
            #print(x)
            #print(ch)

            cha.append(ch)


            val.append(x)
            sum += ch
            y += 1
        y = 0
        i += 1

    counter = 0
    while counter < len(cha):
        cha2.append(cha[counter] / sum)
        counter += 1




    print(sum)
    print(val)
    print(cha)
    valueForCycleByChance = np.random.choice(val, 1, p=cha2)
    print(valueForCycleByChance)

    #while counter < ndPossibleAxisValues.size:
        #chance = norm.pdf(ndPossibleAxisValues[counter], loc=100, scale=1)
        #chancesForEachPossibleAxisValue.append(chance)
        # print("wert: " + str(ndPossibleAxisValues[counter]) + ", chance: " + str(chancesForEachPossibleAxisValue[counter]))
        #sum += chance
        #counter += 1

    # valueForCycleByChance = np.random.choice(ndPossibleAxisValues, 1, p=chancesForEachPossibleAxisValue)
    # print("valueForCycleByChance: " + valueForCycleByChance)

    #print(sum)
    #print(chancesForEachPossibleAxisValue)
    # plt.hist(ndPossibleAxisValues, bins = 100)
    # plt.show()


# this function is for calculating all the chances for a range of .2f numbers in a normal distribution
# loc has to have 2 decimal places
# scale has a default value of .5 and is the mean deviation in percent
# max_offset_in_percent is std set to 10 percent and defines the range of values which get created for the chance
# evaluation. this value might need to get increased when the scale is rising
def get_random_number_and_chance(loc, scale=.5, max_offset_in_percent=10):

    values = []
    chance_for_value = []
    chance_for_value_normalized = []
    sum_of_chances = 0  # all the chances combined do not add up to 1, that's why we need to store it so that we can
    # divide the chances by this sum to get the real chance. this value will only differ by a very small value
    step_size = .01  # step_size matters for the chance calculation as we have to loop through all the possible value
    # from min to max with the the given step_size. as loc has to be with 2 decimal places, step_size is also
    mean = loc * scale / 100 # /100 cause scale is in percent
    max_offset = max_offset_in_percent / 100

    # generating values and chance list
    counter = 0
    min_val = round(loc - (loc * max_offset), 2)
    max_val = round((loc + (loc * max_offset)), 2)
    current_value = min_val

    while min_val <= current_value <= max_val:
        chance = norm.pdf(current_value, loc, mean)
        values.append(current_value)
        chance_for_value.append(chance)
        sum_of_chances += chance
        current_value += step_size
        counter += 1

    # normalize chances
    counter = 0
    while counter < len(chance_for_value):
        chance_for_value_normalized.append(chance_for_value[counter] / sum_of_chances)
        counter += 1

    return np.random.choice(values, 1, p=chance_for_value_normalized)

def test():
    a = .005
    b = .01
    c = 0

    while a < 1:
        a += a * b
        print(str(a))
        c += 1

    print("c: " + str(c))

#print(get_random_number_and_chance(5.24, .5, 10))
test()
