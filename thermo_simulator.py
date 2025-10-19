import argparse, json
import numpy as np
import matplotlib.pyplot as plt

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
    P_all = [P0]; V_all = [V0]; T_all = [T0]
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

    plt.figure()
    plt.plot(x, y, linewidth=2)
    plt.xlabel(xlabel); plt.ylabel(ylabel)
    plt.title(f"{axes} Diagram")
    plt.grid(True)
    if save_path:
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    # Show only if running interactively
    try:
        plt.show()
    except Exception:
        pass

def main():
    import argparse
    ap = argparse.ArgumentParser(description="Thermo Sim: chain ideal-gas processes and plot diagrams.")
    ap.add_argument("--n", type=float, required=True, help="moles")
    ap.add_argument("--R", type=float, required=True, help="gas constant (J/mol.K)")
    ap.add_argument("--P0", type=float, required=True, help="initial pressure (Pa)")
    ap.add_argument("--V0", type=float, required=True, help="initial volume (m^3)")
    ap.add_argument("--T0", type=float, required=True, help="initial temperature (K)")
    ap.add_argument("--axes", type=str, required=True, help="PV, TV, PT, VT, or VP")
    ap.add_argument("--processes", type=str, required=True, help="path to JSON file describing the process list")
    ap.add_argument("--save", type=str, default=None, help="optional path to save the plot image")
    args = ap.parse_args()

    with open(args.processes, "r") as f:
        processes = json.load(f)

    P, V, T = run_chain(args.n, args.R, args.P0, args.V0, args.T0, processes)
    plot_axes(args.axes, P, V, T, save_path=args.save)

if __name__ == "__main__":
    main()
