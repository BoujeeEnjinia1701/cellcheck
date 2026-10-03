"""CellCheck product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a powder-coated steel tray with a rolled rim and
nameplate, ceramic fibre liner, aluminium base plate with channel numbers, eight four-wire cell
holders with nickel contacts, 18650 cells with ID labels, saddle thermistor clips, a slotted
perforated guard, populated charger and sense boards with lit status LEDs, TO-220 load MOSFETs
on the finned heatsink, two 60 mm fans with blades and finger guards, the controller, watchdog
perfboard, a lit display with three buttons and the power inlet with rocker and fuse holder.
Context: a silicone bench mat and three labelled bins holding matched groups A, B and C.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension and interface comes from PARAMS and the helpers in model.py
(model.py has no derived(); channel_x() and heatsink_extent() play that role here).
Axes as model.py: X across the front of the unit, Y from front (-Y) to back (+Y), Z up,
the bench top at z = 0.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build123d import (Align, Axis, Box, Compound, Cylinder, Plane, Pos, Rectangle, RectangleRounded,
                       RegularPolygon, Rot, SlotOverall, Sphere, Text, Vector, extrude, fillet)
from model import PARAMS, channel_x, guard_studs, heatsink_extent, n_fins, standoff_xy

TITLE = "CellCheck: bench grader for salvaged lithium cells"
RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); lit display at front "
             "right, eight test bays under the slotted guard, heatsink and fans at the back, graded cells "
             "in bins A, B and C in front"},
    {"name": "exploded", "groups": ["shell", "internal", "accessory"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): steel tray and liner, "
             "base plate, cell holders and contacts, cells and thermistor clips, guard, charger and sense "
             "boards, load MOSFETs, heatsink, fan shroud and fans, controller, watchdog board, display, "
             "power inlet, rest rack and 12 V adapter"},
    {"name": "detail", "groups": ["shell", "internal"], "explode": False, "el": 42, "az": -28,
     "note": "Detail view from the front right and higher above (about 42 deg elevation): cells in the "
             "four-wire holders under the guard, status LEDs on the sense boards and the lit display"},
]

# Colours (restrained product palette; accent from the kit)
C_TRAY = "#DADDE1"       # powder-coated steel
C_ACCENT = "#0F766E"
C_DARK = "#2B3038"       # housings
C_BLACK = "#1C1F24"
C_HOLDER = "#23272E"
C_ALU = "#C3C9D0"
C_STEEL = "#A9B0B8"
C_NICKEL = "#CDD1D6"
C_LINER = "#ECE7DC"
C_PCB_NAVY = "#1E3A5F"
C_PCB_GREEN = "#166534"
C_PCB_BLACK = "#1A1D21"
C_PERF = "#C9A66B"
C_LABEL = "#F4F4F0"
C_WARN = "#E8B931"
C_NTC = "#C2410C"
C_MAT = "#7C8691"
C_BIN = "#E6E8EB"
GRADE_COL = {"A": C_ACCENT, "B": "#2F5DA8", "C": "#B45309"}
WRAPS = ["#2F4F8F", "#2E7D6B", "#5B3F8C", "#A23B3B", "#2A2E35", "#5A8FC2"]

# 18650 cell shown in the bays (the holders take 18650 and 21700; model.py draws 21700 envelopes)
R18, L18 = 9.25, 65.0
FONT = str(HERE.parents[1] / ".kit/fonts/IBMPlexSans-SemiBold.ttf")

P = PARAMS
CX = channel_x(P)
PZ = P["plate_top"]
F = P["foot_h"]                                            # rubber feet lift the tray off the bench
CY = P["cell_y"]
GROOVE_Z = PZ + P["cell_axis_h"] - (P["cell_r"] + 0.5)   # bottom of the holder groove
CZ18 = GROOVE_Z + R18                                      # 18650 axis resting in the groove
OCCUPIED = [0, 1, 2, 4, 5, 6]                              # bays with a cell; 3 and 7 shown empty
DISCHARGING = 5                                            # channel shown on the discharge step


# ---------------------------------------------------------------- helpers
def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _b(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _prism(L, W, r, z0, h, x=0.0, y=0.0):
    """Rounded-rectangle prism in plan, from z0 up by h."""
    r = max(min(r, min(L, W) / 2 - 0.01), 0.01)
    return Pos(x, y, z0) * extrude(RectangleRounded(L, W, r), amount=h)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _text(txt, size, h):
    """Raised text on the local XY plane, centred at the origin, extruded +Z by h (None on failure)."""
    try:
        t = extrude(Text(txt, size, font_path=FONT, align=(Align.CENTER, Align.CENTER)), amount=h)
        return t if t.is_valid else None
    except Exception:
        return None


def _front(shape, x, y_face, z):
    """Place a local-XY feature (thickness +Z) on a face looking toward -Y at y_face."""
    return Pos(x, y_face, z) * Rot(90, 0, 0) * shape


def _cmp(shapes):
    shapes = [s for s in shapes if s is not None]
    return shapes[0] if len(shapes) == 1 else Compound(children=shapes)


def _cell_local(wrap_col):
    """18650 cell along local Z, negative end at z = 0. Returns {kind: shape}."""
    endc = 0.5
    wrap = Pos(0, 0, L18 / 2) * Cylinder(R18, L18 - 2 * endc)
    wrap = _fillet_try(wrap, wrap.edges(), [0.8, 0.5])
    pos = Pos(0, 0, L18 - endc / 2) * Cylinder(7.2, endc) + Pos(0, 0, L18 + 0.3) * Cylinder(3.4, 0.6)
    neg = Pos(0, 0, endc / 2) * Cylinder(7.8, endc)
    ring = Pos(0, 0, L18 - endc + 0.15) * (Cylinder(8.8, 0.3) - Cylinder(4.4, 1.0))
    label = Pos(0, 0, L18 * 0.42) * (Cylinder(R18 + 0.18, 16.0) - Cylinder(R18 - 0.2, 17.0))
    return {"wrap": wrap, "metal": pos + neg, "ring": ring, "label": label}


# ---------------------------------------------------------------- model
def product_parts(P=PARAMS):
    out = []
    buckets = {}

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    def collect(key, shape):
        buckets.setdefault(key, []).append(shape)

    def flush(key, name, color, material, bom, group, explode):
        if buckets.get(key):
            add(name, _cmp(buckets[key]), color, material, bom, group, explode)

    L, W, H, t = P["tray_l"], P["tray_w"], P["tray_h"], P["tray_t"]
    cx = CX

    # ---- 1 Steel tray: rounded corners, rolled rim, intake slots, nameplate; ceramic fibre liner
    rc = 10.0
    tray = _prism(L, W, rc, 0, H)
    tray = _fillet_try(tray, _bottom(tray), [3.0, 2.0, 1.0])
    tray -= _prism(L - 2 * t, W - 2 * t, rc - t, t, H + 5)
    rim = _prism(L + 3.0, W + 3.0, rc + 1.5, H - 2.5, 2.5) - _prism(L - 2 * t, W - 2 * t, rc - t, H - 5, 10)
    rim = _fillet_try(rim, _top(rim), [1.0, 0.6])
    tray += rim
    for fx in P["fan_x"]:
        z0, z1 = P["intake_z0"], P["intake_z1"]
        slot = Pos(fx, W / 2, (z0 + z1) / 2) * Rot(90, 0, 0) * extrude(
            RectangleRounded(P["intake_w"], z1 - z0, 4.0), amount=8, both=True)
        tray -= slot
    add("Steel tray, powder coated", tray, C_TRAY, "painted", 1, "shell", (0, 0, -170))
    liner = _prism(L - 2 * t, W - 2 * t, rc - t, t, P["liner_t"])
    add("Ceramic fibre liner", liner, C_LINER, "fabric", 1, "shell", (0, 0, -130))

    plate_name = _prism(112, 17, 3.0, 0, 0.6)
    plate_name = _fillet_try(plate_name, _top(plate_name), [0.3, 0.2])
    add("Nameplate", _front(plate_name, -140, -W / 2, 23), C_ACCENT, "painted", None, "shell", (0, 0, -170))
    txt = _text("CELLCHECK", 8.5, 0.3)
    if txt is not None:
        add("Nameplate lettering", _front(Pos(0, 0, 0.6) * txt, -140, -W / 2, 23), "#F5F7F7", "plastic",
            None, "shell", (0, 0, -170))
    warn = _prism(64, 14, 1.5, 0, 0.25)
    add("Warning label, lithium cells", _front(warn, 110, -W / 2, 23), C_WARN, "paper", 17, "shell",
        (0, 0, -170))
    wt = _text("LI-ION: ATTENDED USE ONLY", 4.2, 0.15)
    if wt is not None:
        add("Warning label print", _front(Pos(0, 0, 0.25) * wt, 110, -W / 2, 23), C_BLACK, "plastic", 17,
            "shell", (0, 0, -170))

    # ---- 2 Base plate on standoffs, fixing screws, channel numbers
    pl, pw = P["plate_l"] / 2, P["plate_w"] / 2
    plate = _prism(2 * pl, 2 * pw, 6.0, PZ - P["plate_t"], P["plate_t"])
    plate = _fillet_try(plate, _top(plate), [0.6, 0.3])
    seal_s = []
    for x in cx:                                      # two wire slots per channel, sealed with silicone
        for yc in (P["down_slot_y"], P["up_slot_y"]):
            plate -= _b(x - P["slot_w"] / 2, x + P["slot_w"] / 2, yc - P["slot_d"] / 2, yc + P["slot_d"] / 2,
                        PZ - P["plate_t"] - 1, PZ + 1)
            sl = _b(x - P["slot_w"] / 2 - 0.3, x + P["slot_w"] / 2 + 0.3, yc - P["slot_d"] / 2 - 0.3,
                    yc + P["slot_d"] / 2 + 0.3, PZ - P["plate_t"], PZ + P["seal_bead"])
            seal_s.append(_fillet_try(sl, _top(sl), [1.0, 0.6]))
    add("Base plate, aluminium", plate, C_ALU, "metal", 2, "internal", (0, 0, -90))
    z_floor = t + P["liner_t"]
    std = []
    heads = []
    for sx, sy in standoff_xy(P):                     # six standoffs, every screw head reachable from above
        hgt = PZ - P["plate_t"] - z_floor
        std.append(Pos(sx, sy, z_floor) * extrude(RegularPolygon(4.6, 6), amount=hgt))
        hd = Pos(sx, sy, PZ + 1.0) * Cylinder(3.6, 2.0)
        hd = _fillet_try(hd, _top(hd), [0.8, 0.5])
        hd -= Pos(sx, sy, PZ + 2.0) * (Box(4.0, 0.8, 1.6) + Box(0.8, 4.0, 1.6))
        heads.append(hd)
    add("Silicone slot seals", _cmp(seal_s), "#D97706", "rubber", 16, "internal", (0, 0, -40))
    add("Standoffs", _cmp(std), C_ALU, "metal", 2, "internal", (0, 0, -120))
    add("Plate screws", _cmp(heads), C_NICKEL, "metal", 2, "internal", (0, 0, -40))
    nums = []
    for i, x in enumerate(cx):
        tx = _text(str(i + 1), 7.0, 0.3)
        if tx is not None:
            nums.append(Pos(x, -121, PZ) * tx)
    if nums:
        add("Channel number labels", _cmp(nums), C_LABEL, "paper", 17, "internal", (0, 0, -90))

    # ---- 3 Cell holders with four-wire contacts (force and sense at each end)
    hw, hl = P["holder_w"] / 2, P["holder_l"] / 2
    CZ = PZ + P["cell_axis_h"]
    bodies, contacts, tabs = [], [], []
    for x in cx:
        body = _b(x - hw, x + hw, CY - hl, CY + hl, PZ, PZ + P["holder_h"])
        body = _fillet_try(body, body.edges().filter_by(Axis.Z), [2.0, 1.0])
        body = _fillet_try(body, _top(body), [1.0, 0.5])
        body -= Pos(x, CY, CZ) * Rot(90, 0, 0) * Cylinder(P["cell_r"] + 0.5, P["cell_l"] + 6)
        for ys in (-1, 1):
            y_out = CY + ys * hl
            y_in = CY + ys * (hl - 6)
            post = _b(x - 9, x + 9, min(y_out, y_in), max(y_out, y_in), PZ, CZ + 10)
            post = _fillet_try(post, post.edges().filter_by(Axis.Z), [1.5, 0.8])
            post = _fillet_try(post, _top(post), [1.2, 0.6])
            body += post
            face = y_in
            tip = CY + ys * L18 / 2
            for dx in (-3.6, 3.6):
                c = Pos(x + dx, (face + tip) / 2, CZ18) * Rot(90, 0, 0) * Cylinder(2.2, abs(face - tip))
                contacts.append(c)
                tabs.append(_b(x + dx - 1.5, x + dx + 1.5, y_out - ys * 3.5 - 0.4, y_out - ys * 3.5 + 0.4,
                               CZ + 10, CZ + 14))
        bodies.append(body)
    add("Cell holders", _cmp(bodies), C_HOLDER, "plastic", 3, "internal", (0, 0, 0))
    add("Holder contacts, nickel", _cmp(contacts), C_NICKEL, "metal", 3, "internal", (0, 0, 0))
    add("Holder solder tabs", _cmp(tabs), C_NICKEL, "metal", 3, "internal", (0, 0, 20))

    # ---- cells under test (18650, not supplied), with ID labels
    for k, i in enumerate(OCCUPIED):
        col = WRAPS[k % len(WRAPS)]
        c = _cell_local(col)
        loc = Pos(cx[i], CY + L18 / 2, CZ18) * Rot(90, 0, 0)
        collect(("bay", col), loc * c["wrap"])
        collect(("bay", "metal"), loc * c["metal"])
        collect(("bay", "ring"), loc * c["ring"])
        collect(("bay", "label"), loc * c["label"])
    for col in WRAPS:
        flush(("bay", col), f"Cell wraps under test {col}", col, "painted", None, "internal", (0, 0, 70))
    flush(("bay", "metal"), "Cell terminals under test", C_NICKEL, "metal", None, "internal", (0, 0, 70))
    flush(("bay", "ring"), "Cell insulator rings under test", C_LABEL, "paper", 17, "internal", (0, 0, 70))
    flush(("bay", "label"), "Cell ID labels under test", C_LABEL, "paper", 17, "internal", (0, 0, 70))

    # ---- 4 NTC thermistor clips: saddles on the cells; parked on the back post of empty bays
    clips, leads = [], []
    for i, x in enumerate(cx):
        if i in OCCUPIED:
            clip = _b(x - 4, x + 4, CY - 8, CY + 8, CZ18 + R18 - 3.0, CZ18 + R18 + 3.5)
            clip = _fillet_try(clip, clip.edges().filter_by(Axis.Y), [1.5, 0.8])
            clip -= Pos(x, CY, CZ18) * Rot(90, 0, 0) * Cylinder(R18 + 0.05, 30)
            lead = Pos(x, CY + 14, CZ18 + R18 + 1.5) * Rot(90, 0, 0) * Cylinder(0.9, 12)
        else:
            z0 = CZ + 10
            clip = _b(x - 8, x + 8, CY + hl - 5, CY + hl - 1, z0, z0 + 4)
            clip = _fillet_try(clip, clip.edges().filter_by(Axis.X), [1.2, 0.6])
            lead = Pos(x + 12, CY + hl - 3, z0 + 2) * Rot(0, 90, 0) * Cylinder(0.9, 8)
        clips.append(clip)
        leads.append(lead)
    add("NTC thermistor clips", _cmp(clips), C_NTC, "plastic", 4, "internal", (0, -40, 140))
    add("NTC leads", _cmp(leads), C_BLACK, "rubber", 4, "internal", (0, -40, 140))

    # ---- 5 Perforated steel guard: slotted top, front, back and ends; foot flanges with screws
    gx0, gx1 = cx[0] - P["guard_margin_x"], cx[-1] + P["guard_margin_x"]
    gy0, gy1 = CY - P["guard_margin_y"], CY + P["guard_margin_y"]
    gz0, gz1 = PZ, CZ + P["cell_r"] + P["guard_clear"]
    gs = 1.0      # sheet thickness shown (0.8 mm in the BOM, thickened for the render)
    gl, gw, gh = gx1 - gx0, gy1 - gy0, gz1 - gz0
    gxc, gyc = (gx0 + gx1) / 2, (gy0 + gy1) / 2

    def slotted(a, b, slot_l, rot, pitch, rows, margin=7.0):
        sk = Rectangle(a, b)
        cols = int((a - 2 * margin) // pitch)
        x_start = -(cols - 1) * pitch / 2
        row_pitch = (b - 2 * margin) / rows
        for r in range(rows):
            yr = -b / 2 + margin + row_pitch * (r + 0.5)
            off = pitch / 2 if r % 2 else 0.0
            n = cols - (1 if r % 2 else 0)
            for c in range(n):
                sk -= Pos(x_start + off + c * pitch, yr) * Rot(0, 0, rot) * SlotOverall(slot_l, 4.6)
        return sk

    top = Pos(gxc, gyc, gz1 - gs) * extrude(slotted(gl, gw, 19.0, 90, 7.5, 4), amount=gs)
    fr = extrude(slotted(gl, gh, 15.0, 90, 7.5, 2), amount=gs)
    front = Pos(gxc, gy0, gz0 + gh / 2) * Rot(90, 0, 0) * Pos(0, 0, -gs) * fr
    back = Pos(gxc, gy1, gz0 + gh / 2) * Rot(90, 0, 0) * fr
    en = extrude(slotted(gh, gw, 15.0, 0, 7.5, 3), amount=gs)
    left = Pos(gx0, gyc, gz0 + gh / 2) * Rot(0, -90, 0) * Pos(0, 0, -gs) * en
    right = Pos(gx1, gyc, gz0 + gh / 2) * Rot(0, -90, 0) * en
    guard = top + front + back + left + right
    gfl = P["guard_flange"]
    fl_l = _b(gx0 - gfl, gx0 + 0.01, gy0, gy1, gz0, gz0 + gs)
    fl_r = _b(gx1 - 0.01, gx1 + gfl, gy0, gy1, gz0, gz0 + gs)
    fl_l = _fillet_try(fl_l, fl_l.edges().filter_by(Axis.Z), [2.5, 1.0])
    fl_r = _fillet_try(fl_r, fl_r.edges().filter_by(Axis.Z), [2.5, 1.0])
    guard += fl_l + fl_r
    add("Perforated steel cell guard", guard, C_STEEL, "metal", 5, "shell", (0, -120, 240))
    gscr = []
    for gx, gy in guard_studs(P):                     # two knurled M4 thumb screws through the end flanges
        hd = Pos(gx, gy, gz0 + gs + 3.0) * Cylinder(7.0, 6.0)
        hd = _fillet_try(hd, _top(hd), [1.2, 0.6])
        for k in range(12):
            hd -= Pos(gx, gy, gz0 + gs + 3.0) * Rot(0, 0, k * 30) * Pos(7.0, 0, 0) * Cylinder(0.6, 6.2)
        gscr.append(hd)
    add("Guard thumb screws", _cmp(gscr), C_NICKEL, "metal", 20, "shell", (0, -120, 300))

    # ---- 6 Charger modules (TP5100 class)
    y0, y1 = P["charger_y"]
    pcbs, dark, caps, term = [], [], [], []
    for x in cx:
        pcbs.append(_prism(24, y1 - y0, 1.0, PZ + P["board_lift"], 1.6, x=x, y=(y0 + y1) / 2))
        for sx in (-9.5, 9.5):
            for sy in (y0 + 3, y1 - 3):
                pcbs.append(Pos(x + sx, sy, PZ + P["board_lift"] / 2) * Cylinder(1.6, P["board_lift"]))
        zt = PZ + P["board_lift"] + 1.6
        ind = _b(x - 4, x + 4, y0 + 12, y0 + 20, zt, zt + 4.6)
        dark.append(_fillet_try(ind, ind.edges().filter_by(Axis.Z), [1.2, 0.6]))
        dark.append(_b(x - 7.5, x - 3.5, y0 + 4, y0 + 9, zt, zt + 1.1))
        caps.append(Pos(x + 6.5, y0 + 7, zt + 2.9) * Cylinder(3.0, 5.8))
        term.append(_b(x - 10, x + 10, y1 - 5.5, y1 - 0.5, zt, zt + 5.0))
    add("Charger module PCBs", _cmp(pcbs), C_PCB_NAVY, "plastic", 6, "internal", (0, 40, 50))
    add("Charger inductors and ICs", _cmp(dark), C_BLACK, "plastic", 6, "internal", (0, 40, 50))
    add("Charger capacitors", _cmp(caps), C_NICKEL, "metal", 6, "internal", (0, 40, 50))
    add("Charger terminal blocks", _cmp(term), "#2F7A4B", "plastic", 6, "internal", (0, 40, 50))

    # ---- 7 Channel sense and switch boards, with status LEDs
    y0, y1 = P["sense_y"]
    spcb, schips, shunts, led_g, led_a, led_off = [], [], [], [], [], []
    for i, x in enumerate(cx):
        spcb.append(_prism(24, y1 - y0, 1.0, PZ + P["board_lift"], 1.6, x=x, y=(y0 + y1) / 2))
        for sx in (-9.5, 9.5):
            for sy in (y0 + 3, y1 - 3):
                spcb.append(Pos(x + sx, sy, PZ + P["board_lift"] / 2) * Cylinder(1.5, P["board_lift"]))
        zt = PZ + P["board_lift"] + 1.6
        schips.append(_b(x - 2, x + 2, y0 + 8, y0 + 12, zt, zt + 1.0))
        schips.append(_b(x - 9, x - 3, y0 + 12, y0 + 17, zt, zt + 1.4))
        schips.append(_b(x + 5, x + 11, y1 - 5, y1 - 2.5, zt, zt + 2.5))
        shunts.append(_b(x - 3.5, x + 3.5, y0 + 2.5, y0 + 5.0, zt, zt + 1.2))
        led = _b(x + 5.5, x + 9.0, y0 + 3.0, y0 + 5.5, zt, zt + 1.3)
        (led_a if i == DISCHARGING else led_g if i in OCCUPIED else led_off).append(led)
    add("Sense board PCBs", _cmp(spcb), C_PCB_GREEN, "plastic", 7, "internal", (0, 80, 110))
    add("Sense board chips and headers", _cmp(schips + led_off), C_BLACK, "plastic", 7, "internal",
        (0, 80, 110))
    add("Current shunts", _cmp(shunts), C_NICKEL, "metal", 7, "internal", (0, 80, 110))
    add("Status LEDs, charging (lit)", _cmp(led_g), "#34D399", "emissive", 7, "internal", (0, 80, 110))
    add("Status LED, discharging (lit)", _cmp(led_a), "#FBBF24", "emissive", 7, "internal", (0, 80, 110))

    # ---- 8 Load MOSFETs (TO-220) on the spine; 9 heatsink; 10 shroud and fans
    hx0, hx1, hy0, hy1, hz0, hz1 = heatsink_extent(P)
    bodies, mtabs, legs, mscr = [], [], [], []
    for x in cx:
        bd = _b(x - 5, x + 5, hy0 - 4.5, hy0 - 1.3, PZ + 14, PZ + 23.5)
        bodies.append(_fillet_try(bd, bd.edges().filter_by(Axis.Y), [0.6, 0.3]))
        tb = _b(x - 5, x + 5, hy0 - 1.3, hy0, PZ + 14, PZ + 30)
        tb -= Pos(x, hy0 - 0.65, PZ + 26.5) * Rot(90, 0, 0) * Cylinder(1.8, 3)
        mtabs.append(tb)
        for dx in (-2.54, 0, 2.54):
            legs.append(_b(x + dx - 0.4, x + dx + 0.4, hy0 - 3.2, hy0 - 2.6, PZ + 3, PZ + 14))
        s = Pos(x, hy0 - 2.3, PZ + 26.5) * Rot(90, 0, 0) * Cylinder(2.7, 2.0)
        s = _fillet_try(s, s.edges().sort_by(Axis.Y)[:1], [0.5, 0.3])
        mscr.append(s)
    add("Load MOSFET bodies", _cmp(bodies), C_BLACK, "plastic", 8, "internal", (0, 120, 170))
    add("Load MOSFET tabs and leads", _cmp(mtabs + legs), C_NICKEL, "metal", 8, "internal", (0, 120, 170))
    add("MOSFET clamp screws", _cmp(mscr), C_NICKEL, "metal", 8, "internal", (0, 95, 170))

    spine_y1 = hy0 + P["spine_t"]
    hs = _b(hx0, hx1, hy0, spine_y1, hz0, hz1)
    for i in range(n_fins(P)):
        fx = hx0 + i * P["fin_pitch"]
        hs += _b(fx, fx + P["fin_t"], spine_y1 - 0.01, hy1, hz0, hz1)
    add("Heatsink, aluminium", hs, "#BFC5CC", "metal", 9, "internal", (0, 190, 170))

    sy0 = hy1 + P["shroud_gap"]
    sy1 = sy0 + P["shroud_t"]
    fz = PZ + P["fan"] / 2
    shroud = _b(hx0, hx1, sy0, sy1, hz0, PZ + P["fan"])
    shroud += _b(hx0, hx1, hy1, sy0, hz1 - 1, hz1) + _b(hx0 - 1, hx0, hy1, sy1, hz0, hz1)
    shroud += _b(hx1, hx1 + 1, hy1, sy1, hz0, hz1)
    for fx in P["fan_x"]:
        shroud -= Pos(fx, (sy0 + sy1) / 2, fz) * Rot(90, 0, 0) * Cylinder(27, 4)
    add("Fan shroud, aluminium", shroud, C_ALU, "metal", 10, "internal", (0, 250, 170))

    frames, blades, fguards, hubs = [], [], [], []
    ft = P["fan_t"]
    for fx in P["fan_x"]:
        loc = Pos(fx, sy1 + ft / 2, fz) * Rot(-90, 0, 0)          # local Z -> world +Y
        fr_ = extrude(RectangleRounded(60, 60, 4.0), amount=ft / 2, both=True)
        fr_ -= Cylinder(28.5, ft + 2)
        for sx in (-25, 25):
            for sy in (-25, 25):
                fr_ -= Pos(sx, sy, 0) * Cylinder(2.2, ft + 2)
        frames.append(loc * fr_)
        hub = Cylinder(12.0, ft - 2)
        hub = _fillet_try(hub, hub.edges(), [1.5, 0.8])
        hubs.append(loc * hub)
        bl = None
        for k in range(7):
            b = Rot(0, 0, k * 360 / 7 + 10) * Pos(20.0, 0, 0) * Rot(32, 0, 0) * Box(16.5, 11.0, 1.4)
            bl = b if bl is None else bl + b
        bl = bl & Cylinder(27.8, ft - 2.5)
        blades.append(loc * bl)
        g = None
        for r in (10.0, 17.0, 24.0):
            ring = Cylinder(r + 0.6, 1.2) - Cylinder(r - 0.6, 2.0)
            g = ring if g is None else g + ring
        for a in (45, 135):
            g += Rot(0, 0, a) * Box(58.0, 1.2, 1.2)
        g += Cylinder(4.0, 1.2)
        fguards.append(Pos(fx, sy1 + ft + 0.6, fz) * Rot(-90, 0, 0) * g)
    add("Fan frames", _cmp(frames), C_BLACK, "plastic", 10, "internal", (0, 290, 170))
    add("Fan hubs", _cmp(hubs), "#2E333B", "plastic", 10, "internal", (0, 290, 170))
    add("Fan blades", _cmp(blades), "#2A2E35", "plastic", 10, "internal", (0, 290, 170))
    add("Fan finger guards", _cmp(fguards), "#B8BEC6", "metal", 10, "internal", (0, 320, 170))

    # ---- 11 Controller (ESP32-S3 class)
    x0, x1, y0, y1, h = P["ctrl"]
    xc, yc = (x0 + x1) / 2, (y0 + y1) / 2
    cp = [_prism(x1 - x0, y1 - y0, 2.0, PZ + 4.0, 1.6, x=xc, y=yc)]
    for sx in (x0 + 3, x1 - 3):
        for sy in (y0 + 3, y1 - 3):
            cp.append(Pos(sx, sy, PZ + 2.0) * Cylinder(1.8, 4.0))
    zt = PZ + 5.6
    add("Controller PCB", _cmp(cp), C_PCB_BLACK, "plastic", 11, "internal", (120, 0, 60))
    cmet = [_b(xc - 9, xc + 9, yc - 2, yc + 20, zt, zt + 3.2),
            _b(xc - 4.5, xc + 4.5, y0 - 1, y0 + 6, zt, zt + 3.2),
            _b(xc - 6, xc + 6, y1 - 12, y1 - 1, zt, zt + 1.5)]
    add("Controller module can, USB-C and card slot", _cmp(cmet), C_NICKEL, "metal", 11, "internal",
        (120, 0, 60))
    hdr = [_b(x0 + 1.5, x0 + 4.0, y0 + 8, y1 - 8, zt, PZ + h),
           _b(x1 - 4.0, x1 - 1.5, y0 + 8, y1 - 8, zt, PZ + h),
           _b(xc - 5, xc + 3, yc - 12, yc - 6, zt, zt + 1.0)]
    add("Controller headers and chips", _cmp(hdr), C_BLACK, "plastic", 11, "internal", (120, 0, 60))

    # ---- 18 Watchdog and undervoltage perfboard
    x0, x1, y0, y1, h = P["watchdog"]
    xc, yc = (x0 + x1) / 2, (y0 + y1) / 2
    wp = [_prism(x1 - x0, y1 - y0, 1.0, PZ + 3.0, 1.6, x=xc, y=yc)]
    for sx in (x0 + 3, x1 - 3):
        for sy in (y0 + 3, y1 - 3):
            wp.append(Pos(sx, sy, PZ + 1.5) * Cylinder(1.6, 3.0))
    add("Watchdog perfboard", _cmp(wp), C_PERF, "plastic", 18, "internal", (130, -40, 80))
    zt = PZ + 4.6
    dips = [_b(xc - 19, xc - 9, yc - 3.25, yc + 3.25, zt, zt + 3.3),
            _b(xc - 5, xc + 5, yc - 3.25, yc + 3.25, zt, zt + 3.3),
            _b(xc + 8, xc + 21, yc - 3.25, yc + 3.25, zt, zt + 3.3)]
    add("Watchdog and comparator ICs", _cmp(dips), C_BLACK, "plastic", 18, "internal", (130, -40, 80))

    # ---- 12 Display and buttons: charcoal stand, dark glass, lit channel rows
    dx0, dx1, dy0, dy1, dh = P["display"]
    dxc = (dx0 + dx1) / 2
    stand = _b(dx0, dx1, dy0, dy1, PZ, PZ + dh)
    stand = _fillet_try(stand, stand.edges().filter_by(Axis.Z), [3.0, 1.5])
    stand = _fillet_try(stand, _top(stand), [2.0, 1.0])
    add("Display stand", stand, C_DARK, "plastic", 12, "shell", (130, -90, 40))
    bez = _b(dx0 + 5, dx1 - 5, dy0 - 2, dy0 + 0.5, PZ + 18, PZ + dh - 3)
    bez = _fillet_try(bez, bez.edges().filter_by(Axis.Y), [1.5, 0.8])
    add("Display glass", bez, "#12161B", "screen", 12, "shell", (130, -90, 40))
    zs0, zs1 = PZ + 21, PZ + dh - 6
    yface = dy0 - 2.0
    ui_hdr = _b(dxc - 21, dxc + 21, yface - 0.2, yface + 0.05, zs1 - 3.2, zs1 - 1.0)
    rows_g, rows_a, rows_dim = [], [], []
    rh = (zs1 - 5.0 - zs0) / 8
    prog = [0.85, 0.6, 0.95, 0.0, 0.4, 0.55, 0.75, 0.0]
    for i in range(8):
        z = zs1 - 5.0 - (i + 0.5) * rh
        full = 36.0
        rows_dim.append(_b(dxc - 18, dxc - 18 + full, yface - 0.1, yface + 0.05, z - rh * 0.28, z + rh * 0.28))
        rows_dim.append(_b(dxc - 22, dxc - 20, yface - 0.2, yface + 0.05, z - rh * 0.28, z + rh * 0.28))
        if i in OCCUPIED:
            seg = _b(dxc - 18, dxc - 18 + full * prog[i], yface - 0.2, yface + 0.05, z - rh * 0.28, z + rh * 0.28)
            (rows_a if i == DISCHARGING else rows_g).append(seg)
    add("Display screen, header (lit)", ui_hdr, "#D8F3EF", "emissive", 12, "shell", (130, -90, 40))
    add("Display screen, charge bars (lit)", _cmp(rows_g), "#34D399", "emissive", 12, "shell", (130, -90, 40))
    add("Display screen, discharge bar (lit)", _cmp(rows_a), "#FBBF24", "emissive", 12, "shell",
        (130, -90, 40))
    add("Display screen, idle rows (lit)", _cmp(rows_dim), "#3B4A57", "emissive", 12, "shell", (130, -90, 40))
    btns, btn_acc = [], None
    for k, bx in enumerate((dxc - 16, dxc, dxc + 16)):
        b = Pos(bx, (dy0 + dy1) / 2, PZ + dh + 1.0) * Cylinder(3.4, 2.4)
        b = _fillet_try(b, _top(b), [0.9, 0.5])
        if k == 1:
            btn_acc = b
        else:
            btns.append(b)
    add("Display buttons", _cmp(btns), "#3A4049", "rubber", 12, "shell", (130, -90, 60))
    add("Display select button", btn_acc, C_ACCENT, "plastic", 12, "shell", (130, -90, 60))

    # ---- 13 Power inlet: housing, rocker switch, fuse holder, DC jack, power LED
    x0, x1, y0, y1, h = P["inlet"]
    xc, yc = (x0 + x1) / 2, (y0 + y1) / 2
    inl = _b(x0, x1, y0, y1, PZ, PZ + h)
    inl = _fillet_try(inl, inl.edges().filter_by(Axis.Z), [3.0, 1.5])
    inl = _fillet_try(inl, _top(inl), [1.5, 0.8])
    inl -= _b(xc - 13, xc + 1, yc - 8, yc + 8, PZ + h - 2, PZ + h + 1)
    add("Power inlet housing", inl, C_DARK, "plastic", 13, "internal", (140, 120, 40))
    rock = _b(xc - 12, xc, yc - 7, yc + 7, PZ + h - 2, PZ + h + 1.2)
    rock = _fillet_try(rock, _top(rock), [0.8, 0.4])
    rock -= Pos(xc - 3, yc, PZ + h + 1.5) * Rot(0, 12, 0) * Box(20, 16, 1.2)
    add("Rocker switch", rock, C_BLACK, "plastic", 13, "internal", (140, 120, 40))
    fh = Pos(xc + 13, yc - 6, PZ + h + 2.0) * Cylinder(5.0, 4.0)
    fh = _fillet_try(fh, _top(fh), [1.0, 0.5])
    fh -= Pos(xc + 13, yc - 6, PZ + h + 4.0) * Box(6.0, 1.0, 1.4)
    add("Fuse holder cap", fh, C_BLACK, "plastic", 13, "internal", (140, 120, 40))
    jack = Pos(x1 + 1.5, 105, PZ + 14) * Rot(0, 90, 0) * (Cylinder(4.5, 3.0) - Cylinder(3.0, 4.0))
    add("DC jack", jack, C_NICKEL, "metal", 13, "internal", (140, 120, 40))
    pled = Pos(xc + 13, yc + 9, PZ + h + 0.4) * Cylinder(1.6, 1.0)
    add("Power LED (lit)", pled, "#34D399", "emissive", 13, "internal", (140, 120, 40))

    # ---- 14 Certified 12 V adapter with cable to the inlet (accessory)
    ax0, ax1, ay0, ay1, ah = P["adapter"]
    ad = _b(ax0, ax1, ay0, ay1, 0, ah)
    ad = _fillet_try(ad, ad.edges().filter_by(Axis.X), [6.0, 4.0, 2.0])
    ad = _fillet_try(ad, ad.edges().filter_by(Axis.Y), [3.0, 1.5])
    add("12 V 5 A certified adapter", ad, "#16181C", "plastic", 14, "accessory", (220, 0, 0))
    lab = _prism(70, 34, 2.0, ah - 0.05, 0.3, x=(ax0 + ax1) / 2, y=(ay0 + ay1) / 2)
    add("Adapter rating label", lab, "#D9DDE2", "paper", 14, "accessory", (220, 0, 0))
    pts = [(ax0 - 6, 50, 14), (ax0 - 20, 58, 3), (240, 80, 3), (236, 98, 20), (231, 105, 50),
           (220, 105, 50), (212, 105, PZ + F + 20), (x1 + 3.5, 105, PZ + F + 14)]
    cab = None
    for a, b in zip(pts[:-1], pts[1:]):
        va, vb = Vector(*a), Vector(*b)
        d = vb - va
        seg = Cylinder(2.2, d.length, align=(Align.CENTER, Align.CENTER, Align.MIN))
        seg = Plane(origin=va, z_dir=d.normalized()).location * seg
        seg += Pos(*b) * Sphere(2.2)
        cab = seg if cab is None else cab + seg
    cab += Pos(ax0 - 3, 50, 14) * Rot(0, 90, 0) * Cylinder(4.0, 7.0)
    cab += Pos(ax1 + 3, 50, 14) * Rot(0, 90, 0) * Cylinder(4.0, 7.0)
    cab += Pos(ax1 + 45, 50, 14) * Rot(0, 90, 0) * Cylinder(3.0, 80.0)
    add("Adapter cables", cab, C_BLACK, "rubber", 14, "accessory", (220, 0, 0))

    # ---- 15 Rest rack with numbered columns and resting 18650 cells (accessory)
    rp, x1r, y0r = P["rack_pitch"], P["rack_x1"], P["rack_y0"]
    nc, nr = P["rack_cols"], P["rack_rows"]
    rx0, rx1, ry1 = x1r - nc * rp - 8, x1r, y0r + nr * rp + 8
    rack = _b(rx0, rx1, y0r, ry1, 0, P["rack_h"])
    rack = _fillet_try(rack, rack.edges().filter_by(Axis.Z), [6.0, 3.0])
    rack = _fillet_try(rack, _top(rack), [1.5, 0.8])
    k = 0
    for i in range(nc):
        for j in range(nr):
            x, y = x1r - 4 - rp / 2 - i * rp, y0r + 4 + rp / 2 + j * rp
            rack -= Pos(x, y, P["rack_h"] - 5) * Cylinder(P["cell_r"] + 0.8, 25)
            if (i + j) % 3 != 1:
                col = WRAPS[k % len(WRAPS)]
                k += 1
                c = _cell_local(col)
                loc = Pos(x, y, 5.0)
                collect(("rack", col), loc * c["wrap"])
                collect(("rack", "metal"), loc * c["metal"])
                collect(("rack", "ring"), loc * c["ring"])
                collect(("rack", "label"), loc * c["label"])
    add("Self-discharge rest rack", rack, "#EEF0F2", "plastic", 15, "accessory", (150, -470, 0))
    rn = []
    for i in range(nc):
        tx = _text(str(nc - i), 7.0, 0.4)
        if tx is not None:
            rn.append(_front(tx, x1r - 4 - rp / 2 - i * rp, y0r, P["rack_h"] / 2))
    if rn:
        add("Rest rack column numbers", _cmp(rn), C_ACCENT, "plastic", 15, "accessory", (150, -470, 0))
    for col in WRAPS:
        flush(("rack", col), f"Cell wraps resting {col}", col, "painted", None, "accessory", (150, -470, 0))
    flush(("rack", "metal"), "Cell terminals resting", C_NICKEL, "metal", None, "accessory", (150, -470, 0))
    flush(("rack", "ring"), "Cell insulator rings resting", C_LABEL, "paper", 17, "accessory", (150, -470, 0))
    flush(("rack", "label"), "Cell ID labels resting", C_LABEL, "paper", 17, "accessory", (150, -470, 0))

    # ---- context: silicone bench mat and three labelled bins with matched groups A, B, C
    mat = _prism(504, 424, 12.0, -1.5, 1.5, x=0, y=-46)
    add("Silicone bench mat", mat, C_MAT, "rubber", None, "context", (0, 0, 0))
    bins, plates, letters = [], [], []
    bw, bd, bh, bt = 100.0, 72.0, 34.0, 2.0
    by_ = -W / 2 - 18 - bd / 2
    for n, (g, bxc) in enumerate(zip("ABC", (-150.0, -40.0, 70.0))):
        bn = _prism(bw, bd, 6.0, 0, bh, x=bxc, y=by_)
        bn = _fillet_try(bn, _bottom(bn), [2.5, 1.5])
        bn -= _prism(bw - 2 * bt, bd - 2 * bt, 6.0 - bt, bt, bh, x=bxc, y=by_)
        lip = _prism(bw + 2, bd + 2, 7.0, bh - 2, 2, x=bxc, y=by_) - _prism(bw - 2 * bt, bd - 2 * bt, 4.0, bh - 5, 8, x=bxc, y=by_)
        bn += lip
        bins.append(bn)
        pl_ = _prism(26, 16, 2.0, 0, 0.6)
        plates.append((g, _front(pl_, bxc, by_ - bd / 2 - 1.0, bh / 2 + 1)))
        tx = _text(g, 10.0, 0.3)
        if tx is not None:
            letters.append(_front(Pos(0, 0, 0.6) * tx, bxc, by_ - bd / 2 - 1.0, bh / 2 + 1))
        ncell = 3 if g != "C" else 2
        for m in range(ncell):
            col = WRAPS[(n * 2 + m) % len(WRAPS)]
            c = _cell_local(col)
            yy = by_ - (ncell - 1) * 9.6 + m * 19.2
            loc = Pos(bxc - L18 / 2 - 0.3, yy, bt + R18) * Rot(0, 90, 0)
            collect(("bin", col), loc * c["wrap"])
            collect(("bin", "metal"), loc * c["metal"])
            collect(("bin", "label"), loc * c["label"])
            collect(("bin", "ring"), loc * c["ring"])
    add("Matched group bins", _cmp(bins), C_BIN, "plastic", None, "context", (0, 0, 0))
    for g, s in plates:
        add(f"Grade {g} bin label", s, GRADE_COL[g], "painted", None, "context", (0, 0, 0))
    if letters:
        add("Grade letters", _cmp(letters), "#F5F7F7", "plastic", None, "context", (0, 0, 0))
    for col in WRAPS:
        flush(("bin", col), f"Cell wraps graded {col}", col, "painted", None, "context", (0, 0, 0))
    flush(("bin", "metal"), "Cell terminals graded", C_NICKEL, "metal", None, "context", (0, 0, 0))
    flush(("bin", "ring"), "Cell insulator rings graded", C_LABEL, "paper", None, "context", (0, 0, 0))
    flush(("bin", "label"), "Cell ID labels graded", C_LABEL, "paper", None, "context", (0, 0, 0))
    # the tray and everything in it stands on six rubber feet (the bench items stay at bench level)
    for o in out:
        if o["group"] in ("shell", "internal"):
            o["shape"] = Pos(0, 0, F) * o["shape"]
    feet = []
    for fx, fy in standoff_xy(P):
        ft_ = Pos(fx, fy, F / 2) * Cylinder(P["foot_d"] / 2, F)
        feet.append(_fillet_try(ft_, ft_.edges(), [2.0, 1.0]))
    add("Rubber feet", _cmp(feet), "#1F2328", "rubber", 19, "shell", (0, 0, -210))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:42s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:8.2f} cm3")
