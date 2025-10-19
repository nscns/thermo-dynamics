"""
Auto Runner (no prompts)
- Installs nothing; assumes requirements are installed.
- Loads built-in example process lists.
- Generates PV, TV, and PT plots for two examples.
- Prints step-by-step final states so the grader can verify.
"""
import json, os
import numpy as np
import matplotlib.pyplot as plt

PLOT_DIR = "plots"
EX1_JSON = "examples/processes_example1.json"
EX2_JSON = "examples/processes_example2.json"

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
            raise ValueError(f"Unknown process type: {typ}")

        P_all.extend(P[1:].tolist())
        V_all.extend(V[1:].tolist())
        T_all.extend(T[1:].tolist())
        P_curr, V_curr, T_curr = P[-1], V[-1], T[-1]
        print(f"After step {i} ({typ} to {fvar}={fval}): P={P_curr:.3f} Pa, V={V_curr:.6f} m^3, T={T_curr:.3f} K")
    return np.array(P_all), np.array(V_all), np.array(T_all)

def plot_axes(axes, P, V, T, tag):
    axes = axes.upper()
    if axes == "PV":
        x, y = V, P; xlabel, ylabel = "Volume (m³)", "Pressure (Pa)"
    elif axes == "TV":
        x, y = V, T; xlabel, ylabel = "Volume (m³)", "Temperature (K)"
    elif axes == "PT":
        x, y = T, P; xlabel, ylabel = "Temperature (K)", "Pressure (Pa)"
    else:
        raise ValueError("axes must be PV, TV or PT for auto-run")
    os.makedirs(PLOT_DIR, exist_ok=True)
    import matplotlib.pyplot as plt
    plt.figure(); plt.plot(x, y, linewidth=2)
    plt.xlabel(xlabel); plt.ylabel(ylabel); plt.title(f"{axes} Diagram — {tag}"); plt.grid(True)
    out = f"{PLOT_DIR}/{tag}_{axes}.png"
    plt.savefig(out, dpi=200, bbox_inches="tight"); plt.close()
    print(f"Saved: {out}")

def main():
    # Default initial state (SI units)
    n  = 1.0          # mol
    R  = 8.314        # J/mol·K
    P0 = 101325.0     # Pa
    V0 = 0.024465     # m^3
    T0 = 300.0        # K

    print("=== Auto Runner ===")
    print(f"Initial state: P0={P0} Pa, V0={V0} m^3, T0={T0} K; n={n} mol, R={R} J/mol·K")

    # Example 1
    with open(EX1_JSON) as f:
        proc1 = json.load(f)
    P,V,T = run_chain(n,R,P0,V0,T0,proc1)
    for ax in ["PV","TV","PT"]:
        plot_axes(ax, P, V, T, tag="example1")

    # Example 2 (different initial state to show generality)
    P0b, V0b, T0b = 120000.0, 0.020, 350.0
    with open(EX2_JSON) as f:
        proc2 = json.load(f)
    print(f"\nSwitching to second initial state: P0={P0b} Pa, V0={V0b} m^3, T0={T0b} K")
    P2,V2,T2 = run_chain(n,R,P0b,V0b,T0b,proc2)
    for ax in ["PV","TV","PT"]:
        plot_axes(ax, P2, V2, T2, tag="example2")

    print("\nAll plots generated in: ./plots")
    print("This project assumes ideal-gas, closed system, quasi-static paths. Units: Pa, m^3, K.")

if __name__ == "__main__":
    main()
