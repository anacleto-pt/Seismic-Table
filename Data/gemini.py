import math

def read_file(filename):
    data = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip():
                data.append(line.strip().split(','))
    return data

def extract_data(data):
    parsed = {}
    for row in data:
        try:
            t = float(row[0])
            val = float(row[2])
            parsed[t] = val
        except ValueError:
            pass
    return parsed

def sync_datasets(data_ns, data_ew):
    common_times = sorted(list(set(data_ns.keys()) & set(data_ew.keys())))
    return [(t, data_ew[t], data_ns[t]) for t in common_times]

def actuator_lengths(x_mm, y_mm, l_mm):
    dn = math.sqrt(x_mm**2 + (y_mm + l_mm)**2)
    de = math.sqrt((x_mm + l_mm)**2 + y_mm**2)
    ds = math.sqrt(x_mm**2 + (y_mm - l_mm)**2)
    dw = math.sqrt((x_mm - l_mm)**2 + y_mm**2)
    return dn, de, ds, dw

def calculate_all_steps(synced_data, l_mm, lead, step_angle, microstepping, adjustment):
    steps_per_rev = 360 / step_angle
    factor = adjustment * (steps_per_rev * microstepping) / lead
    
    dict_n, dict_e, dict_s, dict_w = {}, {}, {}, {}
    
    if not synced_data:
        return dict_n, dict_e, dict_s, dict_w

    _, init_x, init_y = synced_data[0]
    prev_dn, prev_de, prev_ds, prev_dw = actuator_lengths(init_x * 1000, init_y * 1000, l_mm)
    
    dict_n[synced_data[0][0]] = 0
    dict_e[synced_data[0][0]] = 0
    dict_s[synced_data[0][0]] = 0
    dict_w[synced_data[0][0]] = 0

    for i in range(1, len(synced_data)):
        t, x_m, y_m = synced_data[i]
        
        x_mm = x_m * 1000
        y_mm = y_m * 1000
        
        dn, de, ds, dw = actuator_lengths(x_mm, y_mm, l_mm)
        
        dict_n[t] = int((dn - prev_dn) * factor)
        dict_e[t] = int((de - prev_de) * factor)
        dict_s[t] = int((ds - prev_ds) * factor)
        dict_w[t] = int((dw - prev_dw) * factor)
        
        prev_dn, prev_de, prev_ds, prev_dw = dn, de, ds, dw
        
    return dict_n, dict_e, dict_s, dict_w

def main(file_ns, file_ew, l_mm=250.0, lead=8.0, step_angle=1.8, microstepping=2, adjustment=1.0):
    raw_ns = read_file(file_ns)
    raw_ew = read_file(file_ew)
    
    data_ns = extract_data(raw_ns)
    data_ew = extract_data(raw_ew)
    
    synced_data = sync_datasets(data_ns, data_ew)
    
    steps_n, steps_e, steps_s, steps_w = calculate_all_steps(
        synced_data, 
        l_mm, 
        lead, 
        step_angle, 
        microstepping, 
        adjustment
    )
    
    print(steps_n)
    print(steps_e)
    print(steps_s)
    print(steps_w)

if __name__ == "__main__":
    main("Data/NS.csv", "Data/EW.csv")