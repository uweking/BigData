import json
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import csv
import time


class RobotRotation:
    axis_1 = 0
    axis_2 = 0
    axis_3 = 0
    axis_4 = 0
    axis_5 = 0
    axis_6 = 0

    def __init__(self, a1, a2, a3, a4, a5, a6):
        self.axis_1 = a1
        self.axis_2 = a2
        self.axis_3 = a3
        self.axis_4 = a4
        self.axis_5 = a5
        self.axis_6 = a6




simulated_axis_1 = 0
simulated_axis_2 = 0
simulated_axis_3 = 0
simulated_axis_4 = 0
simulated_axis_5 = 0
simulated_axis_6 = 0
stdCycle = []
simCycle = []
neutralPosition = RobotRotation(-5.182,
                                -107.275,
                                105.275,
                                -3.092,
                                51.233,
                                5.024)

# first and last step are the neutralPosition
maxCycleSteps = 73
csv_file_name_prefix = "cycle_100_"




def simulateValueForStep(step):
    global simulated_axis_1
    global simulated_axis_2
    global simulated_axis_3
    global simulated_axis_4
    global simulated_axis_5
    global simulated_axis_6

    simulated_axis_1 = stdCycle[step].axis_1
    simulated_axis_2 = stdCycle[step].axis_2
    simulated_axis_3 = stdCycle[step].axis_3
    simulated_axis_4 = stdCycle[step].axis_4
    simulated_axis_5 = stdCycle[step].axis_5
    simulated_axis_6 = stdCycle[step].axis_6


def loadStandardCycle():

    start_time = int(time.time_ns() / 1_000_000)
    measurement_id = 0
    counter = 0

    with open('kuka_cycle_real.json') as file:
        data = json.load(file)

    csv_file = open("stdCycle.csv", 'a', newline='')

    i = 0
    while i < len(data["measurements"]):
        print(i)
        stdCycle.append(RobotRotation(round(data["measurements"][i]["position"]["a1"]["value"], 2),
                                      round(data["measurements"][i + 1]["position"]["a2"]["value"], 2),
                                      round(data["measurements"][i + 2]["position"]["a3"]["value"], 2),
                                      round(data["measurements"][i + 3]["position"]["a4"]["value"], 2),
                                      round(data["measurements"][i + 4]["position"]["a5"]["value"], 2),
                                      round(data["measurements"][i + 5]["position"]["a6"]["value"], 2)))

        data_writer = csv.writer(csv_file)
        data_writer.writerow(["stdCycle",
                              str(start_time + (measurement_id * 1000)),
                              measurement_id,
                              0,  # current cycle
                              counter,  # current cycle step
                              round(data["measurements"][i]["position"]["a1"]["value"], 2),
                              round(data["measurements"][i + 1]["position"]["a2"]["value"], 2),
                              round(data["measurements"][i + 2]["position"]["a3"]["value"], 2),
                              round(data["measurements"][i + 3]["position"]["a4"]["value"], 2),
                              round(data["measurements"][i + 4]["position"]["a5"]["value"], 2),
                              round(data["measurements"][i + 5]["position"]["a6"]["value"], 2)])

        counter += 1
        measurement_id += 1
        i += 6

    csv_file.close()


def simulateFullCycle(cycles):

    global stdCycle
    global simCycle
    temp_cycle = []
    counter = 0
    cycle_counter = 0
    start_mean = .05
    mean = start_mean
    measurement_id = 0
    start_time = int(time.time_ns() / 1_000_000)
    file_counter = 0
    mean_growth = .01  # 1%
    runs_per_cycle = 100
    # before we can start simulating data, we need to load the std data where we base our simulation on
    loadStandardCycle()

    print("starting simulation")

    while cycle_counter < cycles:
        # compute the next mean
        if cycle_counter != 0 and cycle_counter % runs_per_cycle == 0:
            mean = compute_next_mean_with_growth_rate(mean, mean_growth)

        # generating the name of the next csv file
        if cycle_counter % runs_per_cycle == 0:
            csv_file_name = csv_file_name_prefix + str(file_counter) + "_" + str(round(mean, 5)) + ".csv"
            file_counter += 1

        csv_file = open(csv_file_name, 'a', newline='')

        # print("starting simulation of cycle " + str(cycle_counter))

        while counter < len(stdCycle):
            axis1std = round((stdCycle[counter]).axis_1, 2)
            axis2std = round((stdCycle[counter]).axis_2, 2)
            axis3std = round((stdCycle[counter]).axis_3, 2)
            axis4std = round((stdCycle[counter]).axis_4, 2)
            axis5std = round((stdCycle[counter]).axis_5, 2)
            axis6std = round((stdCycle[counter]).axis_6, 2)

            data_writer = csv.writer(csv_file)
            data_writer.writerow(["mean_" + str(round(mean, 5)),
                                  str(start_time + (measurement_id * 1000)),
                                  measurement_id,
                                  cycle_counter,  # current cycle
                                  counter,  # current cycle step
                                  round(get_random_number_by_chance(axis1std, scale=round(mean, 5))[0], 2),
                                  round(get_random_number_by_chance(axis2std, scale=round(mean, 5))[0], 2),
                                  round(get_random_number_by_chance(axis3std, scale=round(mean, 5))[0], 2),
                                  round(get_random_number_by_chance(axis4std, scale=round(mean, 5))[0], 2),
                                  round(get_random_number_by_chance(axis5std, scale=round(mean, 5))[0], 2),
                                  round(get_random_number_by_chance(axis6std, scale=round(mean, 5))[0], 2)
                                  ])

            counter += 1
            measurement_id += 1

        cycle_counter += 1
        counter = 0
        csv_file.close()

    print("finished simulation")



def compute_next_mean_with_growth_rate(mean, growth_rate):
    next_mean = mean + (mean * growth_rate)
    # print("next mean: " + str(next_mean))
    return next_mean

# this function is for calculating all the chances for a range of .2f numbers in a normal distribution
# loc has to have 2 decimal places
# scale has a default value of .5 and is the mean deviation in percent
# max_offset_in_percent is std set to 10 percent and defines the range of values which get created for the chance
# evaluation. this value might need to get increased when the scale is rising
def get_random_number_by_chance(loc, scale=.25, max_offset_in_percent=1.25):

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
    min_val = round(loc - abs(loc * max_offset), 2)
    max_val = round((loc + abs(loc * max_offset)), 2)
    current_value = min_val

    while min_val <= current_value <= max_val:
        chance = norm.pdf(current_value, loc, abs(mean))
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

    global simCycle

    loadStandardCycle()
    simulateFullCycle(2)

    print(len(simCycle))
    print()

    i = 0
    k = 0

    while i < simCycle[k].get_length():
        print(str(simCycle[0].cycle[i].axis_1) + "  :  " + str(simCycle[1].cycle[i].axis_1))
        i += 1

simulateFullCycle(10000)
# loadStandardCycle()