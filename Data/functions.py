import pandas as pd

def Data(filename1, filename2):
    ns = pd.read_csv(filename1)
    ew = pd.read_csv(filename2)
    ns.drop(ns.columns[1], axis=1, inplace=True)
    ew.drop(ew.columns[1], axis=1, inplace=True)
    return ns, ew


def steps_calc(data1, data2, max_steps_per_window=50, max_position=2500, microstepping=2, lead=8, step_angle=1.8, subsample=2):
    """
    subsample: pega 1 em cada N pontos do CSV original.
               subsample=1 → frequência original (50Hz)
               subsample=2 → metade da frequência (~25Hz, mais parecido com sismo real percetível)
               subsample=3 → um terço (~17Hz)
    """
    steps_per_revolution = 360 / step_angle

    steps_N, steps_E, steps_S, steps_W = [], [], [], []
    pos_NS = 0
    pos_EW = 0

    indices_ns = range(1, len(data1.displacement), subsample)
    indices_ew = range(1, len(data2.displacement), subsample)

    prev_ns = data1.displacement.iloc[0]
    for i in indices_ns:
        curr = data1.displacement.iloc[i]
        delta_mm = (curr - prev_ns) * 1000
        prev_ns = curr

        s = round((delta_mm / lead) * steps_per_revolution * microstepping)
        s = max(-max_steps_per_window, min(max_steps_per_window, s))

        nova_pos = pos_NS + s
        if nova_pos > max_position:
            s = max_position - pos_NS
        elif nova_pos < -max_position:
            s = -max_position - pos_NS

        pos_NS += s
        steps_N.append(s)
        steps_S.append(-s)

    prev_ew = data2.displacement.iloc[0]
    for i in indices_ew:
        curr = data2.displacement.iloc[i]
        delta_mm = (curr - prev_ew) * 1000
        prev_ew = curr

        s = round((delta_mm / lead) * steps_per_revolution * microstepping)
        s = max(-max_steps_per_window, min(max_steps_per_window, s))

        nova_pos = pos_EW + s
        if nova_pos > max_position:
            s = max_position - pos_EW
        elif nova_pos < -max_position:
            s = -max_position - pos_EW

        pos_EW += s
        steps_E.append(s)
        steps_W.append(-s)

    min_len = min(len(steps_N), len(steps_E))
    steps_N = steps_N[:min_len]
    steps_S = steps_S[:min_len]
    steps_E = steps_E[:min_len]
    steps_W = steps_W[:min_len]

    print(f"// totalPontos = {min_len}")
    print(f"// Pos NS final: {pos_NS} | Pos EW final: {pos_EW}")
    print(f"// Intervalo firmware: {20 * subsample}ms")

    return steps_N, steps_E, steps_S, steps_W


def print_cpp_arrays(name, data):
    array_content = ", ".join(map(str, data))
    print(f"\n// --- {name} Data ---")
    print(f"int sismo_{name}[] = {{ {array_content} }};")
    print(f"int sismo_{name}_len = {len(data)};")