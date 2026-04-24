# Coluna 1 Tempo
# Coluna 2 Aceleracao
# Coluna 3 Deslocamento
# Total Steps = (Distance in mm / Lead) * Steps Per Revolution * Microstepping

import matplotlib.pyplot as plt
import pandas as pd

def DataFix(filename):
    data = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            data.append(line.split(','))
    return data

def steps_calc(data, lead, step_angle, microstepping, adjustment):
    displacement = []
    [displacement.append(float(data[i][2])) for i in range(1, len(data))]
    steps_per_revolution = 360 / step_angle
    steps = {data[0][0]: 0}
    for i in range(1, len(displacement)):
        steps[data[i][0]] = int(adjustment * (((displacement[i] - displacement[i - 1]) * 1000 / lead) * steps_per_revolution * microstepping))
    return steps

def dataplot(data):
    time = []
    displacement = []
    for i in range(1, len(data)):
        time.append(float(data[i][0]))
        displacement.append(float(data[i][2]))
    plt.plot(time, displacement)
    plt.xlabel('Time (s)')
    plt.ylabel('Displacement (m)')
    plt.title('Time vs Displacement')
    plt.grid()
    plt.show()


print(DataFix("Data/EW.csv")[0])
print(steps_calc(DataFix("Data/EW.csv"), lead = 8, step_angle = 1.8, microstepping = 2, adjustment = 1))
