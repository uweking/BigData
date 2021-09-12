#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from datetime import datetime
import paho.mqtt.client as mqtt
import time, threading, random
import os
import valueSimulator


serverUrl = "localhost"
clientId = "big_data"
# device_name = "KUKA_Simulator"
#tenant = "nwxrc"
##username = "cumulocityforsc4rlet@gmail.com" # take the secrets from keepass
#username = "iot_connector_technical_user"
#password = "W&H:$MXG#:'rK2U1TP4S"
#a1_stdVal = 0
#a2_stdVal = -110
#a3_stdVal = 107
#a4_stdVal = 0
#a5_stdVal = 3
#a6_stdVal = -1
#runstate_stdVal = 0
#anomalyscore_stdVal = 0
#runstate = 0
receivedMessages = []
#timeoutOnAck = 5 # in seconds
cyclesToSimulate = 1

#display all incoming messages
def on_message(client, userdata, msg):
    print("message received")

# send temnperature measurement
def sendTempMeasurements():
    while True:
        # print("temp data send")
        publish("temp/", "time,value\n" + str(int(time.time_ns() / 1_000_000)) + "," + str(random.uniform(-10, 10)))
        time.sleep(5)

# send axis measurement
def sendAxisMeasurements():
    global cyclesToSimulate
    measurementId = 0
    cycle = 0
    cycleStep = 0

    print("start sending simulated data")

    while cycle < cyclesToSimulate:
        print("start sending data from cycle " + str(cycle))
        while cycleStep < valueSimulator.maxCycleSteps:
            # print("axis data send")

            publish("axis/", "time,id,cycle,cycleStep,a1,a2,a3,a4,a5,a6,value\n" + str(int(time.time_ns() / 1_000_000) + 100000000) +
                    "," + str(measurementId) +
                    "," + str(cycle) +
                    "," + str(cycleStep) +
                    "," + str(valueSimulator.simCycle[cycle].cycle[cycleStep].axis_1) +
                    "," + str(valueSimulator.simCycle[cycle].cycle[cycleStep].axis_2) +
                    "," + str(valueSimulator.simCycle[cycle].cycle[cycleStep].axis_3) +
                    "," + str(valueSimulator.simCycle[cycle].cycle[cycleStep].axis_4) +
                    "," + str(valueSimulator.simCycle[cycle].cycle[cycleStep].axis_5) +
                    "," + str(valueSimulator.simCycle[cycle].cycle[cycleStep].axis_6)
                    )
            measurementId += 1
            cycleStep += 1
            time.sleep(1)
        print("finished sending data from cycle " + str(cycle))
        cycleStep = 0
        cycle += 1
        time.sleep(1)

    print("finished sending simulated data")


# publish a message
# qos = 2
def publish(topic, message, waitForAck = False):
    mid = client.publish(topic, message, 2)[1]


def on_publish(client, userdata, mid):
    receivedMessages.append(mid)


client = mqtt.Client(clientId)
client.on_message = on_message
client.on_publish = on_publish

client.connect(serverUrl)
client.loop_start()

if __name__ == "__main__":
    print("start")
    valueSimulator.simulateFullCycle(cyclesToSimulate)
    axisData = threading.Thread(target=sendAxisMeasurements)
    axisData.start()
    #tempData = threading.Thread(target=sendTempMeasurements)
    #tempData.start()
    axisData.join()
    print("end")
