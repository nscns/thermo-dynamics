# Thermo Sim (CHPE3102 Project)

A **ready-to-run** Python simulator for basic **closed-system** thermodynamic processes:
- **Isochoric** (constant volume)
- **Isobaric** (constant pressure)
- **Isothermal** (constant temperature)

Chain multiple processes **in any order** and plot **PV, TV, PT, VT, VP** diagrams.

> Assumes ideal-gas behavior (PV = nRT), closed system, quasi-static paths.

## Quick Start

1. Install Python 3.9+.
2. In this folder:
   ```bash
   pip install -r requirements.txt
   ```
3. Run an example:
   ```bash
   python thermo_simulator.py --n 1.0 --R 8.314      --P0 101325 --V0 0.024465 --T0 300      --axes PV --processes examples/processes_example1.json      --save plots/example1_PV.png
   ```

## Files
- `thermo_simulator.py` – main script (CLI)
- `examples/` – two ready-made process sequences
- `plots/` – output images (created on save)
- `USER_GUIDE.md` – ≤ 2 pages with 2 worked examples
- `requirements.txt`, `.gitignore`, `LICENSE`, `README.md`

## Upload to GitHub (fast)
- Create an empty repo on GitHub.
- Click **Add file → Upload files** and drag this whole folder.
- Commit.


## Interactive Mode (no JSON, no flags)
Run and answer prompts:
```bat
py -3 -m pip install -r requirements.txt
py -3 thermo_simulator_interactive.py
```
or double‑click `run_interactive.bat`. It will:
- Ask you for n, R, P0, V0, T0
- Ask how many steps and types (isothermal/isobaric/isochoric)
- Ask desired axes (PV/TV/PT/VT/VP)
- Save the plot (and optionally a JSON of your steps)

## How to get your GitHub link & share
- After you upload, the **repository link** is just the URL in your browser’s address bar, like:
  `https://github.com/<your-username>/<repo-name>`
- To share the **repo**, copy that URL and send it to your instructor.
- To share a **specific file**, click the file in GitHub and copy that page’s URL.
- To add collaborators: Repo **Settings → Collaborators and teams → Add people** (enter GitHub username/email).


## Super‑Simple Mode (only initial/final P,V,T)
No process selection, no JSON. It just connects the initial and final states with a straight path on the chosen axes.

**Run (Windows):**
- Double‑click `run_simple.bat`, or
- Use:
  ```bat
  py -3 -m pip install -r requirements.txt
  py -3 thermo_plot_simple.py
  ```
Output saved to `plots/simple_<AXES>.png`.


---

## Instructor Quick-Start (no input required)

**Assumptions (as required by the assignment):** ideal-gas behavior (PV = nRT), closed system (n constant), quasi‑static paths, SI units. The simulator lets you define multiple processes in order and plot PV/TV/PT/VT/VP diagrams【7†source】.

### One command (Codespaces / Linux / macOS)
```bash
bash run_all.sh
```
This installs requirements and generates **PV, TV, PT** plots for two built-in examples under `./plots`.

### One command (Windows)
Double-click `run_all.bat` (or run it in CMD).

### What gets produced
- `plots/example1_PV.png`, `plots/example1_TV.png`, `plots/example1_PT.png`
- `plots/example2_PV.png`, `plots/example2_TV.png`, `plots/example2_PT.png`
- Terminal prints the final **(P, V, T)** after each step for both examples.

### Where examples are defined
- `examples/processes_example1.json`
- `examples/processes_example2.json`

### Change initial conditions (optional)
Edit the top of `auto_run.py`:
```python
n  = 1.0
R  = 8.314
P0 = 101325.0
V0 = 0.024465
T0 = 300.0
```
Example 2 uses a second set: `P0b=120000.0`, `V0b=0.020`, `T0b=350.0`.

### Change the process sequence (optional)
Edit the JSON files above; the code supports three types:
- `isothermal` (final_var = P or V)
- `isobaric`   (final_var = T or V)
- `isochoric`  (final_var = T or P)

Each object also accepts `"steps"` for path resolution.

---
