"""CellCheck prototype build plan pictures (CCK-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|layouts|joints|steps|wiring ...]
With no argument it draws everything. Every picture is drawn from cad/src/model.py
(build_components), so the pictures and the model never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/CCK-DWG-101 to 110        making sketches for the made, cut and drilled components
    docs/05-build-plan/plate-holes.png     base plate hole and slot positions (matplotlib)
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/wiring.png          block-level wiring with wire sizes (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import (PARAMS as P, build_components, channel_x, heatsink_extent, guard_extent,  # noqa: E402
                   guard_studs, standoff_xy, _board_standoffs, _bay_screws, bx)

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-02"
F = P["foot_h"]
PZ = P["plate_top"] + F                  # plate top above the bench
C = build_components(P)
CX = channel_x(P)

COL = {"tray": "#6B7280", "liner": "#E7E5E4", "feet": "#111827", "standoffs": "#A16207", "plate": "#CBD5E1",
       "holders": "#374151", "cells": "#A8B0BA", "clips": "#C2410C", "guard": "#9CA3AF", "chargers": "#0F766E",
       "boards": "#15803D", "mosfets": "#1F2937", "heatsink": "#94A3B8", "shroud": "#64748B", "fans": "#334155",
       "ctrl": "#D4A017", "watchdog": "#DC2626", "buck": "#7C3AED", "stand": "#E2E8F0", "display": "#38BDF8",
       "inlet_house": "#991B1B", "inlet_parts": "#111827", "adapter": "#111827", "rack": "#E5E7EB",
       "rest": "#A8B0BA", "bolt": "#111827", "nylon": "#F5F5F4"}


def S(*ks):
    out = None
    for k in ks:
        out = C[k].shape if out is None else out + C[k].shape
    return out


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def win(sh, x0, x1, y0, y1, z0, z1):
    return sh & bx(x0, x1, y0, y1, z0, z1)


def bench(x0=-520, x1=460, y0=-230, y1=180):
    return part("Bench", bx(x0, x1, y0, y1, -12, 0), "#E5E7EB")


# ----------------------------------------------------------------- named components, in build order
def made():
    return {
        "tray": part("Steel tray, cut and drilled", S("tray"), COL["tray"]),
        "feet": part("Rubber feet with studs (6)", S("feet"), COL["feet"]),
        "standoffs": part("Hex standoffs (6)", S("standoffs"), COL["standoffs"]),
        "liner": part("Ceramic fibre liner", S("liner"), COL["liner"]),
        "plate": part("Base plate", S("plate"), COL["plate"]),
        "holders": part("Cell holders (8)", S("holders", "holder_screws"), COL["holders"]),
        "rivets": part("Rivet nuts (2)", S("rivet_nuts"), COL["bolt"]),
        "modules": part("Chargers and channel boards (8 each)", S("chargers", "boards", "board_standoffs"), COL["chargers"]),
        "mosfets": part("Load MOSFETs (8)", S("mosfets", "mosfet_screws"), COL["mosfets"]),
        "heatsink": part("Heatsink, drilled and tapped", S("heatsink", "hs_screws"), COL["heatsink"]),
        "shroud": part("Fan shroud", S("shroud", "shroud_screws"), COL["shroud"]),
        "fans": part("Fans with finger guards (2)", S("fans", "fan_screws", "fan_guards", "fan_guard_screws"), COL["fans"]),
        "seals": part("Silicone seals in the wire slots (16)", S("seals"), "#F59E0B"),
        "bay": part("Controller, watchdog board, 5 V converter", S("ctrl", "watchdog", "buck"), COL["ctrl"]),
        "display": part("Display stand and display", S("stand", "display"), COL["display"]),
        "inlet": part("Inlet housing, jack, fuse, switch", S("inlet_house", "inlet_parts", "bay_screws"), COL["inlet_house"]),
        "guard": part("Perforated guard and thumb screws", S("guard", "thumb_screws"), "#0E7490"),
        "clips": part("Thermistor clips (8)", S("clips"), COL["clips"]),
        "rack": part("Rest rack", S("rack"), COL["rack"]),
        "adapter": part("12 V adapter", S("adapter"), COL["adapter"]),
    }


ORDER = ["tray", "feet", "standoffs", "liner", "plate", "holders", "rivets", "modules", "mosfets", "heatsink",
         "shroud", "fans", "bay", "display", "inlet", "guard", "clips", "rack", "adapter"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"tray": (0, 0, -110), "feet": (0, 0, -210), "standoffs": (0, 0, 70), "liner": (0, 0, -30),
           "plate": (0, 0, 170), "holders": (0, 0, 230), "rivets": (0, -150, 150), "modules": (0, 30, 260),
           "mosfets": (0, 40, 300), "heatsink": (0, 90, 330), "shroud": (0, 170, 360), "fans": (0, 250, 380),
           "bay": (130, 0, 220), "display": (170, -150, 160), "inlet": (190, 120, 260), "guard": (-170, -330, 260),
           "clips": (0, -140, 300), "rack": (-60, -40, -60), "adapter": (90, 60, -60)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "CellCheck prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front right and above; the rest rack and adapter stand on the bench beside the tray",
                       elev=30, azim=-60, size=(11, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets():
    from build123d import Pos
    M = made()
    base = dict(project="CellCheck", date=DATE)
    down = lambda s: Pos(0, 0, -F) * s  # noqa: E731
    out = []
    hx0, hx1, hy0, hy1, *_ = heatsink_extent(P)
    gx0, gx1, gy0, gy1, gz0, gz1 = guard_extent(P)

    out.append(bv.component_sheet(
        Part("Steel tray", S("tray"), COL["tray"]), [M["liner"], M["plate"], M["feet"]],
        dwg_no="CCK-DWG-101", title="CellCheck steel tray (bought, cut and drilled): making sketch",
        material="Bought steel tray 460 x 300 x 45 mm, 1.5 mm wall", view_shape=down(S("tray")), inset_view=(30, -60),
        notes=["Buy a plain steel tray about 460 x 300 x 45 mm, 1.5 mm wall, with a flat",
               "  floor at least 457 x 297 mm inside. No plastic coating.",
               "Two fan intake slots in the back wall, 56 wide x 22 tall, from 20 to 42 mm",
               "  up from the floor, centred 110 mm left and 50 mm right of the centre.",
               "  Drill 6 mm in each corner, cut between with a hacksaw or nibbler, file.",
               "Six 4.5 mm holes in the floor for the foot studs, 124 mm each side of",
               "  the centre line front to back, at 210 mm left, 45 mm left and",
               "  120 mm right of centre. Measure from the centre lines you scribe.",
               "Deburr every cut edge inside and out; touch up bare steel with paint.",
               "Fit: a rubber foot under each hole; its stud goes up into a standoff.",
               "Check: the six holes match the base plate's corner holes when the plate",
               "  is laid on top, centred, before the liner goes in."], **base))

    out.append(bv.component_sheet(
        Part("Ceramic fibre liner", S("liner"), "#D6D3D1"), [M["tray"], M["standoffs"]],
        dwg_no="CCK-DWG-102", title="CellCheck ceramic fibre liner: making sketch",
        material="Ceramic fibre sheet 3 mm", view_shape=down(S("liner")), inset_view=(30, -60),
        notes=["Cut 457 x 297 mm from 3 mm ceramic fibre sheet with a sharp knife",
               "  and a steel rule; trim so it lies flat on the tray floor.",
               "Six 12 mm holes at the standoff positions (the same places as the",
               "  tray's stud holes): 124 mm each side front to back, at 210 left,",
               "  45 left and 120 right of centre. Cut with a 12 mm hole punch or knife.",
               "Wear a dust mask (FFP2 or N95), gloves and long sleeves; cut outdoors",
               "  or with dust extraction; wet-wipe the bench afterwards.",
               "Fit: lies loose on the floor round the standoffs, 2 mm clear of each.",
               "Check: no tears; the floor is covered except at the six holes."], **base))

    out.append(bv.component_sheet(
        Part("Base plate", S("plate"), COL["plate"]), [M["tray"], M["holders"], M["heatsink"], M["standoffs"]],
        dwg_no="CCK-DWG-103", title="CellCheck base plate: making sketch",
        material="Aluminium sheet 1.5 mm, 5052 or 6061 class", view_shape=down(S("plate")), inset_view=(30, -60),
        notes=["Blank 430 x 270 mm, 1.5 mm aluminium; round the corners to 3 mm.",
               "Measure every hole from the left edge and the front edge; the",
               "  hole layout picture in the build plan gives every position.",
               "Six 4.5 mm holes for the standoffs, 11 mm from the front and back.",
               "Per channel (eight channels, 40 mm apart, first at 45 mm from the left):",
               "  two 3.4 mm holder screw holes; a 16 x 5 mm wire slot behind the",
               "  holder and another between the charger and the channel board;",
               "  four 3.4 mm holes for the board standoffs.",
               "Two 6 mm holes for the guard rivet nuts; set M4 rivet nuts in them.",
               "Three 3.4 mm heatsink screw holes; 3.4 mm holes for the right-hand bay.",
               "Slots: drill 5 mm at each end, cut between, file; fit edge grommet strip.",
               "  After wiring, each slot is filled with silicone round the leads.",
               "Check: lay the holders and heatsink on it and look through each hole."], **base))

    out.append(bv.component_sheet(
        Part("Heatsink", S("heatsink"), COL["heatsink"]), [M["plate"], M["mosfets"], M["shroud"]],
        dwg_no="CCK-DWG-104", title="CellCheck heatsink (bought, drilled and tapped): making sketch",
        material="Aluminium finned heatsink 320 x 36 x 50 mm", view_shape=down(S("heatsink")), inset_view=(30, -60),
        notes=["Bought: a 6 mm spine 320 x 50 mm with 40 fins 30 mm deep at 8 mm pitch.",
               "MOSFET holes: eight M3 tapped holes through the spine (drill 2.5),",
               "  26.5 mm up from the bottom edge, 20 mm from the left end and then",
               "  every 40 mm, each midway between two fins. Deburr the front face flat.",
               "Plate screws: three M3 tapped holes 10 mm deep in the bottom edge,",
               "  centred in the spine's 6 mm thickness, 40, 160 and 280 mm from the left end.",
               "Shroud screws: two M3 tapped holes 8 mm deep in each end of the spine,",
               "  centred in its thickness, 15 and 35 mm up from the bottom edge.",
               "Use cutting fluid; back the tap out often; the walls are thin.",
               "Fit: stands on the plate, fins to the back; MOSFETs on the smooth face.",
               "Check: an M3 screw runs freely into every hole."], **base))

    out.append(bv.component_sheet(
        Part("Fan shroud", S("shroud"), COL["shroud"]), [M["heatsink"], M["fans"], M["plate"]],
        dwg_no="CCK-DWG-105", title="CellCheck fan shroud: making sketch",
        material="Aluminium sheet 1 mm", view_shape=down(S("shroud")), inset_view=(30, 55),
        notes=["One blank 322 x 60 mm back with a 39 x 50 mm flange on each end.",
               "Two 54 mm fan holes, centred 30 mm up, 81 mm and 241 mm from the",
               "  left end of the back; cut with a hole saw or step drill.",
               "Fan screw holes 3.4 mm on a 50 mm square round each fan hole.",
               "Fold each end flange 90 degrees forward, square to the back.",
               "Two 3.4 mm holes in each flange, 3 mm from the free end (in line",
               "  with the spine), 15 and 35 mm up from the bottom edge.",
               "Fit the fans to the back first, screws from the inside; each fan",
               "  gets a 60 mm finger guard on its outer face (four small screws).",
               "Fit: the flanges lie on the spine ends; the back stands 3 mm",
               "  behind the fins; the bottom edge rests on the plate.",
               "Check: the flange holes line up with the tapped holes in the spine."], **base))

    dx0, dx1, dy0, dy1, dh = P["display"]
    out.append(bv.component_sheet(
        Part("Display stand", S("stand"), "#CBD5E1"), [M["plate"], M["display"], M["guard"]],
        dwg_no="CCK-DWG-106", title="CellCheck display stand: making sketch",
        material="PETG, 3D printed, 40 % infill", view_shape=down(S("stand")), inset_view=(30, 50),
        notes=[f"Print: a foot {dx1 - dx0:.0f} x {dy1 - dy0:.0f} x 5 mm and an upright {dx1 - dx0:.0f} x 8 x {dh:.0f} mm,",
               "  15 mm back from the foot's front edge, printed lying on its back.",
               "Window 64 x 28 mm in the upright, 22 mm up, for the display's pins.",
               "Two 3 mm pilot holes in the foot, 6 mm in from each end and 7 mm",
               "  from the front, for M3 screws from under the plate.",
               "Three 7 mm holes in the foot's front strip, 25 mm apart, for the",
               "  panel-mount push buttons, held by their nuts.",
               "Fit: the display module screws to the upright's front face with its",
               "  four corner holes (M2.5 or M3 self-tappers).",
               "Check: the 86 x 50 mm display board sits flat on the upright."], **base))

    ix0, ix1, iy0, iy1, ih = P["inlet"]
    out.append(bv.component_sheet(
        Part("Inlet housing", S("inlet_house"), COL["inlet_house"]), [M["plate"], M["bay"]],
        dwg_no="CCK-DWG-107", title="CellCheck inlet housing: making sketch",
        material="PETG, 3D printed, 2 mm walls", view_shape=down(S("inlet_house")), inset_view=(30, -40),
        notes=[f"Print an open-bottomed box {ix1 - ix0:.0f} x {iy1 - iy0:.0f} x {ih:.0f} mm, 2 mm walls, top up.",
               "Top face: DC jack hole 11.2 mm; fuse holder hole 12 mm;",
               "  rocker switch cut-out 12 x 16 mm (check each against its datasheet).",
               "Wire exit notch 20 x 8 mm at the bottom of the front wall.",
               "Two screw bosses inside, 6 mm in from opposite corners, 3 mm pilot",
               "  holes for M3 screws from under the plate.",
               "Fit: jack, fuse holder and switch go in from the top, nuts inside.",
               "The adapter lead comes over the tray's right rim into the jack.",
               "Check: each part snaps or screws in square; nothing rocks."], **base))

    out.append(bv.component_sheet(
        Part("Perforated guard", S("guard"), COL["guard"]), [M["plate"], M["holders"], M["rivets"]],
        dwg_no="CCK-DWG-108", title="CellCheck perforated guard: making sketch",
        material="Perforated steel sheet 0.8 mm, about 50 % open", view_shape=down(S("guard")), inset_view=(30, -60),
        notes=[f"One blank: top {gx1 - gx0:.0f} x {gy1 - gy0:.0f} mm in the middle; front and back",
               f"  {gx1 - gx0:.0f} x {gz1 - gz0:.1f} mm; ends {gy1 - gy0:.0f} x {gz1 - gz0:.1f} mm, each with an",
               f"  {P['guard_flange']:.0f} mm flange; 12 mm tabs on the ends of the front and back.",
               "Cut with aviation snips; drill 3 mm relief holes where folds cross.",
               "Fold the front, back and ends down 90 degrees; fold the tabs round",
               "  the corners and rivet each with two 3.2 mm steel rivets.",
               "Fold each end flange 90 degrees outward, flat with the bottom edge.",
               "One 10 mm hole in each flange, 10 mm out from the end wall, central.",
               "File every cut edge smooth; wear cut-resistant gloves.",
               "Fit: open bottom on the plate over the holders; two M4 knurled thumb",
               "  screws through the flanges into rivet nuts in the plate.",
               "Check: it sits flat with no gap under any wall."], **base))

    clip0 = S("clips") & bx(CX[0] - 20, CX[0] + 20, -200, 200, -10, 200)
    out.append(bv.component_sheet(
        Part("Thermistor clip", clip0, COL["clips"]), [part("Cell", S("cells") & bx(CX[0] - 20, CX[0] + 20, -200, 200, -10, 200), COL["cells"]),
                                                      part("Holder", S("holders") & bx(CX[0] - 20, CX[0] + 20, -200, 200, -10, 200), COL["holders"])],
        dwg_no="CCK-DWG-109", title="CellCheck thermistor clip (print 8 for 21700, 8 for 18650): making sketch",
        material="PETG, 3D printed, 100 % infill", view_shape=Pos(-CX[0], -P["cell_y"], -(PZ + P["cell_axis_h"])) * clip0,
        inset_view=(25, -35),
        notes=["A C-shaped ring 10 mm long, 1.6 mm wall, that springs over the top",
               "  of the cell and wraps 10 degrees past its sides on each side.",
               "21700 clip: 21.0 mm inside. 18650 clip: 18.3 mm inside.",
               "Raised pad on top, 7 x 10 mm and 3 mm high, with a 2 mm hole down",
               "  through it for the thermistor bead, which touches the cell;",
               "  a dab of thermal paste between bead and cell.",
               "Print with the ring's axis vertical; no supports.",
               "Fit: push down over the cell between the holder's contact posts;",
               "  the lower edges stay at least 2 mm above the holder.",
               "Check: it grips the cell and does not slide when the lead is tugged."],
        **base))

    out.append(bv.component_sheet(
        Part("Rest rack", S("rack"), "#CBD5E1"), [M["tray"], M["guard"], M["adapter"], part("Cells resting", S("rest"), COL["rest"])],
        dwg_no="CCK-DWG-110", title="CellCheck rest rack (48 cells): making sketch",
        material="PETG or PLA, 3D printed, 20 % infill", inset_view=(35, -60),
        notes=["Print a block 216 x 164 x 30 mm (needs a bed of 220 x 170 mm or more).",
               "48 pockets 22.6 mm across and 25 mm deep, 8 columns x 6 rows at 26 mm",
               "  pitch, starting 17 mm in from each edge.",
               "Number the columns 1 to 8 and the rows A to F (print or label).",
               "Fit: stands on the bench to the left of the tray; cells stand upright,",
               "  label up, positive end up.",
               "Check: an 18650 and a 21700 each drop in and lift out freely."], **base))
    return out


# ----------------------------------------------------------------- plate hole layout
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle, Circle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    pl, pw = P["plate_l"] / 2, P["plate_w"] / 2
    X = lambda x: x + pl  # noqa: E731  from the left edge
    Y = lambda y: y + pw  # noqa: E731  from the front edge
    groups = [  # (label, colour, [(x, y)], diameter or (w, h))
        ("Standoff screws, 4.5", "#A16207", standoff_xy(P), 4.5),
        ("Holder screws, 3.4", INK, [(x, P["cell_y"] + s * P["holder_screw_dy"]) for x in CX for s in (-1, 1)], 3.4),
        ("Board standoff screws, 3.4", "#15803D", _board_standoffs(P), 3.4),
        ("Heatsink screws, 3.4", "#334155", [(x, P["hs_y0"] + P["spine_t"] / 2) for x in P["hs_screw_x"]], 3.4),
        ("Display and inlet screws, 3.4", "#991B1B", _bay_screws(P), 3.4),
        ("Rivet nuts, 6.0", "#2563EB", guard_studs(P), 6.0),
    ]
    fig = plt.figure(figsize=(12, 8.6), dpi=150)
    ax = fig.add_axes([0.06, 0.08, 0.66, 0.82]); ax.set_aspect("equal"); ax.set_axis_off()
    ax.add_patch(Rectangle((0, 0), 2 * pl, 2 * pw, fc="#F1F5F9", ec=INK, lw=1.2))
    gx0, gx1, gy0, gy1, *_ = guard_extent(P)
    ax.add_patch(Rectangle((X(gx0), Y(gy0)), gx1 - gx0, gy1 - gy0, fc="none", ec=MUT, lw=0.6, ls="--"))
    ax.text(X(gx0) + 3, Y(gy0) + 3, "guard footprint", fontsize=6.5, color=MUT)
    hx0, hx1, hy0, hy1, *_ = heatsink_extent(P)
    ax.add_patch(Rectangle((X(hx0), Y(hy0)), hx1 - hx0, hy1 - hy0, fc="none", ec=MUT, lw=0.6, ls="--"))
    ax.text(X(hx0) + 3, Y(hy1) - 7, "heatsink footprint", fontsize=6.5, color=MUT)
    for name, col, pts, d in groups:
        for x, y in pts:
            ax.add_patch(Circle((X(x), Y(y)), d / 2 + 0.6, fc="white", ec=col, lw=1.2))
    sw, sd = P["slot_w"], P["slot_d"]
    for x in CX:
        for yc in (P["down_slot_y"], P["up_slot_y"]):
            ax.add_patch(Rectangle((X(x) - sw / 2, Y(yc) - sd / 2), sw, sd, fc="#FDE68A", ec="#7C3AED", lw=1.2))
    # channel centre lines and their positions from the left edge
    for i, x in enumerate(CX):
        ax.plot([X(x), X(x)], [0, 2 * pw], color=AC, lw=0.4, ls=(0, (6, 3)))
        ax.text(X(x), -8, f"{X(x):g}", ha="center", va="top", fontsize=7.5, color=AC)
        ax.text(X(x), 2 * pw + 3, f"ch {i + 1}", ha="center", va="bottom", fontsize=7, color=AC)
    ax.text(2 * pl / 2 - 40, -22, "channel centre lines, mm from the left edge", ha="center", fontsize=8, color=MUT)
    # per-channel heights from the front edge, on channel 1
    ys = sorted({round(Y(P["cell_y"] + s * P["holder_screw_dy"]), 1) for s in (-1, 1)}
                | {round(Y(y), 1) for _, y in _board_standoffs(P)[:4]}
                | {round(Y(P["down_slot_y"]), 1), round(Y(P["up_slot_y"]), 1)})
    for i, y in enumerate(ys):
        xl = -8 - 22 * (i % 2)
        ax.plot([xl + 2, X(CX[0]) - 10], [y, y], color=AC, lw=0.35, ls=":")
        ax.text(xl, y, f"{y:g}", ha="right", va="center", fontsize=7.5, color=AC)
    ax.text(-52, pw, "per-channel heights, mm from the front edge", rotation=90, ha="center", va="center", fontsize=8, color=MUT)
    ax.set_xlim(-60, 2 * pl + 6); ax.set_ylim(-30, 2 * pw + 14)
    fig.text(0.03, 0.975, "Base plate: hole and slot positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.945, "Seen from above, front edge at the bottom. Measured from the left edge (x) and the front edge (y), mm, taken from the model.",
             fontsize=8.5, color=MUT, va="top")
    # key with every position that is not repeated per channel
    k = ["Every channel (8, at the centre lines):",
         "  holder screws: on the line, 55 and 105 up",
         "  wire slot 16 x 5 behind the holder, 125.5 up",
         "  wire slot 16 x 5, 171.5 up",
         "  (both slots filled with silicone after wiring)",
         "  charger standoffs: 9 left at 143, 9 right at 165",
         "  board standoffs: 9 left at 178, 9 right at 194",
         "",
         "Other holes (x from left, y from front):"]
    lbl = {"Standoff screws, 4.5": "Standoffs 4.5", "Heatsink screws, 3.4": "Heatsink 3.4",
           "Display and inlet screws, 3.4": "Display, inlet 3.4", "Rivet nuts, 6.0": "Rivet nuts 6.0"}
    for name, col, pts, d in groups:
        if name in lbl:
            xs = sorted({X(x) for x, _ in pts}); yy = sorted({Y(y) for _, y in pts})
            k.append(f"  {lbl[name]}: x {', '.join(f'{v:g}' for v in xs)}")
            k.append(f"      y {', '.join(f'{v:g}' for v in yy)}" + ("  (pairs as drawn)" if name.startswith("Display") else ""))
    bay = [(x, y) for x, y in _board_standoffs(P)[32:]]
    k.append("  Bay standoffs 3.4 (controller, watchdog,")
    k.append("      converter): " + "; ".join(f"{X(x):g}, {Y(y):g}" for x, y in bay[:3]))
    k.append("      " + "; ".join(f"{X(x):g}, {Y(y):g}" for x, y in bay[3:]))
    k.append("")
    k.append("Colour of each ring: what goes through it")
    fig.text(0.735, 0.88, "What each opening is (mm)", fontsize=9, fontweight="bold", color=INK, va="top")
    for i, t in enumerate(k):
        fig.text(0.735, 0.85 - i * 0.024, t, fontsize=7.6, color=INK, va="top")
    y0 = 0.85 - len(k) * 0.024 - 0.01
    for i, (name, col, _, _) in enumerate(groups + [("Wire slots 16 x 5, silicone sealed", "#7C3AED", [], 0)]):
        fig.patches.append(plt.Circle((0.745, y0 - i * 0.024), 0.005, transform=fig.transFigure, fc="white", ec=col, lw=1.4))
        fig.text(0.758, y0 - i * 0.024, name, fontsize=7.6, color=INK, va="center")
    fig.text(0.03, 0.015, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.015, "github.com/BoujeeEnjinia1701/cellcheck", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "plate-holes.png", facecolor="white"); plt.close(fig)
    return OUT / "plate-holes.png"


# ----------------------------------------------------------------- joints
def joints():
    out = []
    x, y = standoff_xy(P)[0]
    box_ = (x - 18, x + 18, y - 14, y + 14, -1, PZ + 6)
    out.append(bv.joint([
        part("Rubber foot and its M4 stud", win(S("feet"), *box_), "#78716C"),
        part("Tray floor", win(S("tray"), *box_), COL["tray"]),
        part("Ceramic fibre liner", win(S("liner"), *box_), "#D6D3D1"),
        part("Hex standoff, 12 mm", win(S("standoffs"), *box_), COL["standoffs"]),
        part("Base plate", win(S("plate"), *box_), COL["plate"]),
        part("M4 screw from the top", win(S("plate_screws"), *box_), COL["bolt"])],
        OUT / "joint-01.png", "Joint 1: foot, tray floor, standoff and base plate (cut through the standoff)",
        subtitle="The foot's stud goes up through the floor into the standoff; the plate screws down into its top",
        cut="+Y", elev=12, azim=-80, size=(8, 6)))
    x = CX[0]
    box_ = (x - 22, x + 22, -112, 0, PZ - 12, PZ + 50)
    out.append(bv.joint([
        part("Base plate (wire slot behind the holder)", win(S("plate"), *box_), COL["plate"]),
        part("Cell holder", win(S("holders"), *box_), COL["holders"]),
        part("M3 screws from under the plate", win(S("holder_screws"), *box_), COL["bolt"]),
        part("Cell (21700 shown)", win(S("cells"), *box_), COL["cells"]),
        part("Thermistor clip", win(S("clips"), *box_), COL["clips"]),
        part("Guard", win(S("guard"), *box_), COL["guard"])],
        OUT / "joint-02.png", "Joint 2: holder, cell, thermistor clip and guard (cut along channel 1)",
        subtitle="The cell rests in the holder and touches the contacts at both ends; the guard stands clear all round",
        cut="-X", elev=15, azim=-30, size=(8, 6)))
    hx0, hx1, hy0, hy1, *_ = heatsink_extent(P)
    x = CX[0]
    box_ = (x - 14, x + 14, hy0 - 10, hy1 + 2, PZ - 4, PZ + 52)
    out.append(bv.joint([
        part("Heatsink spine and fins", win(S("heatsink"), *box_), COL["heatsink"]),
        part("Load MOSFET, insulating pad behind", win(S("mosfets"), *box_), "#B45309"),
        part("M3 screw and shoulder washer", win(S("mosfet_screws"), *box_), COL["bolt"]),
        part("Base plate", win(S("plate"), *box_), COL["plate"])],
        OUT / "joint-03.png", "Joint 3: load MOSFET on the heatsink (cut through channel 1)",
        subtitle="Tab flat on the spine with an insulating pad; one M3 screw into a tapped hole between two fins",
        cut="-X", elev=12, azim=-20, size=(8, 6)))
    box_ = (hx0 - 6, hx0 + 125, hy0 - 4, hy1 + 26, PZ - 2, PZ + 64)
    out.append(bv.joint([
        part("Heatsink", win(S("heatsink"), *box_), COL["heatsink"]),
        part("Shroud side flange and back", win(S("shroud"), *box_), "#60A5FA"),
        part("Two M3 screws into the spine end", win(S("shroud_screws"), *box_), COL["bolt"]),
        part("Fan, screwed from inside the shroud", win(S("fans"), *box_), COL["fans"]),
        part("Finger guard on the fan's outer face", win(S("fan_guards", "fan_guard_screws"), *box_), "#B8BEC6"),
        part("Base plate", win(S("plate"), *box_), COL["plate"])],
        OUT / "joint-04.png", "Joint 4: fan shroud on the left end of the heatsink",
        subtitle="Seen from behind on the left. The flange lies on the spine end; the back stands 3 mm behind the fins; the guard covers the fan",
        elev=26, azim=45, size=(8, 6)))
    (sx, sy), _ = guard_studs(P)
    box_ = (sx - 12, sx + 16, sy - 16, sy + 16, PZ - 10, PZ + 20)
    out.append(bv.joint([
        part("Base plate", win(S("plate"), *box_), COL["plate"]),
        part("M4 rivet nut set in the plate", win(S("rivet_nuts"), *box_), "#B45309"),
        part("Guard end flange (10 mm hole)", win(S("guard"), *box_), COL["guard"]),
        part("M4 knurled thumb screw", win(S("thumb_screws"), *box_), COL["bolt"])],
        OUT / "joint-05.png", "Joint 5: guard flange held by a thumb screw (cut through the left screw)",
        subtitle="The flange lies flat on the plate; the thumb screw clamps it to the rivet nut. Undo two to lift the guard",
        cut="+Y", elev=15, azim=-75, size=(8, 6)))
    x = CX[0]
    box_ = (x - 16, x + 16, 0, 66, PZ - 3, PZ + 16)
    out.append(bv.joint([
        part("Base plate (wire slot between the boards)", win(S("plate"), *box_), COL["plate"]),
        part("Nylon standoffs, 5 mm", win(S("board_standoffs"), *box_), "#E7E5E4"),
        part("Charger module", win(S("chargers"), *box_), COL["chargers"]),
        part("Channel board", win(S("boards"), *box_), COL["boards"]),
        part("Silicone seal in the slot", win(S("seals"), *box_), "#F59E0B")],
        OUT / "joint-06.png", "Joint 6: charger and channel board on their standoffs (channel 1)",
        subtitle="Each board stands 5 mm off the plate on two nylon standoffs; the cell leads come up through the slot, which is sealed with silicone",
        elev=30, azim=-50, size=(8, 6)))
    ix0, ix1, iy0, iy1, ih = P["inlet"]
    box_ = (ix0 - 4, ix1 + 4, iy0 - 4, iy1 + 4, PZ - 3, PZ + ih + 14)
    out.append(bv.joint([
        part("Base plate", win(S("plate"), *box_), COL["plate"]),
        part("Inlet housing", win(S("inlet_house"), *box_), COL["inlet_house"]),
        part("DC jack, fuse holder, rocker switch", win(S("inlet_parts"), *box_), COL["inlet_parts"]),
        part("M3 screws from under the plate", win(S("bay_screws"), *box_), COL["bolt"])],
        OUT / "joint-07.png", "Joint 7: power inlet (housing cut open)",
        subtitle="Jack, fuse holder and switch fit from the top with their nuts inside; the housing screws to the plate",
        cut="+Y", elev=25, azim=-60, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps():
    M = made()
    out = []

    def st(n, done, new, title, sub, **kw):
        out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)

    st(1, [M["tray"]], [mv(M["feet"], (0, 0, -70)), mv(M["standoffs"], (0, 0, 90))],
       "feet and standoffs onto the tray",
       "Each foot's stud up through the floor into a standoff; hand tight plus a quarter turn",
       elev=28, azim=-60, label_done=True)
    st(2, [M["tray"], M["feet"], M["standoffs"]], [mv(M["liner"], (0, 0, 90))],
       "liner into the tray", "Lay it flat over the standoffs; it is not fixed", elev=28, azim=-60, label_done=False)
    st(3, [M["plate"]], [mv(M["holders"], (0, 0, 60)), mv(M["rivets"], (0, 0, 40))],
       "holders and rivet nuts onto the base plate",
       "Two M3 screws per holder from under the plate; set the two M4 rivet nuts with the hand tool",
       elev=30, azim=-60, label_done=True)
    st(4, [M["plate"], M["holders"], M["rivets"]], [mv(M["modules"], (0, 0, 60))],
       "chargers and channel boards onto the plate",
       "Each on two 5 mm nylon standoffs, M3 screws from under the plate; no wiring yet",
       elev=30, azim=-60, label_done=False)
    st(5, [part("Heatsink", S("heatsink"), COL["heatsink"])], [mv(M["mosfets"], (0, -50, 0))],
       "MOSFETs onto the heatsink",
       "Insulating pad under each tab; M3 screw with a shoulder washer, snug; check isolation with a meter",
       elev=20, azim=-60, label_done=True)
    hs = part("Heatsink with MOSFETs", S("heatsink", "hs_screws", "mosfets", "mosfet_screws"), COL["heatsink"])
    on_plate = [M["plate"], M["holders"], M["rivets"], M["modules"]]
    st(6, on_plate, [mv(hs, (0, 0, 70))], "heatsink onto the plate",
       "Fins to the back; three M3 screws up from under the plate into the spine", elev=30, azim=-60, label_done=False)
    st(7, on_plate + [hs], [mv(part("Shroud with fans", S("shroud", "shroud_screws", "fans", "fan_screws", "fan_guards", "fan_guard_screws"), COL["shroud"]), (0, 90, 0))],
       "fan shroud and fans onto the heatsink",
       "Seen from behind. Fans (with their finger guards) screwed to the shroud first, from inside; then two M3 screws into each spine end", elev=30, azim=55, label_done=False)
    fan = part("Shroud with fans", S("shroud", "shroud_screws", "fans", "fan_screws", "fan_guards", "fan_guard_screws"), COL["shroud"])
    st(8, on_plate + [hs, fan], [mv(part("Controller, watchdog board, 5 V converter", S("ctrl", "watchdog", "buck"), COL["ctrl"]), (0, 0, 60)),
                                 mv(M["display"], (0, -40, 50)), mv(M["inlet"], (0, 30, 60))],
       "controller, watchdog board, converter, display and inlet",
       "Boards on 5 mm nylon standoffs; display stand and inlet housing by two M3 screws each from under the plate",
       elev=30, azim=-60, label_done=False)
    full_plate = part("Base plate with everything on it", S("plate", "holders", "holder_screws", "rivet_nuts", "chargers", "boards", "board_standoffs",
                                                           "heatsink", "hs_screws", "mosfets", "mosfet_screws", "shroud", "shroud_screws", "fans",
                                                           "fan_screws", "fan_guards", "fan_guard_screws", "ctrl", "watchdog", "buck", "stand", "display",
                                                           "inlet_house", "inlet_parts", "bay_screws", "seals"), "#3B82F6")
    plate_wired = part("Base plate with everything on it", S("plate", "holders", "holder_screws", "rivet_nuts", "chargers", "boards",
                                                            "board_standoffs", "heatsink", "hs_screws", "mosfets", "mosfet_screws",
                                                            "shroud", "shroud_screws", "fans", "fan_screws", "fan_guards",
                                                            "fan_guard_screws", "ctrl", "watchdog", "buck", "stand", "display",
                                                            "inlet_house", "inlet_parts", "bay_screws"), "#94A3B8")
    st(9, [plate_wired], [mv(M["seals"], (0, 0, 70))], "wire slots sealed with silicone",
       "After wiring, each of the 16 slots is filled round its leads from above and below and left to cure; the leads are not drawn",
       elev=48, azim=-60, size=(9, 6.5), label_done=False)
    tray_done = [M["tray"], M["feet"], M["standoffs"], M["liner"]]
    st(10, tray_done, [mv(full_plate, (0, 0, 120)), mv(part("Six M4 screws", S("plate_screws"), COL["bolt"]), (0, 0, 170))],
       "plate assembly into the tray",
       "Lower it on to the six standoffs with no wire trapped; six M4 screws from the top", elev=30, azim=-60, label_done=True)
    unit = tray_done + [full_plate, part("Plate screws", S("plate_screws"), COL["bolt"])]
    st(11, unit, [mv(M["guard"], (0, 0, 90))], "guard over the cell holders",
       "Open bottom down, flanges over the rivet nuts; two thumb screws, finger tight", elev=30, azim=-60, label_done=False)
    st(12, unit + [M["guard"]], [mv(part("Rest rack", S("rack"), "#14B8A6"), (-70, 0, 0)), mv(M["adapter"], (50, 0, 0))],
       "rest rack and adapter on the bench",
       "Rack to the left of the tray; certified adapter to the right, its lead over the tray rim into the jack",
       context=[bench()], elev=30, azim=-60, label_done=False)
    return out


# ----------------------------------------------------------------- wiring
def wiring():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch
    fig = plt.figure(figsize=(12, 7.6), dpi=150)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 120); ax.set_ylim(0, 76); ax.set_axis_off()
    INK, MUT = "#111827", "#4B5563"
    ax.text(2, 74, "CellCheck prototype: block-level wiring (one channel of eight shown)", fontsize=13, fontweight="bold", color=INK, va="top")
    ax.text(2, 70.6, "Bought modules and small perfboards wired at block level; no circuit board is laid out. Stranded or silicone copper wire; ferrules on screw terminals.",
            fontsize=8.5, color=MUT, va="top")
    ax.text(2, 1.5, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    ax.text(118, 1.5, "github.com/BoujeeEnjinia1701/cellcheck", fontsize=7, color="#0F766E", ha="right", family="monospace")
    ax.add_patch(FancyBboxPatch((2, 13), 63, 50, boxstyle="round,pad=0.4", fc="#F8FAFC", ec="#94A3B8", lw=1, ls="--"))
    ax.text(3.5, 61.8, "Repeated for each of the 8 channels", fontsize=8, color=MUT, va="top")

    def blk(x, y, w, h, title, sub, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3", fc="white", ec=color, lw=1.8))
        ax.text(x + w / 2, y + h - 1.3, title, ha="center", va="top", fontsize=8.6, fontweight="bold", color=INK)
        ax.text(x + w / 2, y + h - 4.0, sub, ha="center", va="top", fontsize=7, color=MUT, linespacing=1.3)

    def wire(pts, color, lw=2.0):
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=1)

    def lab(x, y, text, color, ha="left"):
        ax.text(x, y, text, fontsize=7, color=color, ha=ha, va="center", zorder=3,
                bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    RED, BLU, GRY, BLK = "#B91C1C", "#1D4ED8", "#6B7280", "#111827"
    # shared blocks, right
    blk(100, 12, 16, 9, "12 V adapter", "certified, 60 W", BLK)
    blk(100, 28, 16, 11, "Power inlet", "DC jack, 6.3 A fuse,\nrocker switch", "#991B1B")
    blk(100, 46, 16, 11, "5 V converter", "12 V in, 5 V 3 A out", "#7C3AED")
    blk(78, 46, 16, 14, "Controller", "ESP32-S3 class,\nmicroSD, display,\nthermistor inputs", "#D4A017")
    blk(78, 28, 16, 12, "Watchdog board", "gates every enable;\n2.5 V comparators", "#DC2626")
    blk(78, 12, 16, 9, "Fans (2)", "12 V; tachometer\nto the controller", "#334155")
    # channel blocks, left
    blk(5, 44, 17, 12, "Charger module", "1 A CC-CV, 4.20 V", "#0F766E")
    blk(27, 38, 30, 18, "Channel board", "current monitor and shunt,\ncharge switch, op-amp\nload loop, 3 A fuse clip", "#15803D")
    blk(5, 16, 17, 14, "Cell holder", "force and sense\nat each end;\nthermistor clip", "#374151")
    blk(37, 16, 18, 11, "Load MOSFET", "on the heatsink,\ninsulated tab", "#1F2937")
    # power
    wire([(108, 21), (108, 28)], RED); lab(108.6, 24.5, "12 V lead", RED)
    wire([(108, 39), (108, 46)], RED, 1.4); lab(108.6, 42.5, "12 V, 0.5 mm²", RED)
    wire([(100, 31), (97, 31), (97, 17), (94, 17)], RED, 1.4); lab(96.4, 24, "12 V,\n0.25 mm²", RED, "right")
    wire([(100, 36), (98, 36), (98, 65), (13.5, 65), (13.5, 56)], RED)
    lab(45, 65, "12 V bus to all eight chargers, 1.0 mm² (0.5 mm² drops)", RED, "center")
    wire([(100, 52), (94, 52)], RED, 1.4); lab(97.4, 54, "5 V", RED, "right")
    wire([(108, 57), (108, 67.5), (42, 67.5), (42, 56)], RED, 1.4); lab(75, 67.5, "5 V to the channel boards and display, 0.5 mm²", RED, "center")
    wire([(22, 50), (27, 50)], RED); lab(24.5, 52.6, "charge\nout", RED, "center")
    wire([(22, 21), (35, 21), (35, 38)], RED, 2.6); lab(28.5, 19.2, "force + and -, 1.0 mm²", RED, "center")
    wire([(46, 27), (46, 38)], RED, 2.6); lab(46.6, 32.5, "load, 1.0 mm²", RED)
    # sensing and control
    wire([(22, 27), (29, 27), (29, 38)], GRY, 1.2); lab(28.4, 33.4, "sense + and -,\ntwisted, 0.25 mm²", GRY, "right")
    wire([(10, 16), (10, 10), (68, 10), (68, 48), (78, 48)], GRY, 1.2); lab(40, 10, "thermistor, 0.25 mm², to a controller input", GRY, "center")
    wire([(57, 50), (78, 54)], BLU, 1.2); lab(66, 54.2, "I2C bus", BLU, "center")
    wire([(57, 42), (78, 33)], GRY, 1.2); lab(62.5, 35.4, "charge and load\nenables", GRY, "center")
    wire([(86, 46), (86, 40)], GRY, 1.2); lab(86.6, 43, "heartbeat", GRY)
    ax.text(2, 6.0, "Safety: no cell in any holder and the inlet fuse out until the stop points in section 6 of the plan are passed. All circuits are extra-low voltage: 12.6 V highest.",
            fontsize=7.6, color="#B45309", fontweight="bold")
    ax.text(2, 3.6, "Red: power (wire sizes marked). Blue: data. Grey: sensing and control. Cell leads run under the base plate through the two wire slots of each channel.",
            fontsize=7.2, color=MUT)
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / "wiring.png"
    fig.savefig(out, facecolor="white"); plt.close(fig)
    return out


if __name__ == "__main__":
    what = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps", "wiring"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps, "wiring": wiring}
    for w in what:
        print(w, "->", fns[w]())
