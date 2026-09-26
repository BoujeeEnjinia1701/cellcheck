"""CellCheck parametric model (build123d), TRL 3.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl, and prints the envelopes and part volumes
that CCK-CAL-001 cross-checks for the mass estimate.

Massing-plus detail: correct interfaces (eight four-wire cell holders for 18650 and 21700
cells at a 40 mm pitch, the thermistor clips, the heatsink with vertical fins and its fan
shroud, the 12 V inlet, the tray and guard that form the containment) and main dimensions;
not fabrication detail.

Axes: X across the front of the unit, Y from front (-Y) to back (+Y), Z up. Units mm.
The bench top is z = 0. Cells lie front to back in their holders. BOM numbers match bom/bom.csv.
"""
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # 1 Steel tray with ceramic fibre liner (CCK-PRC-001 v0.3)
    "tray_l": 460.0, "tray_w": 300.0, "tray_h": 45.0, "tray_t": 1.5, "liner_t": 3.0,
    "intake_w": 56.0, "intake_z0": 20.0, "intake_z1": 42.0,   # fan intake slots in the back wall
    # 2 Base plate (2 mm aluminium) on four standoffs
    "plate_l": 430.0, "plate_w": 270.0, "plate_t": 2.0, "plate_top": 15.0,
    # 3 Channels and cell holders
    "n_ch": 8, "pitch": 40.0, "x0": -170.0,
    "cell_y": -55.0,                        # cell axis centre in Y
    "cell_r": 10.5, "cell_l": 70.0,         # largest cell accepted (21700); 18650 fits by adjustment
    "holder_w": 26.0, "holder_l": 84.0, "holder_h": 16.0,
    "cell_axis_h": 20.0,                    # cell axis above the plate top
    # 5 Guard
    "guard_margin_x": 20.0, "guard_margin_y": 50.0, "guard_clear": 18.0, "guard_bar": 3.0,
    # 6, 7 Module rows behind the cells (Y ranges)
    "charger_y": (5.0, 33.0), "charger_h": 9.0, "sense_y": (40.0, 62.0), "sense_h": 6.0,
    # 9 Heatsink: spine carrying the MOSFETs, vertical fins normal to X
    "hs_y0": 78.0, "spine_t": 6.0, "fin_depth": 30.0, "fin_h": 50.0, "fin_t": 1.6, "fin_pitch": 8.0,
    # 10 Fans on a shroud behind the fins, pushing air forward into the fin channels
    "shroud_t": 1.0, "shroud_gap": 3.0, "fan": 60.0, "fan_t": 15.0, "fan_x": (-110.0, 50.0),
    # 11, 12, 13, 18 Right-hand bay
    "ctrl": (150.0, 200.0, -10.0, 50.0, 12.0),
    "watchdog": (150.0, 200.0, -60.0, -25.0, 8.0),
    "display": (145.0, 205.0, -125.0, -113.0, 55.0),
    "inlet": (150.0, 205.0, 85.0, 125.0, 28.0),
    # 14 Adapter on the bench to the right; 15 rest rack on the bench to the left
    "adapter": (270.0, 420.0, 20.0, 80.0, 35.0),
    "rack_x1": -260.0, "rack_y0": -80.0, "rack_cols": 8, "rack_rows": 6, "rack_pitch": 26.0, "rack_h": 30.0,
}


def channel_x(p=PARAMS):
    return [p["x0"] + i * p["pitch"] for i in range(p["n_ch"])]


def _box(x0, x1, y0, y1, z0, z1):
    from build123d import Box, Pos
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def heatsink_extent(p=PARAMS):
    """(x0, x1, y0, y1, z0, z1) of the heatsink, spine plus fins."""
    cx = channel_x(p)
    return (cx[0] - 20.0, cx[-1] + 20.0, p["hs_y0"], p["hs_y0"] + p["spine_t"] + p["fin_depth"],
            p["plate_top"], p["plate_top"] + p["fin_h"])


def n_fins(p=PARAMS):
    x0, x1, *_ = heatsink_extent(p)
    return int((x1 - x0 - p["fin_t"]) // p["fin_pitch"]) + 1


def envelope(p=PARAMS):
    """Envelope of the grader unit (tray and contents) without adapter and rest rack."""
    fan_top = p["plate_top"] + p["fan"]
    top = max(fan_top, p["plate_top"] + p["display"][4], p["plate_top"] + p["fin_h"])
    return (-p["tray_l"] / 2, p["tray_l"] / 2, -p["tray_w"] / 2, p["tray_w"] / 2, 0.0, top)


def build_parts(p=PARAMS):
    """Return a list of (name, shape, colour, bom_item, explode_offset)."""
    from build123d import Cylinder, Pos, Rot
    b = _box
    cx = channel_x(p)
    L, W, H, t = p["tray_l"], p["tray_w"], p["tray_h"], p["tray_t"]
    PZ = p["plate_top"]
    CY, CR, CL = p["cell_y"], p["cell_r"], p["cell_l"]
    CZ = PZ + p["cell_axis_h"]

    # 1 Steel tray with ceramic fibre liner on the floor; intake slots in the back wall behind the fans
    tray = b(-L / 2, L / 2, -W / 2, W / 2, 0, H) - b(-L / 2 + t, L / 2 - t, -W / 2 + t, W / 2 - t, t, H + 5)
    for fx in p["fan_x"]:
        tray = tray - b(fx - p["intake_w"] / 2, fx + p["intake_w"] / 2, W / 2 - t - 1, W / 2 + 1,
                        p["intake_z0"], p["intake_z1"])
    liner = b(-L / 2 + t, L / 2 - t, -W / 2 + t, W / 2 - t, t, t + p["liner_t"])
    tray = tray + liner

    # 2 Base plate on four standoffs standing on the liner
    pl, pw = p["plate_l"] / 2, p["plate_w"] / 2
    plate = b(-pl, pl, -pw, pw, PZ - p["plate_t"], PZ)
    z_floor = t + p["liner_t"]
    for sx in (-pl + 15, pl - 15):
        for sy in (-pw + 15, pw - 15):
            plate = plate + Pos(sx, sy, (z_floor + PZ - p["plate_t"]) / 2) * Cylinder(5, PZ - p["plate_t"] - z_floor)

    # 3 Cell holders: body with a groove, force and sense contact posts at each end
    hw, hl = p["holder_w"] / 2, p["holder_l"] / 2
    holders = []
    for x in cx:
        body = b(x - hw, x + hw, CY - hl, CY + hl, PZ, PZ + p["holder_h"])
        groove = Pos(x, CY, CZ) * Rot(90, 0, 0) * Cylinder(CR + 0.5, CL + 6)
        posts = (b(x - 9, x + 9, CY - hl, CY - hl + 6, PZ, CZ + 10)
                 + b(x - 9, x + 9, CY + hl - 6, CY + hl, PZ, CZ + 10))
        holders.append(body - groove + posts)
    holders = _union(holders)

    # Cells under test (not supplied), 21700 size
    cells = _union(Pos(x, CY, CZ) * Rot(90, 0, 0) * Cylinder(CR, CL) for x in cx)

    # 4 NTC thermistor clips on top of each cell
    ntc = _union(b(x - 4, x + 4, CY - 8, CY + 8, CZ + CR, CZ + CR + 5) for x in cx)

    # 5 Perforated steel guard (drawn as a frame and bars so the cells stay visible)
    gx0, gx1 = cx[0] - p["guard_margin_x"], cx[-1] + p["guard_margin_x"]
    gy0, gy1 = CY - p["guard_margin_y"], CY + p["guard_margin_y"]
    gz0, gz1 = PZ, CZ + CR + p["guard_clear"]
    bar = p["guard_bar"]
    g = []
    for gx in (gx0, gx1):
        for gy in (gy0, gy1):
            g.append(b(gx - bar / 2, gx + bar / 2, gy - bar / 2, gy + bar / 2, gz0, gz1))
    for gy in (gy0, gy1):
        g.append(b(gx0, gx1, gy - bar / 2, gy + bar / 2, gz1 - bar, gz1))
        g.append(b(gx0, gx1, gy - bar / 2, gy + bar / 2, gz0, gz0 + bar))
    k = 0
    while gx0 + k * 20 <= gx1:
        gx = gx0 + k * 20
        g.append(b(gx - 1, gx + 1, gy0, gy1, gz1 - bar, gz1))
        k += 1
    guard = _union(g)

    # 6 Charger modules and 7 channel sense and switch boards
    y0, y1 = p["charger_y"]
    chargers = _union(b(x - 12, x + 12, y0, y1, PZ, PZ + p["charger_h"]) for x in cx)
    y0, y1 = p["sense_y"]
    sense = _union(b(x - 12, x + 12, y0, y1, PZ, PZ + p["sense_h"]) for x in cx)

    # 9 Heatsink: spine along X, vertical fins normal to X (channels open to the top and back)
    hx0, hx1, hy0, hy1, hz0, hz1 = heatsink_extent(p)
    spine_y1 = hy0 + p["spine_t"]
    heatsink = b(hx0, hx1, hy0, spine_y1, hz0, hz1)
    for i in range(n_fins(p)):
        fx = hx0 + i * p["fin_pitch"]
        heatsink = heatsink + b(fx, fx + p["fin_t"], spine_y1, hy1, hz0, hz1)

    # 8 Load MOSFETs (TO-220) on the front face of the spine
    mosfets = _union(b(x - 5, x + 5, hy0 - 4.5, hy0, PZ + 14, PZ + 30)
                     + b(x - 4, x + 4, hy0 - 2, hy0, PZ + 3, PZ + 14) for x in cx)

    # 10 Fan shroud across the back of the fins and two 60 mm fans on it
    sy0 = hy1 + p["shroud_gap"]
    sy1 = sy0 + p["shroud_t"]
    shroud = b(hx0, hx1, sy0, sy1, hz0, PZ + p["fan"])
    shroud = shroud + b(hx0, hx1, hy1, sy0, hz1 - 1, hz1) + b(hx0 - 1, hx0, hy1, sy1, hz0, hz1)
    shroud = shroud + b(hx1, hx1 + 1, hy1, sy1, hz0, hz1)
    fans = None
    for fx in p["fan_x"]:
        fz = PZ + p["fan"] / 2
        shroud = shroud - Pos(fx, (sy0 + sy1) / 2, fz) * Rot(90, 0, 0) * Cylinder(27, 4)
        f = (b(fx - 30, fx + 30, sy1, sy1 + p["fan_t"], PZ, PZ + p["fan"])
             - Pos(fx, sy1 + p["fan_t"] / 2, fz) * Rot(90, 0, 0) * Cylinder(27, p["fan_t"] + 2)
             + Pos(fx, sy1 + p["fan_t"] / 2, fz) * Rot(90, 0, 0) * Cylinder(12, p["fan_t"] - 2))
        fans = f if fans is None else fans + f
    fans = fans + shroud

    # 11 Controller, 18 watchdog and undervoltage comparator board, 12 display, 13 inlet
    def blk(v):
        x0, x1, y0, y1, h = v
        return b(x0, x1, y0, y1, PZ, PZ + h)
    controller = blk(p["ctrl"])
    watchdog = blk(p["watchdog"])
    dx0, dx1, dy0, dy1, dh = p["display"]
    display = b(dx0, dx1, dy0, dy1, PZ, PZ + dh) + b(dx0 + 5, dx1 - 5, dy0 - 2, dy0, PZ + 18, PZ + dh - 3)
    inlet = blk(p["inlet"])

    # 14 Certified 12 V adapter on the bench
    ax0, ax1, ay0, ay1, ah = p["adapter"]
    adapter = b(ax0, ax1, ay0, ay1, 0, ah)

    # 15 Rest rack (printed), cols x rows cells upright; resting cells shown in part of the slots
    rp, x1r, y0r = p["rack_pitch"], p["rack_x1"], p["rack_y0"]
    nc, nr = p["rack_cols"], p["rack_rows"]
    rack = b(x1r - nc * rp - 8, x1r, y0r, y0r + nr * rp + 8, 0, p["rack_h"])
    rest = []
    for i in range(nc):
        for j in range(nr):
            x, y = x1r - 4 - rp / 2 - i * rp, y0r + 4 + rp / 2 + j * rp
            rack = rack - Pos(x, y, p["rack_h"] - 5) * Cylinder(CR + 0.8, 25)
            if (i + j) % 3 != 1:
                rest.append(Pos(x, y, 5 + CL / 2) * Cylinder(CR, CL))
    rest = _union(rest)

    return [
        ("Steel tray with ceramic fibre liner", tray, "#6B7280", 1, (0, 0, -170)),
        ("Base plate on standoffs", plate, "#D1D5DB", 2, (0, 0, -90)),
        ("Cell holders, four-wire contacts", holders, "#374151", 3, (0, 0, 0)),
        ("Cells under test (not supplied)", cells, "#A8B0BA", None, (0, 0, 70)),
        ("NTC thermistor clips", ntc, "#C2410C", 4, (0, -40, 140)),
        ("Perforated steel cell guard", guard, "#9CA3AF", 5, (0, -120, 240)),
        ("Charger modules, 1 A CC-CV", chargers, "#0F766E", 6, (0, 40, 50)),
        ("Channel sense and switch boards", sense, "#15803D", 7, (0, 80, 110)),
        ("Load MOSFETs", mosfets, "#1F2937", 8, (0, 120, 170)),
        ("Heatsink, vertical fins", heatsink, "#94A3B8", 9, (0, 190, 170)),
        ("Fans, 60 mm, on shroud", fans, "#4B5563", 10, (0, 290, 170)),
        ("Controller, ESP32-S3 class", controller, "#D4A017", 11, (120, 0, 60)),
        ("Display and buttons", display, "#38BDF8", 12, (130, -90, 40)),
        ("Power inlet, fuse and switch", inlet, "#991B1B", 13, (140, 120, 40)),
        ("12 V 5 A certified adapter", adapter, "#111827", 14, (220, 0, 0)),
        ("Self-discharge rest rack, 48 cells", rack, "#E5E7EB", 15, (150, -470, 0)),
        ("Cells resting (not supplied)", rest, "#A8B0BA", None, (150, -470, 0)),
        ("Watchdog and undervoltage board", watchdog, "#DC2626", 18, (130, -40, 80)),
    ]


UNIT_ITEMS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 18}   # parts inside the tray


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


if __name__ == "__main__":
    from build123d import export_step, export_stl
    root = Path(__file__).resolve().parents[1]
    (root / "step").mkdir(exist_ok=True); (root / "stl").mkdir(exist_ok=True)
    parts = build_parts()
    for name, shape in assemblies(parts).items():
        export_step(shape, str(root / "step" / f"{name}.step"))
        export_stl(shape, str(root / "stl" / f"{name}.stl"))
        bb = shape.bounding_box()
        print(f"{name:24s} {bb.size.X:6.1f} x {bb.size.Y:6.1f} x {bb.size.Z:6.1f} mm")
    e = envelope()
    print(f"grader unit envelope: {e[1]-e[0]:.0f} x {e[3]-e[2]:.0f} x {e[5]-e[4]:.0f} mm; "
          f"heatsink fins: {n_fins()}")
    print("part volumes (cm3):")
    for name, shape, _, bom, _ in parts:
        print(f"  {str(bom or '-'):>3s} {name:38s} {shape.volume / 1000:8.1f}")
    # Clash check inside the unit (pairwise intersection volume above 1 mm3)
    unit = [(n, s) for n, s, _, bom, _ in parts if bom in UNIT_ITEMS or n.startswith("Cells under test")]
    clashes = []
    for i in range(len(unit)):
        for j in range(i + 1, len(unit)):
            bi, bj = unit[i][1].bounding_box(), unit[j][1].bounding_box()
            if (bi.min.X > bj.max.X or bj.min.X > bi.max.X or bi.min.Y > bj.max.Y or bj.min.Y > bi.max.Y
                    or bi.min.Z > bj.max.Z or bj.min.Z > bi.max.Z):
                continue
            v = (unit[i][1] & unit[j][1]).volume
            if v > 1.0:
                clashes.append(f"{unit[i][0]} / {unit[j][0]}: {v:.0f} mm3")
    print("clashes: " + ("none" if not clashes else "; ".join(clashes)))
