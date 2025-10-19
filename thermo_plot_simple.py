import numpy as np
import matplotlib.pyplot as plt

def ask_float(name, default=None):
    while True:
        s = input(f"{name}" + (f" [{default}]" if default is not None else "") + ": ").strip()
        if s == "" and default is not None:
            return float(default)
        try:
            return float(s)
        except ValueError:
            print("Enter a number.")

def main():
    print("=== Simple Thermo Plotter ===")
    print("Inputs in SI: P (Pa), V (m^3), T (K)")
    # Initial state
    P0 = ask_float("Initial Pressure P0 (Pa)", 101325.0)
    V0 = ask_float("Initial Volume V0 (m^3)", 0.02)
    T0 = ask_float("Initial Temperature T0 (K)", 300.0)
    # Final state
    P1 = ask_float("Final Pressure P1 (Pa)", 150000.0)
    V1 = ask_float("Final Volume V1 (m^3)", 0.04)
    T1 = ask_float("Final Temperature T1 (K)", 400.0)

    axes = input("Plot axes (PV/TV/PT/VT/VP) [PV]: ").strip().upper() or "PV"
    steps = int(ask_float("Path resolution (points)", 200))

    # Straight-line interpolation between start and end states
    P = np.linspace(P0, P1, steps)
    V = np.linspace(V0, V1, steps)
    T = np.linspace(T0, T1, steps)

    # Select axes
    if axes == "PV":
        x, y = V, P; xlabel, ylabel = "Volume (m³)", "Pressure (Pa)"
    elif axes == "TV":
        x, y = V, T; xlabel, ylabel = "Volume (m³)", "Temperature (K)"
    elif axes == "PT":
        x, y = T, P; xlabel, ylabel = "Temperature (K)", "Pressure (Pa)"
    elif axes == "VT":
        x, y = T, V; xlabel, ylabel = "Temperature (K)", "Volume (m³)"
    elif axes == "VP":
        x, y = P, V; xlabel, ylabel = "Pressure (Pa)", "Volume (m³)"
    else:
        raise SystemExit("Invalid axes. Use PV/TV/PT/VT/VP.")

    import os
    os.makedirs("plots", exist_ok=True)
    save_path = f"plots/simple_{axes}.png"

    plt.figure()
    plt.plot(x, y, linewidth=2)
    plt.scatter([x[0], x[-1]],[y[0], y[-1]], marker='o')  # mark endpoints
    plt.xlabel(xlabel); plt.ylabel(ylabel); plt.title(f"{axes} Diagram (linear path)"); plt.grid(True)
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    try:
        plt.show()
    except Exception:
        pass

    print(f"\nSaved plot: {save_path}")
    print(f"Initial: P={P0:.3f} Pa, V={V0:.6f} m^3, T={T0:.2f} K")
    print(f"Final:   P={P1:.3f} Pa, V={V1:.6f} m^3, T={T1:.2f} K")

if __name__ == "__main__":
    main()
