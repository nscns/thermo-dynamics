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
