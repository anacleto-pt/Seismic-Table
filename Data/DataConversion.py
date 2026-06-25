# DataConversion.py
from functions import Data, steps_calc, print_cpp_arrays

def main():
    Filename1, Filename2 = "Data/NS.csv", "Data/EW.csv"
    ns, ew = Data(Filename1, Filename2)

    stepsN, stepsE, stepsS, stepsW = steps_calc(
        ns, ew,
        max_steps_per_window = 40,   # menos agressivo
        max_position         = 1000,
        microstepping        = 2,
        subsample            = 2
    )

    print_cpp_arrays("N", stepsN)
    print_cpp_arrays("E", stepsE)
    print_cpp_arrays("S", stepsS)
    print_cpp_arrays("W", stepsW)

if __name__ == "__main__":
    main()