"""CellCheck concept media (TRL 3), generated from the parametric model.

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Axes: X across the front of the unit, Y from front (-Y) to back (+Y), Z up. The bench top is z = 0.
Geometry comes from cad/src/model.py, so the media match the STEP files and drawing CCK-DWG-001.
Key figures are printed by docs/04-calcs/sizing.py (CCK-CAL-001). BOM numbers match bom/bom.csv.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build123d import Box, Pos
from concept import Part, render_all
from model import build_parts


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


# the perforated guard is drawn see-through so the cells and holders under it stay visible
parts = [Part(n, shape, colour, bom, ex, 0.4 if bom == 5 else 1.0) for n, shape, colour, bom, ex in build_parts()]

bench = box(-500, 440, -215, 170, -30, 0)
laptop_pack = box(-100, 100, -205, -160, 0, 22)   # salvaged laptop pack in front of the tray
context = [Part("Bench top", bench, "#C8CDD3"), Part("salvaged laptop pack", laptop_pack, "#8B95A1")]

render_all(
    parts, project="CellCheck", title="Cell grader concept", dwg_no="CCK-DWG-010", date="2026-10-02",
    key_figures=["8 channels, 18650 and 21700 cells, four-wire contacts",
                 "1 A charge and 1 A discharge per channel",
                 "DC resistance: 0.5 A then 2.0 A pulse, IEC 61960 pattern",
                 "6.33 h per 1.8 Ah cell; 12.0 cells per 10 h day (calc.)",
                 "14-day self-discharge rest rack, 48 cells",
                 "33.6 W peak heat; MOSFET cases 59 C (calc.)",
                 "460 x 300 x 85 mm, 4.94 kg; $178 in parts (est.)"],
    scale_figure=False, context=context,
    cut=False,  # open-top bench unit: the hero and exploded views already show every internal part
    flow={"title": "material flow per 100 salvaged cells (all values are estimates)", "unit": "cells",
          "stages": [("Cells from packs", 100), ("Visual, voltage check", 91),
                     ("Capacity, resistance", 70), ("14-day rest check", 66),
                     ("Graded groups A, B, C", 66)],
          "losses": [(1, "Damaged or dead (est.)", 9), (2, "Weak, resistive, hot (est.)", 21),
                     (3, "Self-discharge (est.)", 4)]},
)
