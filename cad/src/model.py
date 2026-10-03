"""CellCheck parametric model (build123d), TRL 3, constructable design (CCK-DDR-003).

Run from the repo root:
    python cad/src/model.py            exports STEP and STL into cad/step and cad/stl, prints the
                                       envelope, part volumes and the constructability checks
    python cad/src/model.py --check    prints the constructability checks only

Every component is made or bought as described in the build plan CCK-BLD-001, and every one is
fixed to the parts next to it: six rubber feet with M4 studs hold six hex standoffs to the tray
floor, the base plate screws onto the standoffs, and everything else is screwed to the plate.
build_components() returns each component with its fixings; build_parts() returns the BOM-level
list used by the concept media, the drawing and the calculation note.

Axes: X across the front of the unit, Y from front (-Y) to back (+Y), Z up. Units mm.
The bench top is z = 0; the tray stands on its feet, so the tray floor is foot_h above the bench.
Inside build_components the geometry is drawn with the tray floor at z = 0 and then lifted.
Cells lie front to back in their holders. BOM numbers match bom/bom.csv.
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 Steel tray with ceramic fibre liner (CCK-PRC-001 v0.3)
    "tray_l": 460.0, "tray_w": 300.0, "tray_h": 45.0, "tray_t": 1.5, "liner_t": 3.0,
    "intake_w": 56.0, "intake_z0": 20.0, "intake_z1": 42.0,   # fan intake slots in the back wall
    # 19 Rubber feet with M4 studs, one under each standoff (CCK-DDR-003, P1)
    "foot_d": 20.0, "foot_h": 8.0,
    # 2 Base plate (1.5 mm aluminium) on six 12 mm hex standoffs (CCK-DDR-003, P1 and P2)
    "plate_l": 430.0, "plate_w": 270.0, "plate_t": 1.5, "plate_top": 15.0,
    "standoff_h": 12.0, "standoff_af": 7.0,
    "standoff_x": (-210.0, -45.0, 120.0), "standoff_y": 124.0,
    # 3 Channels and cell holders
    "n_ch": 8, "pitch": 40.0, "x0": -170.0,
    "cell_y": -55.0,                        # cell axis centre in Y
    "cell_r": 10.5, "cell_l": 70.0,         # largest cell accepted (21700); 18650 fits by adjustment
    "holder_w": 26.0, "holder_l": 84.0, "holder_h": 16.0,
    "holder_screw_dy": 25.0,                # two M3 screws from below, either side of the cell centre
    "cell_axis_h": 20.0,                    # cell axis above the plate top
    "slot_w": 16.0, "slot_d": 5.0,          # wire slots through the plate, one down and one up per channel
    "down_slot_y": -9.5, "up_slot_y": 36.5,
    # 4 Thermistor clip: printed C-clip round the top of the cell (CCK-DDR-003, P8)
    "clip_len": 10.0, "clip_wall": 1.6, "clip_wrap_below": 10.0,   # degrees below the cell axis
    # 5 Guard: folded 0.8 mm perforated steel, end flanges held by two thumb screws (CCK-DDR-003, P4)
    "guard_margin_x": 20.0, "guard_margin_y": 50.0, "guard_clear": 18.0, "guard_t": 0.8,
    "guard_flange": 18.0, "guard_stud_out": 10.0,
    # 6, 7 Module rows behind the cells (Y ranges); boards on 5 mm nylon standoffs
    "charger_y": (5.0, 33.0), "charger_h": 9.0, "sense_y": (40.0, 62.0), "sense_h": 6.0,
    "board_lift": 5.0,
    # 9 Heatsink: spine carrying the MOSFETs, vertical fins normal to X
    "hs_y0": 78.0, "spine_t": 6.0, "fin_depth": 30.0, "fin_h": 50.0, "fin_t": 1.6, "fin_pitch": 8.0,
    "hs_screw_x": (-150.0, -30.0, 90.0),
    # 10 Fans on a folded shroud behind the fins, pushing air forward into the fin channels
    "shroud_t": 1.0, "shroud_gap": 3.0, "fan": 60.0, "fan_t": 15.0, "fan_x": (-110.0, 50.0),
    "fan_guard_t": 1.6,                     # 60 mm steel wire finger guard on each fan (CCK-DEC-001, item 9)
    "seal_bead": 1.5,                       # silicone bead standing proud of each wire slot, top and bottom (item 2)
    # 11, 12, 13, 18, 21 Right-hand bay: (x0, x1, y0, y1, height)
    "ctrl": (160.0, 210.0, -10.0, 50.0, 12.0),
    "watchdog": (160.0, 210.0, -60.0, -25.0, 8.0),
    "buck": (160.0, 185.0, 58.0, 78.0, 8.0),
    "display": (126.0, 214.0, -133.0, -108.0, 62.0),   # printed stand footprint and height (CCK-DDR-003, P6)
    "inlet": (150.0, 205.0, 85.0, 125.0, 28.0),
    # 14 Adapter on the bench to the right; 15 rest rack on the bench to the left
    "adapter": (270.0, 420.0, 20.0, 80.0, 35.0),
    "rack_x1": -260.0, "rack_y0": -80.0, "rack_cols": 8, "rack_rows": 6, "rack_pitch": 26.0, "rack_h": 30.0,
}


@dataclass
class Comp:
    name: str
    shape: object
    bom: object        # BOM line number, or None (cells, context)
    kind: str          # "made", "bought", "fixing", "context"
    group: str         # BOM-level group for build_parts(), or None for fixings


def channel_x(p=PARAMS):
    return [p["x0"] + i * p["pitch"] for i in range(p["n_ch"])]


def heatsink_extent(p=PARAMS):
    """(x0, x1, y0, y1, z0, z1) of the heatsink, spine plus fins, above the tray floor."""
    cx = channel_x(p)
    return (cx[0] - 20.0, cx[-1] + 20.0, p["hs_y0"], p["hs_y0"] + p["spine_t"] + p["fin_depth"],
            p["plate_top"], p["plate_top"] + p["fin_h"])


def n_fins(p=PARAMS):
    x0, x1, *_ = heatsink_extent(p)
    return int((x1 - x0 - p["fin_t"]) // p["fin_pitch"]) + 1


def guard_extent(p=PARAMS):
    """(x0, x1, y0, y1, z0, z1) of the guard box, outside faces, flanges excluded."""
    cx = channel_x(p)
    cz = p["plate_top"] + p["cell_axis_h"]
    return (cx[0] - p["guard_margin_x"], cx[-1] + p["guard_margin_x"],
            p["cell_y"] - p["guard_margin_y"], p["cell_y"] + p["guard_margin_y"],
            p["plate_top"], cz + p["cell_r"] + p["guard_clear"])


def guard_studs(p=PARAMS):
    gx0, gx1, *_ = guard_extent(p)
    return [(gx0 - p["guard_stud_out"], p["cell_y"]), (gx1 + p["guard_stud_out"], p["cell_y"])]


def standoff_xy(p=PARAMS):
    return [(x, s * p["standoff_y"]) for x in p["standoff_x"] for s in (-1, 1)]


def envelope(p=PARAMS):
    """Envelope of the grader unit (tray, feet and contents) without adapter and rest rack."""
    top = max(p["plate_top"] + p["fan"], p["plate_top"] + p["display"][4], p["plate_top"] + p["fin_h"])
    return (-p["tray_l"] / 2, p["tray_l"] / 2, -p["tray_w"] / 2, p["tray_w"] / 2, 0.0, top + p["foot_h"])


# ------------------------------------------------------------------ geometry helpers
def bx(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def zcyl(x, y, z0, r, h):
    from build123d import Cylinder, Pos, Align
    return Pos(x, y, z0) * Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def ycyl(x, y0, z, r, h):
    from build123d import Cylinder, Pos, Rot, Align
    return Pos(x, y0, z) * Rot(-90, 0, 0) * Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def xcyl(x0, y, z, r, h):
    from build123d import Cylinder, Pos, Rot, Align
    return Pos(x0, y, z) * Rot(0, 90, 0) * Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))


def zhex(x, y, z0, af, h):
    from build123d import RegularPolygon, extrude, Pos, Plane
    poly = RegularPolygon(af / math.sqrt(3), 6)
    return Pos(x, y, z0) * extrude(poly, h)


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


# ------------------------------------------------------------------ components
def build_components(p=PARAMS):
    """Every component and fixing as a Comp, keyed by a short name, at its place on the bench."""
    from build123d import Pos
    cx = channel_x(p)
    L, W, H, t = p["tray_l"], p["tray_w"], p["tray_h"], p["tray_t"]
    PZ, PT = p["plate_top"], p["plate_t"]
    PB = PZ - PT                                    # underside of the plate
    CY, CR, CL = p["cell_y"], p["cell_r"], p["cell_l"]
    CZ = PZ + p["cell_axis_h"]
    F = p["foot_h"]
    C = {}

    def add(key, name, shape, bom, kind, group, lift=True):
        C[key] = Comp(name, Pos(0, 0, F) * shape if lift else shape, bom, kind, group)

    sxy = standoff_xy(p)

    # 1 Steel tray: bought, two intake slots cut in the back wall, six stud holes in the floor
    tray = bx(-L / 2, L / 2, -W / 2, W / 2, 0, H) - bx(-L / 2 + t, L / 2 - t, -W / 2 + t, W / 2 - t, t, H + 5)
    for fx in p["fan_x"]:
        tray -= bx(fx - p["intake_w"] / 2, fx + p["intake_w"] / 2, W / 2 - t - 1, W / 2 + 1, p["intake_z0"], p["intake_z1"])
    for x, y in sxy:
        tray -= zcyl(x, y, -1, 2.25, t + 2)
    add("tray", "Steel tray", tray, 1, "made", "tray")

    # 1 Ceramic fibre liner on the floor, cut round the standoffs
    liner = bx(-L / 2 + t, L / 2 - t, -W / 2 + t, W / 2 - t, t, t + p["liner_t"])
    for x, y in sxy:
        liner -= zcyl(x, y, 0, 6.0, 10)
    add("liner", "Ceramic fibre liner", liner, 1, "made", "tray")

    # 19 Rubber feet with M4 studs: the stud passes up through the tray floor into the standoff
    feet = fuse(zcyl(x, y, -F, p["foot_d"] / 2, F) + zcyl(x, y, 0, 2.0, t + 5) for x, y in sxy)
    add("feet", "Rubber feet with M4 studs (6)", feet, 19, "bought", "tray")

    # 2 Hex standoffs, floor to plate
    so = fuse(zhex(x, y, t, p["standoff_af"], PB - t) - zcyl(x, y, t - 1, 2.0, PB - t + 2) for x, y in sxy)
    add("standoffs", "Hex standoffs M4 x 12 (6)", so, 2, "bought", "plate")

    # 2 Base plate with every hole and slot
    pl, pw = p["plate_l"] / 2, p["plate_w"] / 2
    plate = bx(-pl, pl, -pw, pw, PB, PZ)
    holes = []
    for x, y in sxy:
        holes.append((x, y, 2.25))
    for x in cx:
        for s in (-1, 1):
            holes.append((x, CY + s * p["holder_screw_dy"], 1.7))
    for x, y in guard_studs(p):
        holes.append((x, y, 3.0))                   # M4 rivet nut body
    for x in p["hs_screw_x"]:
        holes.append((x, p["hs_y0"] + p["spine_t"] / 2, 1.7))
    for x, y in _board_standoffs(p):
        holes.append((x, y, 1.7))
    for x, y in _bay_screws(p):
        holes.append((x, y, 1.7))
    for x, y, r in holes:
        plate -= zcyl(x, y, PB - 1, r, PT + 2)
    sw, sd = p["slot_w"], p["slot_d"]
    for x in cx:
        for yc in (p["down_slot_y"], p["up_slot_y"]):
            plate -= bx(x - sw / 2, x + sw / 2, yc - sd / 2, yc + sd / 2, PB - 1, PZ + 1)
    add("plate", "Base plate", plate, 2, "made", "plate")
    # 16 High-temperature silicone filling each wire slot round the leads after wiring (CCK-DEC-001, item 2);
    #    the leads are not modelled, so the seal is drawn as a solid plug with a bead above and below
    sb = p["seal_bead"]
    seals = fuse(bx(x - sw_ / 2, x + sw_ / 2, yc - sd_ / 2, yc + sd_ / 2, PB - sb, PZ + sb)
                 for x in cx for yc in (p["down_slot_y"], p["up_slot_y"])
                 for sw_, sd_ in [(p["slot_w"], p["slot_d"])])
    add("seals", "Silicone slot seals (16)", seals, 16, "bought", "seals")
    add("plate_screws", "M4 screws, plate to standoffs (6)",
        fuse(zcyl(x, y, PZ, 3.8, 2.2) + zcyl(x, y, PB - 5, 2.0, 5 + PT) for x, y in sxy), 20, "fixing", None)

    # 3 Cell holders: body with a groove the cell rests in, force and sense contact posts at each end
    hw, hl = p["holder_w"] / 2, p["holder_l"] / 2
    holders, hscr = [], []
    for x in cx:
        body = bx(x - hw, x + hw, CY - hl, CY + hl, PZ, PZ + p["holder_h"])
        body -= ycyl(x, CY - CL / 2 - 3, CZ, CR, CL + 6)
        posts = (bx(x - 9, x + 9, CY - hl, CY - CL / 2, PZ, CZ + 10)
                 + bx(x - 9, x + 9, CY + CL / 2, CY + hl, PZ, CZ + 10))   # contacts touch the cell ends
        hb = body + posts
        for s in (-1, 1):
            yy = CY + s * p["holder_screw_dy"]
            hb -= zcyl(x, yy, PZ - 1, 1.5, 9)
            hscr.append(zcyl(x, yy, PB - 2.0, 2.75, 2.0) + zcyl(x, yy, PB, 1.5, PT + 6))
        holders.append(hb)
    add("holders", "Cell holders, four-wire (8)", fuse(holders), 3, "bought", "holders")
    add("holder_screws", "M3 screws, holders (16)", fuse(hscr), 20, "fixing", None)

    # Cells under test (not supplied), 21700 size, resting in the groove and touching both contact posts
    cells = fuse(ycyl(x, CY - CL / 2, CZ, CR, CL) for x in cx)
    add("cells", "Cells under test (not supplied)", cells, None, "context", "cells")

    # 4 Thermistor C-clips: printed, round the top of each cell, with a pocket for the thermistor
    cw = p["clip_wall"]
    zcut = CZ - CR * math.sin(math.radians(p["clip_wrap_below"]))
    clips = []
    for x in cx:
        ring = ycyl(x, CY - p["clip_len"] / 2, CZ, CR + cw, p["clip_len"]) - ycyl(x, CY - p["clip_len"] / 2 - 1, CZ, CR, p["clip_len"] + 2)
        ring -= bx(x - 20, x + 20, CY - 10, CY + 10, zcut - 30, zcut)
        ring += bx(x - 3.5, x + 3.5, CY - p["clip_len"] / 2, CY + p["clip_len"] / 2, CZ + CR + cw - 0.5, CZ + CR + cw + 3.0)
        clips.append(ring)
    add("clips", "Thermistor clips (8)", fuse(clips), 4, "made", "clips")

    # 5 Guard: open-bottomed folded box with end flanges; M4 rivet nuts in the plate, thumb screws
    gx0, gx1, gy0, gy1, gz0, gz1 = guard_extent(p)
    gt, gf = p["guard_t"], p["guard_flange"]
    guard = bx(gx0, gx1, gy0, gy1, gz0, gz1) - bx(gx0 + gt, gx1 - gt, gy0 + gt, gy1 - gt, gz0 - 1, gz1 - gt)
    guard += bx(gx0 - gf, gx0, gy0, gy1, PZ, PZ + gt) + bx(gx1, gx1 + gf, gy0, gy1, PZ, PZ + gt)
    for x, y in guard_studs(p):
        guard -= zcyl(x, y, PZ - 1, 5.0, gt + 2)
    add("guard", "Perforated steel guard", guard, 5, "made", "guard")
    rn = fuse(zcyl(x, y, PB - 7, 3.0, 7 + PT) - zcyl(x, y, PB - 8, 2.0, 9 + PT) + zcyl(x, y, PZ, 4.5, gt) for x, y in guard_studs(p))
    add("rivet_nuts", "M4 rivet nuts in the plate (2)", rn, 20, "fixing", None)
    ts = fuse(zcyl(x, y, PZ + gt, 7.0, 6.0) + zcyl(x, y, PB - 5, 2.0, PZ + gt - PB + 5) for x, y in guard_studs(p))
    add("thumb_screws", "M4 knurled thumb screws (2)", ts, 20, "fixing", None)

    # 6 Charger modules and 7 channel boards, each on two 5 mm nylon standoffs
    lift = p["board_lift"]
    y0, y1 = p["charger_y"]
    chargers = fuse(bx(x - 12, x + 12, y0, y1, PZ + lift, PZ + lift + p["charger_h"]) for x in cx)
    add("chargers", "Charger modules (8)", chargers, 6, "bought", "chargers")
    y0, y1 = p["sense_y"]
    boards = fuse(bx(x - 12, x + 12, y0, y1, PZ + lift, PZ + lift + p["sense_h"]) for x in cx)
    add("boards", "Channel boards (8)", boards, 7, "bought", "boards")
    bst = [zcyl(x, y, PZ, 2.5, lift) for x, y in _board_standoffs(p)]
    for key in ("ctrl", "watchdog", "buck"):
        bst += [zcyl(x, y, PZ, 2.5, lift) for x, y in _bay_standoffs(p, key)]
    add("board_standoffs", "Nylon standoffs 5 mm", fuse(bst), 20, "fixing", None)

    # 9 Heatsink: spine along X, vertical fins normal to X; M3 tapped holes for the MOSFETs,
    #   the plate screws (bottom edge) and the shroud screws (ends)
    hx0, hx1, hy0, hy1, hz0, hz1 = heatsink_extent(p)
    spine_y1 = hy0 + p["spine_t"]
    ym = hy0 + p["spine_t"] / 2
    heatsink = bx(hx0, hx1, hy0, spine_y1, hz0, hz1)
    for i in range(n_fins(p)):
        fx = hx0 + i * p["fin_pitch"]
        heatsink += bx(fx, fx + p["fin_t"], spine_y1, hy1, hz0, hz1)
    zt = PZ + 26.5                                   # MOSFET tab hole height
    for x in cx:
        heatsink -= ycyl(x, hy0 - 1, zt, 1.5, p["spine_t"] + 2)
    for x in p["hs_screw_x"]:
        heatsink -= zcyl(x, ym, PZ - 1, 1.5, 11)
    shroud_z = (PZ + 15, PZ + 35)
    for z in shroud_z:
        heatsink -= xcyl(hx0 - 1, ym, z, 1.5, 9) + xcyl(hx1 - 8, ym, z, 1.5, 9)
    add("heatsink", "Heatsink", heatsink, 9, "made", "heatsink")
    add("hs_screws", "M3 screws, heatsink to plate (3)",
        fuse(zcyl(x, ym, PB - 2.0, 2.75, 2.0) + zcyl(x, ym, PB, 1.5, PT + 8) for x in p["hs_screw_x"]), 20, "fixing", None)

    # 8 Load MOSFETs (TO-220): body and tab against the spine, clamped by one M3 screw each
    mos, mscr = [], []
    for x in cx:
        body = bx(x - 5, x + 5, hy0 - 4.5, hy0, PZ + 14, PZ + 23)
        tab = bx(x - 5, x + 5, hy0 - 1.3, hy0, PZ + 23, PZ + 30) - ycyl(x, hy0 - 2, zt, 1.6, 3)
        legs = bx(x - 4, x + 4, hy0 - 2.5, hy0 - 2, PZ + 3, PZ + 14)
        mos.append(body + tab + legs)
        mscr.append(ycyl(x, hy0 - 1.3 - 2.4, zt, 2.75, 2.4) + ycyl(x, hy0 - 1.3, zt, 1.5, 1.3 + p["spine_t"]))
    add("mosfets", "Load MOSFETs (8)", fuse(mos), 8, "bought", "mosfets")
    add("mosfet_screws", "M3 screws, MOSFETs (8)", fuse(mscr), 20, "fixing", None)

    # 10 Shroud: folded 1 mm aluminium, back sheet with two fan holes and two side flanges
    #    screwed to the ends of the spine; fans screwed to the back sheet from inside
    st = p["shroud_t"]
    sy0 = hy1 + p["shroud_gap"]
    sy1 = sy0 + st
    fz = PZ + p["fan"] / 2
    shroud = bx(hx0 - st, hx1 + st, sy0, sy1, PZ, PZ + p["fan"])
    shroud += bx(hx0 - st, hx0, hy0, sy0, PZ, hz1) + bx(hx1, hx1 + st, hy0, sy0, PZ, hz1)
    sscr = []
    for z in shroud_z:
        shroud -= xcyl(hx0 - st - 1, ym, z, 1.7, st + 2) + xcyl(hx1 - 1, ym, z, 1.7, st + 2)
        sscr.append(xcyl(hx0 - st - 2.0, ym, z, 2.75, 2.0) + xcyl(hx0 - st, ym, z, 1.5, st + 6))
        sscr.append(xcyl(hx1 + st, ym, z, 2.75, 2.0) + xcyl(hx1 - 6, ym, z, 1.5, st + 6))
    fans, fscr, fguards, fgscr = None, [], [], []
    for fx in p["fan_x"]:
        shroud -= ycyl(fx, sy0 - 1, fz, 27, st + 2)
        for dx in (-25, 25):
            for dz in (-25, 25):
                shroud -= ycyl(fx + dx, sy0 - 1, fz + dz, 1.7, st + 2)
                fscr.append(ycyl(fx + dx, sy0 - 1.5, fz + dz, 2.5, 1.5) + ycyl(fx + dx, sy0, fz + dz, 1.4, st + 6))
        f = (bx(fx - 30, fx + 30, sy1, sy1 + p["fan_t"], PZ, PZ + p["fan"])
             - ycyl(fx, sy1 - 1, fz, 27, p["fan_t"] + 2)
             + ycyl(fx, sy1 + 1, fz, 12, p["fan_t"] - 2))
        for dx in (-25, 25):
            for dz in (-25, 25):
                f -= ycyl(fx + dx, sy1 - 1, fz + dz, 1.4, 7)
                f -= ycyl(fx + dx, sy1 + p["fan_t"] - 6, fz + dz, 1.4, 7)      # guard screw pilot holes
        fans = f if fans is None else fans + f
        # Finger guard (CCK-DEC-001, item 9): steel wire guard on the outer face of the fan, three
        # rings and a cross inside a square frame, held by four small self-tapping screws
        gy, gw_ = sy1 + p["fan_t"], p["fan_guard_t"]
        g = bx(fx - 30, fx + 30, gy, gy + gw_, fz - 30, fz + 30) - bx(fx - 28, fx + 28, gy - 1, gy + gw_ + 1, fz - 28, fz + 28)
        for r in (10.0, 17.0, 24.0):
            g += ycyl(fx, gy, fz, r + 0.8, gw_) - ycyl(fx, gy - 1, fz, r - 0.8, gw_ + 2)
        g += bx(fx - 28, fx + 28, gy, gy + gw_, fz - 0.8, fz + 0.8) + bx(fx - 0.8, fx + 0.8, gy, gy + gw_, fz - 28, fz + 28)
        for dx in (-25, 25):
            for dz in (-25, 25):
                g += bx(fx + dx - 4, fx + dx + 4, gy, gy + gw_, fz + dz - 4, fz + dz + 4)    # corner tabs
                g -= ycyl(fx + dx, gy - 1, fz + dz, 1.7, gw_ + 2)
                fgscr.append(ycyl(fx + dx, gy + gw_, fz + dz, 2.5, 1.2) + ycyl(fx + dx, gy - 5.0, fz + dz, 1.4, 5.0 + gw_))
        fguards.append(g)
    add("shroud", "Fan shroud", shroud, 10, "made", "fans")
    add("shroud_screws", "M3 screws, shroud to heatsink (4)", fuse(sscr), 20, "fixing", None)
    add("fans", "Fans, 60 mm (2)", fans, 10, "bought", "fans")
    add("fan_screws", "Fan screws (8)", fuse(fscr), 20, "fixing", None)
    add("fan_guards", "Fan finger guards, 60 mm (2)", fuse(fguards), 10, "bought", "fan_guards")
    add("fan_guard_screws", "Fan guard screws (8)", fuse(fgscr), 20, "fixing", None)

    # 11 Controller, 18 watchdog board, 21 5 V converter, each on two nylon standoffs
    def blk(key):
        x0, x1, y0, y1, h = p[key]
        return bx(x0, x1, y0, y1, PZ + lift, PZ + lift + h)
    add("ctrl", "Controller board", blk("ctrl"), 11, "bought", "ctrl")
    add("watchdog", "Watchdog and undervoltage board", blk("watchdog"), 18, "bought", "watchdog")
    add("buck", "12 V to 5 V converter", blk("buck"), 21, "bought", "buck")

    # 12 Display stand (printed): foot with two screws from below, upright carrying the display
    dx0, dx1, dy0, dy1, dh = p["display"]
    up_y = (dy0 + 15, dy0 + 23)
    stand = bx(dx0, dx1, dy0, dy1, PZ, PZ + 5) + bx(dx0, dx1, up_y[0], up_y[1], PZ, PZ + dh)
    stand -= bx(dx0 + 12, dx1 - 12, up_y[0] - 1, up_y[1] + 1, PZ + 22, PZ + dh - 12)  # window for the display's pins
    for x, y in _bay_screws(p, only="display"):
        stand -= zcyl(x, y, PZ - 1, 1.5, 6)
    xm = (dx0 + dx1) / 2
    for dxb in (-25, 0, 25):
        stand -= zcyl(xm + dxb, dy0 + 7, PZ - 1, 3.5, 7)        # holes for the panel-mount push buttons
    add("stand", "Display stand", stand, 12, "made", "display")
    xm = (dx0 + dx1) / 2
    disp = bx(xm - 43, xm + 43, up_y[0] - 4, up_y[0], PZ + 9, PZ + 59)
    btns = fuse(zcyl(xm + dxb, dy0 + 7, PZ + 1, 3.5, 9) + zcyl(xm + dxb, dy0 + 7, PZ + 5, 5.0, 1.5) for dxb in (-25, 0, 25))
    add("display", "Display and buttons", disp + btns, 12, "bought", "display")

    # 13 Inlet housing (printed) with the DC jack, fuse holder and switch on its top
    ix0, ix1, iy0, iy1, ih = p["inlet"]
    house = bx(ix0, ix1, iy0, iy1, PZ, PZ + ih) - bx(ix0 + 2, ix1 - 2, iy0 + 2, iy1 - 2, PZ - 1, PZ + ih - 2)
    house -= bx(ix0 + 10, ix0 + 30, iy0 - 1, iy0 + 3, PZ - 1, PZ + 8)           # wire exit
    for x, y in _bay_screws(p, only="inlet"):                                    # two screw bosses
        house += zcyl(x, y, PZ, 4.0, 8) - zcyl(x, y, PZ - 1, 1.5, 9)
    xc, yc = (ix0 + ix1) / 2, (iy0 + iy1) / 2
    top = PZ + ih
    jack, fuse_, sw = (xc - 15, yc), (xc + 2, yc - 8), (xc + 16, yc + 6)
    house -= zcyl(*jack, top - 3, 5.6, 4) + zcyl(*fuse_, top - 3, 6.0, 4)
    house -= bx(sw[0] - 6, sw[0] + 6, sw[1] - 8, sw[1] + 8, top - 3, top + 1)
    parts13 = (zcyl(*jack, top - 12, 5.6, 12) + zcyl(*jack, top, 7.0, 2.5)          # DC jack and its nut
               + zcyl(*fuse_, top - 14, 6.0, 14) + zcyl(*fuse_, top, 6.8, 12)       # fuse holder and cap
               + bx(sw[0] - 6, sw[0] + 6, sw[1] - 8, sw[1] + 8, top - 14, top)      # rocker switch body
               + bx(sw[0] - 7.5, sw[0] + 7.5, sw[1] - 9.5, sw[1] + 9.5, top, top + 2.5)
               + bx(sw[0] - 5, sw[0] + 5, sw[1] - 6, sw[1] + 6, top + 2.5, top + 5))
    add("inlet_house", "Inlet housing", house, 13, "made", "inlet")
    add("inlet_parts", "DC jack, fuse holder and switch", parts13, 13, "bought", "inlet")

    # Screws for the bay boards (from below, M3)
    bays = [zcyl(x, y, PB - 2.0, 2.75, 2.0) + zcyl(x, y, PB, 1.5, PT + 4) for x, y in _bay_screws(p)]
    add("bay_screws", "M3 screws, display and inlet (4)", fuse(bays), 20, "fixing", None)

    # 14 Certified 12 V adapter on the bench (not lifted)
    ax0, ax1, ay0, ay1, ah = p["adapter"]
    add("adapter", "12 V 5 A certified adapter", bx(ax0, ax1, ay0, ay1, 0, ah), 14, "bought", "adapter", lift=False)

    # 15 Rest rack (printed), cols x rows cells upright; resting cells shown in part of the slots
    rp, x1r, y0r = p["rack_pitch"], p["rack_x1"], p["rack_y0"]
    nc, nr = p["rack_cols"], p["rack_rows"]
    rack = bx(x1r - nc * rp - 8, x1r, y0r, y0r + nr * rp + 8, 0, p["rack_h"])
    rest = []
    for i in range(nc):
        for j in range(nr):
            x, y = x1r - 4 - rp / 2 - i * rp, y0r + 4 + rp / 2 + j * rp
            rack -= zcyl(x, y, 5, CR + 0.8, 30)
            if (i + j) % 3 != 1:
                rest.append(zcyl(x, y, 5, CR, CL))
    add("rack", "Rest rack", rack, 15, "made", "rack", lift=False)
    add("rest", "Cells resting (not supplied)", fuse(rest), None, "context", "rest", lift=False)
    return C


def _board_standoffs(p=PARAMS):
    out = []
    for x in channel_x(p):
        y0, y1 = p["charger_y"]
        out += [(x - 9, y0 + 3), (x + 9, y1 - 3)]
        y0, y1 = p["sense_y"]
        out += [(x - 9, y0 + 3), (x + 9, y1 - 3)]
    for key in ("ctrl", "watchdog", "buck"):
        out += _bay_standoffs(p, key)
    return out


def _bay_standoffs(p, key):
    x0, x1, y0, y1, _ = p[key]
    return [(x0 + 4, y0 + 4), (x1 - 4, y1 - 4)]


def _bay_screws(p=PARAMS, only=None):
    dx0, dx1, dy0, dy1, _ = p["display"]
    ix0, ix1, iy0, iy1, _ = p["inlet"]
    d = {"display": [(dx0 + 6, dy0 + 7), (dx1 - 6, dy0 + 7)],
         "inlet": [(ix0 + 6, iy0 + 6), (ix1 - 6, iy1 - 6)]}
    return d[only] if only else d["display"] + d["inlet"]


# BOM-level groups, in the order used by the concept media, with names, colours and explode offsets
GROUPS = [
    ("tray", "Steel tray, liner and feet", "#6B7280", 1, (0, 0, -170)),
    ("plate", "Base plate on standoffs", "#D1D5DB", 2, (0, 0, -90)),
    ("holders", "Cell holders, four-wire contacts", "#374151", 3, (0, 0, 0)),
    ("cells", "Cells under test (not supplied)", "#A8B0BA", None, (0, 0, 70)),
    ("clips", "Thermistor clips", "#C2410C", 4, (0, -40, 140)),
    ("guard", "Perforated steel cell guard", "#9CA3AF", 5, (0, -120, 240)),
    ("chargers", "Charger modules, 1 A CC-CV", "#0F766E", 6, (0, 40, 50)),
    ("boards", "Channel boards", "#15803D", 7, (0, 80, 110)),
    ("mosfets", "Load MOSFETs", "#1F2937", 8, (0, 120, 170)),
    ("seals", "Silicone seals in the wire slots", "#F59E0B", 16, (0, 0, -40)),
    ("heatsink", "Heatsink, vertical fins", "#94A3B8", 9, (0, 190, 170)),
    ("fans", "Fans, 60 mm, on shroud", "#4B5563", 10, (0, 290, 170)),
    ("fan_guards", "Fan finger guards, 60 mm", "#B8BEC6", 10, (0, 345, 170)),
    ("ctrl", "Controller, ESP32-S3 class", "#D4A017", 11, (120, 0, 60)),
    ("display", "Display and buttons on stand", "#38BDF8", 12, (130, -90, 40)),
    ("inlet", "Power inlet, fuse and switch", "#991B1B", 13, (140, 120, 40)),
    ("adapter", "12 V 5 A certified adapter", "#111827", 14, (220, 0, 0)),
    ("rack", "Self-discharge rest rack, 48 cells", "#E5E7EB", 15, (150, -470, 0)),
    ("rest", "Cells resting (not supplied)", "#A8B0BA", None, (150, -470, 0)),
    ("watchdog", "Watchdog and undervoltage board", "#DC2626", 18, (130, -40, 80)),
    ("buck", "12 V to 5 V converter", "#7C3AED", 21, (140, 60, 70)),
]


def build_parts(p=PARAMS, C=None):
    """Return a list of (name, shape, colour, bom_item, explode_offset), one per BOM-level group.
    Fixings are left out."""
    C = C or build_components(p)
    out = []
    for g, name, col, bom, ex in GROUPS:
        shapes = [c.shape for c in C.values() if c.group == g]
        out.append((name, fuse(shapes), col, bom, ex))
    return out


UNIT_ITEMS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 18, 19, 21}   # parts in or under the tray


def assemblies(parts=None):
    from build123d import Compound
    parts = parts or build_parts()
    by = {bom: s for _, s, _, bom, _ in parts if bom is not None}
    unit = [s for _, s, _, bom, _ in parts if bom in UNIT_ITEMS]
    unit_cells = unit + [s for n, s, _, bom, _ in parts if n.startswith("Cells under test")]
    return {
        "cellcheck-assembly": Compound(unit_cells),
        "cellcheck-tray": by[1],
        "cellcheck-heatsink": by[9],
        "cellcheck-cell-holders": by[3],
        "cellcheck-rest-rack": by[15],
    }


# ------------------------------------------------------------------ constructability checks
def _vol(a, b_):
    try:
        s = a & b_
        return s.volume if s is not None else 0.0
    except Exception:
        return float("nan")


def checks(p=PARAMS, C=None):
    """Pairs that must touch, or must stay apart by a clearance (mm).
    Returns a list of (description, overlap volume mm3, gap mm, expectation, ok)."""
    C = C or build_components(p)
    S = lambda k: C[k].shape  # noqa: E731
    rows = []

    def chk(desc, a, b_, expect):
        v = _vol(a, b_)
        gp = a.distance_to(b_)
        ok = v < 1e-2 and (gp < 0.05 if expect == "touch" else gp >= expect - 1e-6)
        rows.append((desc, v, gp, expect, ok))

    chk("Feet under the tray floor", S("feet"), S("tray"), "touch")
    chk("Standoffs on the tray floor", S("standoffs"), S("tray"), "touch")
    chk("Standoffs clear of the liner", S("standoffs"), S("liner"), 1.0)
    chk("Liner on the tray floor", S("liner"), S("tray"), "touch")
    chk("Plate on the standoffs", S("plate"), S("standoffs"), "touch")
    chk("Plate clear of the tray walls", S("plate"), S("tray"), 5.0)
    chk("Plate clear of the liner (wire space under it)", S("plate"), S("liner"), 8.0)
    chk("Plate screws on the plate", S("plate_screws"), S("plate"), "touch")
    chk("Holders on the plate", S("holders"), S("plate"), "touch")
    chk("Holder screws under the plate", S("holder_screws"), S("plate"), "touch")
    chk("Holder screws clear of the liner", S("holder_screws"), S("liner"), 1.0)
    chk("Cells in the holder grooves and on the contacts", S("cells"), S("holders"), "touch")
    chk("Thermistor clips on the cells", S("clips"), S("cells"), "touch")
    chk("Thermistor clips clear of the holders", S("clips"), S("holders"), 1.0)
    chk("Guard on the plate", S("guard"), S("plate"), "touch")
    chk("Guard clear of the holders", S("guard"), S("holders"), 3.0)
    chk("Guard clear of the cells and clips", S("guard"), S("cells") + S("clips"), 5.0)
    chk("Guard clear of the chargers", S("guard"), S("chargers"), 3.0)
    chk("Guard clear of the display stand", S("guard"), S("stand") + S("display"), 1.0)
    chk("Rivet nuts in the plate", S("rivet_nuts"), S("plate"), "touch")
    chk("Thumb screws on the guard flanges", S("thumb_screws"), S("guard"), "touch")
    chk("Thumb screws clear of the guard walls", S("thumb_screws"), S("guard") - _flanges(p), 2.0)
    chk("Chargers on their standoffs", S("chargers"), S("board_standoffs"), "touch")
    chk("Channel boards on their standoffs", S("boards"), S("board_standoffs"), "touch")
    chk("Board standoffs on the plate", S("board_standoffs"), S("plate"), "touch")
    chk("Chargers clear of the channel boards", S("chargers"), S("boards"), 5.0)
    chk("Channel boards clear of the MOSFETs", S("boards"), S("mosfets"), 5.0)
    chk("Heatsink on the plate", S("heatsink"), S("plate"), "touch")
    chk("Heatsink screws into the spine", S("hs_screws"), S("heatsink"), "touch")
    chk("MOSFETs against the spine", S("mosfets"), S("heatsink"), "touch")
    chk("MOSFETs clear of the plate (leads only below)", S("mosfets"), S("plate"), 2.0)
    chk("MOSFET screws through the tabs", S("mosfet_screws"), S("mosfets"), "touch")
    chk("MOSFET screws in the spine", S("mosfet_screws"), S("heatsink"), "touch")
    chk("Shroud on the plate", S("shroud"), S("plate"), "touch")
    chk("Shroud flanges against the spine ends", S("shroud"), S("heatsink"), "touch")
    chk("Shroud screws in the spine ends", S("shroud_screws"), S("heatsink"), "touch")
    chk("Fans on the shroud", S("fans"), S("shroud"), "touch")
    chk("Fans on the plate", S("fans"), S("plate"), "touch")
    chk("Fan screws clear of the fins", S("fan_screws"), S("heatsink"), 1.0)
    chk("Finger guards on the fans", S("fan_guards"), S("fans"), "touch")
    chk("Finger guards clear of the shroud", S("fan_guards"), S("shroud"), 10.0)
    chk("Finger guards clear of the tray back wall", S("fan_guards"), S("tray"), 10.0)
    chk("Guard screws in the finger guards", S("fan_guard_screws"), S("fan_guards"), "touch")
    chk("Guard screws in the fan frames", S("fan_guard_screws"), S("fans"), "touch")
    chk("Silicone seals fill the plate slots", S("seals"), S("plate"), "touch")
    chk("Silicone seals clear of the holders", S("seals"), S("holders"), 1.0)
    chk("Silicone seals clear of the chargers and channel boards", S("seals"), S("chargers") + S("boards"), 1.0)
    chk("Silicone seals clear of the guard walls", S("seals"), S("guard"), 1.0)
    chk("Silicone seals clear of the liner and standoffs", S("seals"), S("liner") + S("standoffs"), 1.0)
    chk("Fans clear of the tray back wall", S("fans"), S("tray"), 10.0)
    for k in ("ctrl", "watchdog", "buck"):
        chk(f"{C[k].name} on its standoffs", S(k), S("board_standoffs"), "touch")
    chk("Buck converter clear of the inlet housing", S("buck"), S("inlet_house"), 3.0)
    chk("Buck converter clear of the heatsink and shroud", S("buck"), S("heatsink") + S("shroud"), 10.0)
    chk("Display stand on the plate", S("stand"), S("plate"), "touch")
    chk("Display on its stand", S("display"), S("stand"), "touch")
    chk("Display stand clear of the plate screws", S("stand"), S("plate_screws"), 1.0)
    chk("Inlet housing on the plate", S("inlet_house"), S("plate"), "touch")
    chk("Jack, fuse holder and switch in the housing", S("inlet_parts"), S("inlet_house"), "touch")
    chk("Inlet clear of the plate screws", S("inlet_house"), S("plate_screws"), 1.0)
    chk("Inlet clear of the tray", S("inlet_house") + S("inlet_parts"), S("tray"), 10.0)
    chk("Display clear of the tray", S("stand") + S("display"), S("tray"), 5.0)
    chk("Fixings under the plate clear of the liner",
        S("hs_screws") + S("bay_screws") + S("rivet_nuts") + S("thumb_screws"), S("liner"), 1.0)
    # every made or bought part inside the tray clear of every other it should not touch
    keys = ["holders", "guard", "chargers", "boards", "heatsink", "mosfets", "shroud", "fans",
            "ctrl", "watchdog", "buck", "stand", "inlet_house"]
    touching = {("heatsink", "mosfets"), ("heatsink", "shroud"), ("shroud", "fans")}
    for i, a in enumerate(keys):
        for b_ in keys[i + 1:]:
            if (a, b_) in touching or (b_, a) in touching:
                continue
            chk(f"{C[a].name} apart from {C[b_].name}", S(a), S(b_), 1.0)
    return rows


def _flanges(p=PARAMS):
    from build123d import Pos
    gx0, gx1, gy0, gy1, *_ = guard_extent(p)
    PZ, F = p["plate_top"], p["foot_h"]
    return Pos(0, 0, F) * (bx(gx0 - p["guard_flange"] - 1, gx0 + 0.5, gy0 - 1, gy1 + 1, PZ - 1, PZ + p["guard_t"] + 0.01)
                           + bx(gx1 - 0.5, gx1 + p["guard_flange"] + 1, gy0 - 1, gy1 + 1, PZ - 1, PZ + p["guard_t"] + 0.01))


def print_checks(p=PARAMS, C=None):
    rows = checks(p, C)
    bad = 0
    for desc, v, gp, exp, ok in rows:
        e = "touch" if exp == "touch" else f">= {exp:g} mm"
        print(f"  {'ok ' if ok else 'BAD'}  {desc:62s} overlap {v:8.3f} mm3  gap {gp:7.2f} mm  ({e})")
        bad += not ok
    print(f"constructability checks: {len(rows) - bad} of {len(rows)} pass")
    return bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(1 if print_checks() else 0)
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    C = build_components()
    parts = build_parts(C=C)
    for name, shape in assemblies(parts).items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"), tolerance=0.05, angular_tolerance=0.3)
        bb = shape.bounding_box()
        print(f"{name:24s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm")
    e = envelope()
    print(f"grader unit envelope: {e[1]-e[0]:.0f} x {e[3]-e[2]:.0f} x {e[5]-e[4]:.0f} mm; heatsink fins: {n_fins()}")
    print("part volumes (cm3):")
    for name, shape, _, bom, _ in parts:
        print(f"  {str(bom or '-'):>3s} {name:38s} {shape.volume / 1000:8.1f}")
    print_checks(C=C)
