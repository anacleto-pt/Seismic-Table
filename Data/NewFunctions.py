import pandas as pd

# Coluna 1 Tempo
# Coluna 2 Aceleracao
# Coluna 3 Deslocamento
# Total Steps = (Distance in mm / Lead) * Steps Per Revolution * Microstepping

def Data(filename):
    df = pd.read_csv(filename)
    df.drop(df.columns[1], axis=1, inplace=True)
    return df


def steps_calc(data, adjustment, microstepping, lead = 8, step_angle = 1.8):
    steps_per_revolution = 360 / step_angle
    steps = [(data.displacement[i] / lead) * steps_per_revolution * microstepping * adjustment for i in range(1, len(data.displacement))]
    return steps


print(Data("Data/EW.csv"))
print(steps_calc(Data("Data/EW.csv"), adjustment = 1, microstepping = 2))