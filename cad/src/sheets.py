"""CellCheck general arrangement drawing CCK-DWG-001 (Rev P1).

Run from the repo root:  python cad/src/sheets.py
Builds cad/drawings/CCK-DWG-001.svg, .pdf and .png from the parametric model.
The concept sheet in media/ uses CCK-DWG-010, so DWG-001 is the first free number.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".kit"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drawing import Sheet, project_views  # noqa: E402
from model import PARAMS as P, assemblies, build_parts, envelope, n_fins  # noqa: E402

parts = build_parts()
asm = assemblies(parts)["cellcheck-assembly"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)
e = envelope()

s = Sheet(project="CellCheck", title="General arrangement, eight-channel grader", dwg_no="CCK-DWG-001",
          rev="P1", author="Amish Chadha", date="2026-09-25", concept=True,
          material="Tray 1.5 mm steel; plate 2 mm Al; heatsink Al; guard 0.8 mm perforated steel. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA (CCK-CAL-001, CCK-DDR-001)", "2026-09-25", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 84, label="Isometric view", sublabel="Not to scale; cells shown for reference")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Unit envelope {e[1]-e[0]:.0f} x {e[3]-e[2]:.0f} x {e[5]-e[4]:.0f}; tray {P['tray_t']} steel, liner {P['liner_t']:.0f}",
    f"{P['n_ch']} channels at {P['pitch']:.0f} pitch, channel 1 at x {P['x0']:.0f}; cells along Y at y {P['cell_y']:.0f}",
    f"Holders accept 18650 and 21700 (cell to {P['cell_l']:.0f} long, {2*P['cell_r']:.0f} dia)",
    "Four-wire contacts: force and sense at each cell end",
    f"Cell axis {P['plate_top'] + P['cell_axis_h']:.0f} above bench; guard top {P['plate_top'] + P['cell_axis_h'] + P['cell_r'] + P['guard_clear']:.1f}",
    f"Heatsink 320 x 36 x {P['fin_h']:.0f}: {n_fins()} fins at {P['fin_pitch']:.0f} pitch",
    "2 fans 60 mm on shroud, air into fins, out at top",
    "Fan intake slots 56 x 22 in tray back wall",
    "12 V DC inlet only, 6.3 A fuse; 3 A fuse per cell",
    "Watchdog and 2.5 V comparator board (item 18)",
    "Rest rack (48 cells) and adapter stand beside the tray",
    "Mass about 4.97 kg without adapter (CCK-CAL-001)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=131, width=140)
s.save(ROOT / "cad/drawings/CCK-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/CCK-DWG-001.svg, .pdf, .png")
