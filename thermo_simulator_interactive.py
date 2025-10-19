import json
import numpy as np
import matplotlib.pyplot as plt

# Reuse the same physics from thermo_simulator.py (light copy here)
def isothermal_path(P0, V0, T_const, n, R, final_var, final_value, steps):
    if final_var.upper() == "V":
        V_end = float(final_value)
        V = np.linspace(V0, V_end, steps)
        P = n*R*T_const / V
        T = np.full_like(V, T_const)
    elif final_var.upper() == "P":
        P_end = float(final_value)
        P = np.linspace(P0, P_end, steps)
        V = n*R*T_const / P
        T = np.full_like(P, T_const)
    else:
        raise ValueError("Isothermal requires final_var be 'P' or 'V'")
    return P, V, T

def isobaric_path(P_const, V0, T0, n, R, final_var, final_value, steps):
    if final_var.upper() == "T":
        T_end = float(final_value)
        T = np.linspace(T0, T_end, steps)
        P = np.full_like(T, P_const)
        V = n*R*T / P_const
    elif final_var.upper() == "V":
        V_end = float(final_value)
        V = np.linspace(V0, V_end, steps)
        P = np.full_like(V, P_const)
        T = P_const*V/(n*R)
    else:
        raise ValueError("Isobaric requires final_var be 'T' or 'V'")
    return P, V, T

def isochoric_path(P0, V_const, T0, n, R, final_var, final_value, steps):
    if final_var.upper() == "T":
        T_end = float(final_value)
        T = np.linspace(T0, T_end, steps)
        V = np.full_like(T, V_const)
        P = n*R*T / V_const
    elif final_var.upper() == "P":
        P_end = float(final_value)
        P = np.linspace(P0, P_end, steps)
        V = np.full_like(P, V_const)
        T = P*V_const/(n*R)
    else:
        raise ValueError("Isochoric requires final_var be 'T' or 'P'")
    return P, V, T

def run_chain(n, R, P0, V0, T0, processes):
    import numpy as np
    P_all=[P0]; V_all=[V0]; T_all=[T0]
    P_curr, V_curr, T_curr = P0, V0, T0
    for i, step in enumerate(processes, 1):
        typ = step["type"].lower()
        fvar = step["final_var"]
        fval = step["final_value"]
        s = int(step.get("steps", 100))

        if typ == "isothermal":
            P, V, T = isothermal_path(P_curr, V_curr, T_curr, n, R, fvar, fval, s)
        elif typ == "isobaric":
            P, V, T = isobaric_path(P_curr, V_curr, T_curr, n, R, fvar, fval, s)
        elif typ == "isochoric":
            P, V, T = isochoric_path(P_curr, V_curr, T_curr, n, R, fvar, fval, s)
        else:
            raise ValueError(f"Unknown type: {typ}")

        P_all.extend(P[1:].tolist())
        V_all.extend(V[1:].tolist())
        T_all.extend(T[1:].tolist())
        P_curr, V_curr, T_curr = P[-1], V[-1], T[-1]
        print(f"After step {i}: P={P_curr:.3f} Pa, V={V_curr:.6f} m^3, T={T_curr:.3f} K")
    import numpy as np
    return np.array(P_all), np.array(V_all), np.array(T_all)

def plot_axes(axes, P, V, T, save_path=None):
    axes = axes.upper()
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
        raise ValueError("axes must be one of PV, TV, PT, VT, VP")

    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(x, y, linewidth=2)
    plt.xlabel(xlabel); plt.ylabel(ylabel); plt.title(f"{axes} Diagram"); plt.grid(True)
    if save_path:
        import os; os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    try:
        plt.show()
    except Exception:
        pass

def ask_float(prompt, default=None):
    while True:
        raw = input(f"{prompt}" + (f" [{default}]" if default is not None else "") + ": ").strip()
        if raw == "" and default is not None:
            return float(default)
        try:
            return float(raw)
        except ValueError:
            print("Please enter a number.")

def ask_choice(prompt, choices, default=None):
    chs = "/".join(choices)
    while True:
        raw = input(f"{prompt} ({chs})" + (f" [{default}]" if default else "") + ": ").strip().lower()
        if raw == "" and default:
            return default
        if raw in [c.lower() for c in choices]:
            return raw
        print("Invalid choice.")

def main():
    print("=== Thermo Sim (Interactive) ===")
    print("Units: P in Pa, V in m^3, T in K, R in J/mol·K")
    n  = ask_float("Moles n", 1.0)
    R  = ask_float("Gas constant R (J/mol·K)", 8.314)
    P0 = ask_float("Initial Pressure P0 (Pa)", 101325)
    V0 = ask_float("Initial Volume V0 (m^3)", 0.024465)
    T0 = ask_float("Initial Temperature T0 (K)", 300.0)
    axes = ask_choice("Plot axes", ["PV","TV","PT","VT","VP"], "PV")

    processes = []
    k = int(ask_float("How many process steps?", 2))
    for i in range(1, k+1):
        print(f"\nStep {i}:")
        typ = ask_choice("Type", ["isothermal","isobaric","isochoric"], "isothermal")
        if typ == "isothermal":
            fvar = ask_choice("Final variable", ["P","V"], "V")
        elif typ == "isobaric":
            fvar = ask_choice("Final variable", ["T","V"], "T")
        else:
            fvar = ask_choice("Final variable", ["T","P"], "T")
        fval = ask_float(f"Final value for {fvar}")
        steps = int(ask_float("Resolution (steps along path)", 100))
        processes.append({"type": typ, "final_var": fvar, "final_value": fval, "steps": steps})

    # Ask save path
    default_name = f"plots/interactive_{axes}.png"
    save = input(f"\nSave plot to file? (enter path or leave blank to skip) [{default_name}]: ").strip()
    if save == "":
        save = default_name

    # Optionally dump the process JSON for later reuse
    dump = input("Save your process list to JSON for reuse? (y/n) [y]: ").strip().lower() or "y"
    if dump.startswith("y"):
        out = input("File path for JSON [examples/interactive_run.json]: ").strip() or "examples/interactive_run.json"
        import os; os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w") as f:
            json.dump(processes, f, indent=2)
        print(f"Saved process list to {out}")

    P, V, T = run_chain(n, R, P0, V0, T0, processes)
    plot_axes(axes, P, V, T, save_path=save)
    print("\nDone. Final state:")
    print(f"P={P[-1]:.3f} Pa, V={V[-1]:.6f} m^3, T={T[-1]:.3f} K")
    if save:
        print(f"Plot saved to: {save}")

if __name__ == "__main__":
    main()
