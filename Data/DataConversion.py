from functions import DataFix, steps_calc, dataplot 

def main():
    filename = input("Ficheiro: ")
    print(filename)
    dataset = DataFix(filename)
    steps = steps_calc(data = dataset, lead = 8, step_angle = 1.8, microstepping = 2, adjustment = 1)
    print(steps)
    print("\n\n\nint sismo_steps[] = { " + ", ".join([str(p[1]) for p in steps.items()]) + " };")
    print("\n\n\n" + str(max(steps.values())) + " // Max Steps\n" + str(min(steps.values())) + " // Min Steps")
    dataplot(dataset)

if __name__ == "__main__":
    main()