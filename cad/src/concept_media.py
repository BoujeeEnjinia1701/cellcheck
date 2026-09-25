"""CellCheck concept massing model and media (TRL 2).

Run from the repo root:  python cad/src/concept_media.py
Proportions and main parts only; not for fabrication.

Coordinates in mm: X across the front of the unit, Y from front (-Y) to back (+Y), Z up.
The bench top is at Z = 0. Eight test channels sit side by side at a 40 mm pitch; each channel
holds one 18650 or 21700 cell lying front to back in a four-wire (Kelvin) holder.
BOM numbers match bom/bom.csv.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".kit"))
from build123d import Box, Cylinder, Pos, Rot
from concept import Part, render_all

N_CH = 8                     # test channels
PITCH = 40.0                 # channel pitch along X
X0 = -170.0                  # X of channel 1
CH_X = [X0 + i * PITCH for i in range(N_CH)]
PLATE_Z = 15.0               # top face of the base plate
CELL_Y = -55.0               # cell holder centre in Y
CELL_R, CELL_L = 10.5, 70.0  # 21700 cell


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min and max corners."""
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


# 1 Steel tray (fire-resistant base), 460 x 300 x 45 mm, 1.5 mm walls, ceramic fibre liner inside
tray = box(-230, 230, -150, 150, 0, 45) - box(-228.5, 228.5, -148.5, 148.5, 1.5, 50)

# 2 Base plate (aluminium or FR4 carrier) on four standoffs resting on the tray floor
plate = box(-215, 215, -135, 135, PLATE_Z - 3, PLATE_Z)
for sx in (-200, 200):
    for sy in (-120, 120):
        plate = plate + Pos(sx, sy, (1.5 + PLATE_Z - 3) / 2) * Cylinder(5, PLATE_Z - 3 - 1.5)

# 3 Cell holders with four-wire spring contacts (groove for the cell, contact posts at each end)
CELL_Z = PLATE_Z + 20.0      # cell axis height
holders = []
for x in CH_X:
    body = box(x - 13, x + 13, CELL_Y - 42, CELL_Y + 42, PLATE_Z, PLATE_Z + 16)
    groove = Pos(x, CELL_Y, CELL_Z) * Rot(90, 0, 0) * Cylinder(CELL_R + 0.5, 76)
    posts = (box(x - 9, x + 9, CELL_Y - 42, CELL_Y - 36, PLATE_Z, CELL_Z + 10)
             + box(x - 9, x + 9, CELL_Y + 36, CELL_Y + 42, PLATE_Z, CELL_Z + 10))
    holders.append(body - groove + posts)
holders = union(holders)

# Cells under test (not supplied; shown for context), 21700 size, resting in the grooves
cells = union(Pos(x, CELL_Y, CELL_Z) * Rot(90, 0, 0) * Cylinder(CELL_R, CELL_L) for x in CH_X)

# 4 NTC thermistor clips, one on top of each cell
ntc = union(box(x - 4, x + 4, CELL_Y - 8, CELL_Y + 8, CELL_Z + CELL_R, CELL_Z + CELL_R + 5) for x in CH_X)

# 5 Perforated steel cell guard (drawn as a wire grid so the cells stay visible)
GX0, GX1 = CH_X[0] - 20, CH_X[-1] + 20
GY0, GY1 = CELL_Y - 50, CELL_Y + 50
GZ0, GZ1 = PLATE_Z, CELL_Z + CELL_R + 18
bar = 3.0
guard = []
for gx in (GX0, GX1):                                   # corner posts
    for gy in (GY0, GY1):
        guard.append(box(gx - bar / 2, gx + bar / 2, gy - bar / 2, gy + bar / 2, GZ0, GZ1))
for gy in (GY0, GY1):                                   # long top rails
    guard.append(box(GX0, GX1, gy - bar / 2, gy + bar / 2, GZ1 - bar, GZ1))
for gx in [GX0 + k * 20 for k in range(int((GX1 - GX0) / 20) + 1)]:   # cross bars on top
    guard.append(box(gx - 1, gx + 1, GY0, GY1, GZ1 - bar, GZ1))
for gy in (GY0, GY1):                                   # lower rails
    guard.append(box(GX0, GX1, gy - bar / 2, gy + bar / 2, GZ0, GZ0 + bar))
guard = union(guard)

# 6 Charger modules (1 A CC-CV buck chargers), one per channel, behind the holders
chargers = union(box(x - 12, x + 12, 5, 33, PLATE_Z, PLATE_Z + 9) for x in CH_X)

# 7 Channel sense and switch boards (INA226-class monitor, shunt, charge and load switches)
sense = union(box(x - 12, x + 12, 40, 62, PLATE_Z, PLATE_Z + 6) for x in CH_X)

# 9 Heatsink bar with fins, along the back
HS_Y0, HS_Y1 = 78.0, 108.0
heatsink = box(CH_X[0] - 20, CH_X[-1] + 20, HS_Y0, HS_Y0 + 6, PLATE_Z, PLATE_Z + 50)
for k in range(6):
    fy = HS_Y0 + 6 + k * 4.4
    heatsink = heatsink + box(CH_X[0] - 20, CH_X[-1] + 20, fy, fy + 1.6, PLATE_Z, PLATE_Z + 50)

# 8 Load MOSFETs (TO-220), bolted to the front face of the heatsink
mosfets = union(box(x - 5, x + 5, HS_Y0 - 4.5, HS_Y0, PLATE_Z + 14, PLATE_Z + 30)
                + box(x - 4, x + 4, HS_Y0 - 2, HS_Y0, PLATE_Z + 3, PLATE_Z + 14) for x in CH_X)

# 10 Two 60 mm fans on the back of the heatsink, blowing along the fins toward the back
fans = union(box(fx - 30, fx + 30, HS_Y1, HS_Y1 + 15, PLATE_Z, PLATE_Z + 60)
             - Pos(fx, HS_Y1 + 7.5, PLATE_Z + 30) * Rot(90, 0, 0) * Cylinder(27, 20)
             + Pos(fx, HS_Y1 + 7.5, PLATE_Z + 30) * Rot(90, 0, 0) * Cylinder(12, 13)
             for fx in (-110, 10))

# 11 Controller (ESP32-S3 class board) on the right
controller = box(150, 200, -10, 50, PLATE_Z, PLATE_Z + 12)

# 12 Display and buttons on a printed stand at the front right
display = (box(145, 205, -125, -113, PLATE_Z, PLATE_Z + 55)
           + box(150, 200, -127, -125, PLATE_Z + 18, PLATE_Z + 52))

# 13 Power inlet, main fuse and switch, rear right
inlet = box(150, 205, 80, 120, PLATE_Z, PLATE_Z + 28)

# 14 Certified 12 V 5 A mains adapter, on the bench to the right of the tray
adapter = box(270, 420, 20, 80, 0, 35)

# 15 Self-discharge rest rack (printed, 6 x 8 = 48 cells), on the bench to the left
RK_X1, RK_Y0 = -260.0, -80.0
RC = 26.0
rack = box(RK_X1 - 8 * RC - 8, RK_X1, RK_Y0, RK_Y0 + 6 * RC + 8, 0, 30)
rest_cells = []
for i in range(8):
    for j in range(6):
        cx, cy = RK_X1 - 4 - RC / 2 - i * RC, RK_Y0 + 4 + RC / 2 + j * RC
        rack = rack - Pos(cx, cy, 20) * Cylinder(CELL_R + 0.8, 25)
        if (i + j) % 3 != 1:
            rest_cells.append(Pos(cx, cy, 5 + CELL_L / 2) * Cylinder(CELL_R, CELL_L))
rest_cells = union(rest_cells)

parts = [
    Part("Steel tray with ceramic fibre liner", tray, "#6B7280", 1, (0, 0, -170)),
    Part("Base plate on standoffs", plate, "#D1D5DB", 2, (0, 0, -90)),
    Part("Cell holders, four-wire contacts", holders, "#374151", 3, (0, 0, 0)),
    Part("Cells under test (not supplied)", cells, "#A8B0BA", None, (0, 0, 70)),
    Part("NTC thermistor clips", ntc, "#C2410C", 4, (0, -40, 140)),
    Part("Perforated steel cell guard", guard, "#9CA3AF", 5, (0, -120, 240)),
    Part("Charger modules, 1 A CC-CV", chargers, "#0F766E", 6, (0, 40, 50)),
    Part("Channel sense and switch boards", sense, "#15803D", 7, (0, 80, 110)),
    Part("Load MOSFETs", mosfets, "#1F2937", 8, (0, 120, 170)),
    Part("Heatsink bar", heatsink, "#94A3B8", 9, (0, 190, 170)),
    Part("Fans, 60 mm", fans, "#4B5563", 10, (0, 280, 170)),
    Part("Controller, ESP32-S3 class", controller, "#D4A017", 11, (120, 0, 60)),
    Part("Display and buttons", display, "#38BDF8", 12, (130, -90, 40)),
    Part("Power inlet, fuse and switch", inlet, "#991B1B", 13, (140, 120, 40)),
    Part("12 V 5 A certified adapter", adapter, "#111827", 14, (220, 0, 0)),
    Part("Self-discharge rest rack, 48 cells", rack, "#E5E7EB", 15, (150, -470, 0)),
    Part("Cells resting (not supplied)", rest_cells, "#A8B0BA", None, (150, -470, 0)),
]

bench = box(-500, 440, -215, 170, -30, 0)
laptop_pack = box(-100, 100, -205, -160, 0, 22)   # salvaged laptop pack in front of the tray
context = [Part("Bench top", bench, "#C8CDD3"), Part("salvaged laptop pack", laptop_pack, "#8B95A1")]

render_all(
    parts, project="CellCheck", title="Cell grader concept", dwg_no="CCK-DWG-010",
    key_figures=["8 channels, 18650 and 21700 cells, four-wire contacts",
                 "1 A charge and 1 A discharge per channel (estimate)",
                 "DC resistance: 0.5 A then 2.0 A pulse, IEC 61960 pattern",
                 "About 6.5 h per cell; about 12 cells per 10 h day (est.)",
                 "14-day self-discharge rest rack, 48 cells",
                 "About 29 W heat at full discharge load (estimate)",
                 "About $159 in parts (indicative)"],
    scale_figure=False, context=context,
    cut=False,  # open-top bench unit: the hero and exploded views already show every internal part
    flow={"title": "material flow per 100 salvaged cells (all values are estimates)", "unit": "cells",
          "stages": [("Cells from packs", 100), ("Visual, voltage check", 91),
                     ("Capacity, resistance", 70), ("14-day rest check", 66),
                     ("Graded groups A, B, C", 66)],
          "losses": [(0, "Damaged or dead (est.)", 9), (1, "Weak, resistive, hot (est.)", 21),
                     (2, "Self-discharge (est.)", 4)]},
)
