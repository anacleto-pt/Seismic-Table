import pandas as pd

# Coluna 1 Tempo
# Coluna 2 Aceleracao
# Coluna 3 Deslocamento
# Total Steps = (Distance in mm / Lead) * Steps Per Revolution * Microstepping

def Data(filename1, filename2):
    ns = pd.read_csv(filename1)
    ew = pd.read_csv(filename2)
    ns.drop(ns.columns[1], axis=1, inplace=True)
    ew.drop(ew.columns[1], axis=1, inplace=True)
    return ns, ew


def steps_calc(data1, data2, adjustment, microstepping, lead = 8, step_angle = 1.8):
    steps_per_revolution = 360 / step_angle
    steps_N = []
    steps_E = []
    steps_S = []
    steps_W = []
    for i in range(1, len(data1.displacement)):
        steps_N.append(round(adjustment * (((data1.displacement[i] - data1.displacement[i - 1]) * 1000 / lead) * steps_per_revolution * microstepping)))
        steps_S.append(steps_N[-1] * -1)
    for i in range(1, len(data2.displacement)):
        steps_E.append(round(adjustment * (((data2.displacement[i] - data2.displacement[i - 1]) * 1000 / lead) * steps_per_revolution * microstepping)))
        steps_W.append(steps_E[-1] * -1)
    return steps_N, steps_E, steps_S, steps_W

def print_cpp_arrays(name, data):
    # Join the integers into a string separated by commas
    array_content = ", ".join(map(str, data))
    
    print(f"\n// --- {name} Data ---")
    print(f"int sismo_{name}[] = {{ {array_content} }};")
    print(f"int sismo_{name}_len = {len(data)};")
