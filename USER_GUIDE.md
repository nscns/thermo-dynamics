# Thermo Sim — User Guide (≤ 2 pages)

**Purpose:** Chain ideal-gas, closed-system processes (isochoric, isobaric, isothermal) and plot PV/TV/PT/VT/VP diagrams.

## 1) Assumptions
- Ideal gas: PV = nRT (R supplied by user).
- Closed system (constant moles n).
- Quasi-static paths; each step’s end is next step’s start.
- Units: Pa, m³, K, J/mol·K.

## 2) Inputs
CLI flags and a JSON file with the process list.

**Initial state (required):**
- `--n`, `--R`, `--P0`, `--V0`, `--T0`

**Axes:**
- `--axes` in {PV, TV, PT, VT, VP}

**Process JSON objects:**
- `"type"`: `"isothermal"` or `"isobaric"` or `"isochoric"`
- `"final_var"`: one of `"P"`, `"V"`, `"T"`
- `"final_value"`: numeric
- `"steps"`: optional integer resolution (default 100)

Physics rules:
- Isothermal → final_var must be P or V (T fixed).
- Isobaric → final_var must be T or V (P fixed).
- Isochoric → final_var must be T or P (V fixed).

## 3) Output
- Shows a plot and optionally saves image (`--save`).
- Prints final (P, V, T) after each step.

## 4) Run
```bash
python thermo_simulator.py --n 1.0 --R 8.314   --P0 101325 --V0 0.024465 --T0 300   --axes PV --processes examples/processes_example1.json   --save plots/example1_PV.png
```

## 5) Worked Example A (PV)
Initial: n=1 mol, R=8.314, P0=101325 Pa, V0=0.024465 m³, T0=300 K  
Sequence: `examples/processes_example1.json`
```json
[
  {"type":"isothermal","final_var":"V","final_value":0.04,"steps":120},
  {"type":"isobaric","final_var":"T","final_value":400,"steps":80},
  {"type":"isochoric","final_var":"P","final_value":150000,"steps":80}
]
```
Command:
```bash
python thermo_simulator.py --n 1 --R 8.314 --P0 101325 --V0 0.024465 --T0 300   --axes PV --processes examples/processes_example1.json --save plots/example1_PV.png
```

## 6) Worked Example B (TV)
Initial: n=1, R=8.314, P0=120000 Pa, V0=0.02 m³, T0=350 K  
Sequence: `examples/processes_example2.json`
```json
[
  {"type":"isochoric","final_var":"T","final_value":500,"steps":100},
  {"type":"isothermal","final_var":"P","final_value":100000,"steps":120}
]
```
Command:
```bash
python thermo_simulator.py --n 1 --R 8.314 --P0 120000 --V0 0.02 --T0 350   --axes TV --processes examples/processes_example2.json --save plots/example2_TV.png
```

## 7) Troubleshooting
- Check final_var is allowed for the chosen type.
- Ensure SI units and steps >= 2.
- If image not saved, make sure the folder exists or supply `--save`.
