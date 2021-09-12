from influxdb import InfluxDBClient

def compute_next_mean_with_growth_rate(mean, growth_rate):
    next_mean = mean + (mean * growth_rate)
    print("next mean: " + str(next_mean))
    return next_mean

def printSizesOfMeasurements():
    client = InfluxDBClient(host='localhost', port=8086)
    i = 0
    growthrate = .01
    current_mean = 0.25

    while i < 50:
        current_mean = compute_next_mean_with_growth_rate(current_mean, growthrate)
        print(current_mean)
        query_string = 'SELECT count(*) FROM "robodata"."autogen"."mean_' + str(round(current_mean, 5)) + '"'
        results = client.query(query_string)
        print(results.raw)
        i += 1


printSizesOfMeasurements()