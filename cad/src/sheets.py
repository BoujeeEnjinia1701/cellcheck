"""CellCheck general arrangement drawing CCK-DWG-001 (Rev P3, constructable design CCK-DDR-003, finger guards and sealed slots).

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
from model import PARAMS as P, assemblies, build_parts, envelope, n_fins, guard_extent  # noqa: E402

parts = build_parts()
asm = assemblies(parts)["cellcheck-assembly"]
work = ROOT / "cad/drawings/_views"
views = project_views(asm, work)
e = envelope()

s = Sheet(project="CellCheck", title="General arrangement, eight-channel grader", dwg_no="CCK-DWG-001",
          rev="P3", author="Amish Chadha", date="2026-10-02", concept=True,
          material="Tray 1.5 mm steel; plate 1.5 mm Al; heatsink Al; guard 0.8 mm perforated steel. See bom/bom.csv",
          revisions=[("P1", "Preliminary GA (CCK-CAL-001, CCK-DDR-001)", "2026-09-25", "AC"),
                     ("P2", "Constructable design: feet, standoffs, fixings (CCK-DDR-003)", "2026-10-01", "AC"),
                     ("P3", "Fan finger guards, silicone-sealed wire slots (CCK-DEC-001)", "2026-10-02", "AC")])
s.add_ortho(views, ["front", "top", "right"])
s.add_svg(views["iso"], 276, 30, 140, 84, label="Isometric view", sublabel="Not to scale; the cells sit under the perforated guard")
s.add_notes("Key dimensions and interfaces (mm)", [
    f"Unit envelope {e[1]-e[0]:.0f} x {e[3]-e[2]:.0f} x {e[5]-e[4]:.0f} on six {P['foot_h']:.0f} mm rubber feet",
    f"Tray {P['tray_t']} steel, liner {P['liner_t']:.0f}; plate {P['plate_t']} Al on six 12 mm standoffs",
    f"{P['n_ch']} channels at {P['pitch']:.0f} pitch, channel 1 at x {P['x0']:.0f}; cells along Y",
    f"Holders take 18650 and 21700 (to {P['cell_l']:.0f} long, {2*P['cell_r']:.0f} dia), four-wire",
    f"Guard {guard_extent()[1]-guard_extent()[0]:.0f} x {guard_extent()[3]-guard_extent()[2]:.0f} x {guard_extent()[5]-guard_extent()[4]:.1f}; two M4 thumb screws",
    f"Heatsink 320 x 36 x {P['fin_h']:.0f}: {n_fins()} fins at {P['fin_pitch']:.0f} pitch",
    "2 fans 60 mm, finger guards, on a folded shroud on the spine ends",
    "Fan intake slots 56 x 22 in tray back wall",
    "16 wire slots in the plate, silicone sealed",
    "12 V DC inlet only, 6.3 A fuse; 3 A fuse per cell",
    "Watchdog and 2.5 V comparator board (item 18)",
    "Rest rack (48 cells) and adapter stand beside the tray",
    "Mass about 4.94 kg without adapter (CCK-CAL-001)",
    "PRELIMINARY, NOT FOR FABRICATION",
], x=276, y=131, width=140)
s.save(ROOT / "cad/drawings/CCK-DWG-001")
shutil.rmtree(work, ignore_errors=True)
print("wrote cad/drawings/CCK-DWG-001.svg, .pdf, .png")
