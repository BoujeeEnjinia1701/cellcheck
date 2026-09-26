"""CellCheck sizing calculations, CCK-CAL-001 v0.1 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md and writes docs/04-calcs/results.csv.
First-principles paper estimates; nothing here is measured. The grading and matching check
(section 9) runs on synthetic cells drawn from a seeded random generator, not on real data.
"""
import csv
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad/src"))
from model import PARAMS as P, heatsink_extent, n_fins, envelope  # noqa: E402  (build123d not imported)

rows = []            # (id, value, target, status)


def out(label, value, fmt="{:.2f}", unit=""):
    print(f"  {label:58s} {fmt.format(value)} {unit}".rstrip())
    return value


def head(t):
    print("\n" + t)


# ---------------------------------------------------------------- 1. Assumptions
C_TYP = 1.8          # Ah, typical salvaged 18650 as found (near the 1.62 Ah mean, Olivero-Ortiz et al. 2026)
C_HIGH = 2.5         # Ah, a healthy laptop 18650
C_21700 = 4.5        # Ah, a salvaged 21700 at 90 % of 5 Ah
SOC_ARRIVE = 0.30    # state of charge on arrival
I_CHG = 1.0          # A, charger module CC setting
I_TERM = 0.1         # A, CV termination
SOC_CV = 0.80        # state of charge at the CC to CV change at about 0.5C (assumption)
SOC_REST = 0.80      # state of charge when the recharge stops at 4.10 V terminal under 1 A (assumption)
I_DIS = 1.0          # A, capacity discharge
REST1, REST2 = 0.5, 0.25     # h
DCIR_S = 11.0        # s, 0.5 A for 10 s then 2.0 A for 1 s
HANDLE = 0.5         # h, channel idle for operator handling per cell (conservative)
SD_READ = 0.02       # h, channel time for the day-14 reading (10 s plus insertion)
V_CHG_MEAN, V_DIS_MEAN = 3.90, 3.65   # V, mean cell voltage on charge and on discharge
V_START = 4.20       # V, worst case at the start of discharge
ETA_CHG, ETA_ADP = 0.85, 0.88         # charger module, mains adapter
P_OVH = 3.0          # W, controller, display and fans
ADAPTER_W, ADAPTER_V, MAIN_FUSE = 60.0, 12.0, 6.3
ATTENDED_H = 10.0    # h per attended day
N = P["n_ch"]

# Measurement chain (typical INA226-class and shunt data sheet values; assumptions, to be
# confirmed against the chosen parts' data sheets)
R_SHUNT = 0.025      # ohm
SHUNT_TOL = 0.005    # 0.5 % tolerance
SHUNT_TCR = 100e-6   # per K
SHUNT_DT = 20.0      # K, shunt self and ambient temperature swing
MON_GAIN = 0.001     # monitor gain error, max 0.1 %
MON_SHUNT_OFS = 10e-6  # V, shunt input offset, max
VBUS_LSB = 1.25e-3   # V, bus voltage resolution
VBUS_OFS = 7.5e-3    # V, bus offset, max
VBUS_GAIN = 0.001    # bus gain error, max
REF_METER = 0.0005   # reference meter used for one-time calibration, 0.05 % of reading
REF_COUNTS = 2e-3    # plus 2 counts of 1 mV
CAL_RESID = 0.001    # residual current gain error after calibration against a reference load
CUTOFF_SLOPE = 0.01 / 0.050   # share of capacity per volt near the 2.80 V cut-off (1 % per 50 mV, assumption)
DCIR_TCOEF = 0.015   # per K, DC resistance change with cell temperature (assumption)
DT_REINSERT = 2.0    # K, cell temperature difference between reinsertions
R_GRADE_A = 0.060    # ohm
OCV_TCOEF = 0.2e-3   # V/K, open-circuit voltage change with temperature (assumption)
DT_ROOM = 5.0        # K, bench temperature difference between day 0 and day 14

# Thermal
T_ROOM_MAX = 35.0
T_CASE_MAX = 75.0
R_CS = 1.0           # K/W, TO-220 case to sink through an insulating pad
R_JC = 1.0           # K/W, MOSFET junction to case (typical logic-level TO-220)
K_AL = 200.0         # W/(m K)
FAN_FREE = 8.0e-3    # m3/s per fan, 60 mm 12 V fan free air (assumption)
FAN_SHARE = 0.5      # share of free air delivered through the fins against back pressure
NU = 10.0            # Nusselt number, developing laminar flow between plates (assumption)
K_AIR = 0.026        # W/(m K)
RHO_AIR, CP_AIR = 1.16, 1007.0
R_SPREAD = 0.10      # K/W, spreading in the 6 mm spine (assumption)
H_NAT = 5.0          # W/(m2 K), fins without fans (effective, assumption)
H_CELL = 10.0        # W/(m2 K), natural convection from a cell under the guard

# Masses and densities
RHO_STEEL, RHO_AL, RHO_LINER = 7850.0, 2700.0, 128.0   # kg/m3
GUARD_T, GUARD_OPEN = 0.8e-3, 0.5
BOUGHT = {            # kg, assumptions for bought parts
    "cell holders (8 x 35 g)": 8 * 0.035, "charger modules (8 x 12 g)": 8 * 0.012,
    "sense boards (8 x 8 g)": 8 * 0.008, "MOSFETs and op-amps (8 x 4 g)": 8 * 0.004,
    "controller": 0.030, "display and stand": 0.060, "fans (2 x 45 g)": 2 * 0.045,
    "inlet, fuse, switch": 0.050, "watchdog board": 0.020, "wiring and fuses": 0.200,
    "standoffs and fasteners": 0.100, "NTC clips": 0.010,
}

print("CellCheck sizing, CCK-CAL-001 v0.1 (all values are paper estimates)")

# ---------------------------------------------------------------- 2. Cycle time (R5)
head("2. Cycle time per cell")


def charge_time(c, soc0, soc_cv=SOC_CV, i=I_CHG, i_term=I_TERM):
    """CC from soc0 to soc_cv, then CV with an exponential current decay from i to i_term."""
    t_cc = max(soc_cv - soc0, 0.0) * c / i
    q_cv = (1.0 - soc_cv) * c
    tau = q_cv / (i - i_term)
    return t_cc, tau * math.log(i / i_term)


def stages(c):
    t_cc, t_cv = charge_time(c, SOC_ARRIVE)
    return [("charge", t_cc + t_cv, True), ("rest", REST1, False), ("dcir", DCIR_S / 3600, True),
            ("discharge", c / I_DIS, True), ("rest", REST2, False),
            ("recharge", SOC_REST * c / I_CHG, True), ("handling", HANDLE + SD_READ, False)]


for c in (C_TYP, C_HIGH, C_21700):
    st = stages(c)
    t_cc, t_cv = charge_time(c, SOC_ARRIVE)
    print(f"  cell {c:.1f} Ah: charge {t_cc:.2f} + {t_cv:.2f} h, discharge {c / I_DIS:.2f} h, "
          f"recharge {SOC_REST * c:.2f} h, total channel time {sum(s[1] for s in st):.2f} h")
T_TYP = sum(s[1] for s in stages(C_TYP))
T_HIGH = sum(s[1] for s in stages(C_HIGH))
T_21700 = sum(s[1] for s in stages(C_21700))


def simulate(c, mode, days=14, day_h=ATTENDED_H):
    """Cells finished per day per channel. mode: 'boundary' (current stages start only if they
    finish in the attended window), 'pause' (current stages pause overnight, unit switched off),
    'continuous' (24 h, not allowed; reference only). Rests run at any time; handling is attended."""
    st = stages(c)
    t, done, k = 0.0, [], 0
    while t < days * 24:
        name, dur, current = st[k]
        attended = name == "handling" or (current and mode != "continuous")
        if not attended:
            t += dur
        elif mode == "pause" and current:
            left = dur
            while left > 1e-9:
                day, tod = divmod(t, 24)
                if tod >= day_h:
                    t = (day + 1) * 24
                    continue
                run = min(left, day_h - tod)
                t += run; left -= run
        else:
            day, tod = divmod(t, 24)
            if tod + dur > day_h:
                t = (day + 1) * 24 if tod > 0 or dur > day_h else t
                if dur > day_h:
                    raise ValueError("stage longer than the attended day")
            t += dur
        k += 1
        if k == len(st):
            done.append(t); k = 0
    lo, hi = 3 * 24, (days - 1) * 24      # steady state window
    return sum(1 for d in done if lo <= d < hi) / ((hi - lo) / 24)


head("  Throughput, 8 channels (cells per day, steady state)")
THR = {}
for c in (C_TYP, C_HIGH, C_21700):
    for mode in ("boundary", "pause", "continuous"):   # continuous: 24 h running, handling attended
        THR[(c, mode)] = N * simulate(c, mode)
        out(f"{c:.1f} Ah cells, {mode}", THR[(c, mode)], "{:.1f}", "cells/day")
THR_CONT_SIMPLE = N * 24 / T_TYP
out("check: 8 x 24 h / channel time, 1.8 Ah", THR_CONT_SIMPLE, "{:.1f}", "cells/day")

YIELD = 66 / 100
PACK_CELLS = 4 * 6
CANDIDATES = PACK_CELLS / YIELD
out("candidates for one 4S6P pack at 66 % yield", CANDIDATES, "{:.1f}", "cells")
out("attended days for them (pause mode, 1.8 Ah)", CANDIDATES / THR[(C_TYP, "pause")], "{:.1f}", "days")
out("attended days for them (boundary mode, 1.8 Ah)", CANDIDATES / THR[(C_TYP, "boundary")], "{:.1f}", "days")
r5 = THR[(C_TYP, "pause")]
r5b = THR[(C_TYP, "boundary")]
rows.append(("R5", f"{r5b:.1f} cells/day if current stages finish the same day; {r5:.1f} with an overnight pause; "
             f"{THR[(C_HIGH, 'boundary')]:.1f} for 2.5 Ah cells",
             "12 cells/day on 1.8 Ah cells", "Not met" if r5b < 12 else ("At risk" if r5b < 12.6 else "Met")))

# ---------------------------------------------------------------- 3. Power and energy (R13)
head("3. Power and energy")
p_chg_ch = V_START * I_CHG / ETA_CHG
P_CHG_ALL = N * p_chg_ch + P_OVH
out("adapter load, all channels charging at 4.2 V, 1 A", P_CHG_ALL, "{:.1f}", "W")
out("share of the 60 W adapter", P_CHG_ALL / ADAPTER_W * 100, "{:.0f}", "%")
I_IN = P_CHG_ALL / ADAPTER_V
out("input current at 12 V", I_IN, "{:.2f}", "A")
out("main fuse / input current", MAIN_FUSE / I_IN, "{:.2f}", "x")
V_BUS_MAX = ADAPTER_V * 1.05
out("highest bus voltage (adapter +5 %)", V_BUS_MAX, "{:.1f}", "V")
e_first = (1 - SOC_ARRIVE) * C_TYP * V_CHG_MEAN
e_re = SOC_REST * C_TYP * V_CHG_MEAN
e_ovh = P_OVH * T_TYP / N
E_CELL = ((e_first + e_re) / ETA_CHG + e_ovh) / ETA_ADP
out("first charge into the cell", e_first, "{:.2f}", "Wh")
out("recharge into the cell", e_re, "{:.2f}", "Wh")
out("overhead share per cell", e_ovh, "{:.2f}", "Wh")
out("energy per cell from the mains", E_CELL, "{:.1f}", "Wh")
out("cost per cell at $0.15/kWh", E_CELL / 1000 * 0.15, "{:.4f}", "USD")
E_DIS = C_TYP * V_DIS_MEAN
out("energy burned in the load per cell", E_DIS, "{:.2f}", "Wh")
rows.append(("R13", f"12 V certified adapter, bus at most {V_BUS_MAX:.1f} V, {P_CHG_ALL:.0f} W of 60 W",
             "Certified 12 V; 13 V or less inside; no mains wiring", "Met (design review)"))

# ---------------------------------------------------------------- 4. Heat (R8)
head("4. Heatsink and MOSFET temperature (R8)")
P_EACH_PEAK = V_START * I_DIS
P_PEAK = N * P_EACH_PEAK
P_AVG = N * V_DIS_MEAN * I_DIS
out("heat, all channels discharging, average", P_AVG, "{:.1f}", "W")
out("heat, all channels discharging, peak", P_PEAK, "{:.1f}", "W")
R_SA_NEED = (T_CASE_MAX - T_ROOM_MAX - P_EACH_PEAK * R_CS) / P_PEAK
out("heatsink needed for 75 C cases at 35 C", R_SA_NEED, "{:.2f}", "K/W")
hx0, hx1, hy0, hy1, hz0, hz1 = heatsink_extent()
nf = n_fins()
fin_len = P["fin_depth"] / 1000
fin_h = P["fin_h"] / 1000
gap = (P["fin_pitch"] - P["fin_t"]) / 1000
A_FIN = nf * 2 * fin_len * fin_h
out("fins", nf, "{:.0f}")
out("fin area", A_FIN, "{:.3f}", "m2")
Q_AIR = 2 * FAN_FREE * FAN_SHARE
dh = 2 * gap
h = NU * K_AIR / dh
flow_area = (nf - 1) * gap * fin_h
out("air through the fins", Q_AIR * 1000, "{:.1f}", "L/s")
out("air speed in the fin channels", Q_AIR / flow_area, "{:.2f}", "m/s")
out("heat transfer coefficient", h, "{:.1f}", "W/(m2 K)")
m = math.sqrt(2 * h / (K_AL * P["fin_t"] / 1000))
eta = math.tanh(m * fin_len) / (m * fin_len)
out("fin efficiency", eta, "{:.3f}")
dT_air = P_PEAK / (RHO_AIR * CP_AIR * Q_AIR)
out("air temperature rise", dT_air, "{:.1f}", "K")
R_SA = 1 / (h * eta * A_FIN) + (dT_air / 2) / P_PEAK + R_SPREAD
out("heatsink resistance with fans", R_SA, "{:.2f}", "K/W")
T_CASE = T_ROOM_MAX + P_PEAK * R_SA + P_EACH_PEAK * R_CS
T_J = T_CASE + P_EACH_PEAK * R_JC
out("MOSFET case at 35 C room, peak heat", T_CASE, "{:.1f}", "C")
out("MOSFET junction", T_J, "{:.1f}", "C")
m0 = math.sqrt(2 * H_NAT / (K_AL * P["fin_t"] / 1000))
eta0 = math.tanh(m0 * fin_len) / (m0 * fin_len)
R_SA_NOFAN = 1 / (H_NAT * eta0 * A_FIN) + R_SPREAD
T_CASE_NOFAN = T_ROOM_MAX + P_PEAK * R_SA_NOFAN + P_EACH_PEAK * R_CS
out("heatsink resistance, fans stopped", R_SA_NOFAN, "{:.2f}", "K/W")
out("MOSFET case, fans stopped (steady state)", T_CASE_NOFAN, "{:.0f}", "C")
P_PULSE = V_START * 2.0
out("MOSFET dissipation in the 2.0 A pulse, 1 s", P_PULSE, "{:.1f}", "W")
rows.append(("R8", f"{T_CASE:.0f} C case ({R_SA:.2f} K/W with fans); {T_CASE_NOFAN:.0f} C if the fans stop",
             "75 C or less at 35 C room", "Met" if T_CASE <= T_CASE_MAX else "Not met"))

head("  Cell heating at 1 A")
a_cell = math.pi * 0.018 * 0.065 + 2 * math.pi * 0.009 ** 2
for r in (0.060, 0.150, 0.418):
    q = I_DIS ** 2 * r
    out(f"cell at {r * 1000:.0f} mOhm: heat, rise", q, "{:.2f}", f"W, {q / (H_CELL * a_cell):.1f} K")
DT_CELL_A = I_DIS ** 2 * R_GRADE_A / (H_CELL * a_cell)
DT_CELL_418 = I_DIS ** 2 * 0.418 / (H_CELL * a_cell)

# ---------------------------------------------------------------- 5. Measurement error (R2, R3, R4, R6, R7)
head("5. Measurement error budgets")
i_ofs = MON_SHUNT_OFS / R_SHUNT / I_DIS
i_tc = SHUNT_TCR * SHUNT_DT
v_bus_raw = VBUS_OFS + VBUS_GAIN * 4.3 + VBUS_LSB / 2
cut = v_bus_raw * CUTOFF_SLOPE
CAP_RAW = SHUNT_TOL + MON_GAIN + i_ofs + i_tc + cut
out("current offset share at 1 A", i_ofs * 100, "{:.2f}", "%")
out("capacity error, uncalibrated, worst case", CAP_RAW * 100, "{:.2f}", "%")
REF_V = REF_METER * 4.3 + REF_COUNTS
v_cal = REF_V + VBUS_LSB / 2
CAP_CAL = CAL_RESID + i_ofs + i_tc + v_cal * CUTOFF_SLOPE
out("capacity error, calibrated, worst case", CAP_CAL * 100, "{:.2f}", "%")
rows.append(("R2", f"+/-{CAP_RAW * 100:.1f} % uncalibrated, +/-{CAP_CAL * 100:.1f} % calibrated (worst case)",
             "+/-2 %", "Met" if CAP_RAW <= 0.02 else "At risk"))

out("voltage error, uncalibrated, worst case", v_bus_raw * 1000, "{:.1f}", "mV")
out("voltage error, after two-point calibration", v_cal * 1000, "{:.1f}", "mV")
V_RAW, V_CAL = v_bus_raw, v_cal
rows.append(("R3", f"+/-{V_RAW * 1000:.1f} mV uncalibrated; +/-{V_CAL * 1000:.1f} mV after per-channel calibration",
             "+/-10 mV", "Met (with per-channel calibration)" if V_CAL <= 0.010 else "Not met"))

dI = 2.0 - 0.5
RES = VBUS_LSB / dI
q_term = VBUS_LSB / dI                 # half an LSB on each of two readings
g_term = (SHUNT_TOL + MON_GAIN) * R_GRADE_A
t_term = DCIR_TCOEF * DT_REINSERT * R_GRADE_A
DCIR_WC = q_term + g_term + t_term
DCIR_RSS = math.sqrt(q_term ** 2 + g_term ** 2 + t_term ** 2)
LIMIT = max(0.003, 0.05 * R_GRADE_A)
out("resistance resolution", RES * 1000, "{:.2f}", "mOhm per count")
out("repeatability at 60 mOhm, worst case sum", DCIR_WC * 1000, "{:.2f}", "mOhm")
out("repeatability at 60 mOhm, RSS", DCIR_RSS * 1000, "{:.2f}", "mOhm")
out("R4 limit at 60 mOhm", LIMIT * 1000, "{:.2f}", "mOhm")
out("temperature term alone", t_term * 1000, "{:.2f}", "mOhm")
r4_status = "At risk" if DCIR_WC > 0.9 * LIMIT else "Met"
rows.append(("R4", f"{RES * 1000:.2f} mOhm per count; +/-{DCIR_WC * 1000:.2f} mOhm worst case, "
             f"+/-{DCIR_RSS * 1000:.2f} RSS at 60 mOhm", "1 mOhm; +/-3 mOhm or 5 %", r4_status))

sd_each = V_CAL
sd_temp = OCV_TCOEF * DT_ROOM
SD_WC = 2 * sd_each + sd_temp
SD_RSS = math.sqrt(2 * sd_each ** 2 + sd_temp ** 2)
SD_SAME = 2 * (VBUS_LSB / 2) + sd_temp     # same channel both times: offset and gain cancel
out("self-discharge reading, any two channels, worst case", SD_WC * 1000, "{:.1f}", "mV")
out("self-discharge reading, RSS", SD_RSS * 1000, "{:.1f}", "mV")
out("self-discharge reading, same channel, worst case", SD_SAME * 1000, "{:.1f}", "mV")
rows.append(("R6", f"+/-{SD_WC * 1000:.1f} mV worst case (+/-{SD_RSS * 1000:.1f} RSS); relaxation after charge not bounded",
             "+/-3 mV; flag above 50 mV", "At risk"))

B, R0, T0 = 3950.0, 10000.0, 298.15
def ntc_sens(tc):
    t = tc + 273.15
    r = R0 * math.exp(B * (1 / t - 1 / T0))
    v = 3.3 * r / (r + R0)
    return v, 3.3 * R0 * r / (r + R0) ** 2 * B / t ** 2       # V, V/K (magnitude)
ADC_ERR = 0.020     # V, ESP32-class ADC after its factory calibration (assumption)
v45, s45 = ntc_sens(45.0)
T_ERR = ADC_ERR / s45 + 0.3     # ADC error plus 0.3 K for thermistor and resistor tolerance
out("NTC divider sensitivity at 45 C", s45 * 1000, "{:.1f}", "mV/K")
out("temperature error at 45 C (ADC plus 0.3 K part tolerance)", T_ERR, "{:.2f}", "K")
rows.append(("R7", f"+/-{T_ERR:.1f} K at 45 C, 1 Hz sampling; clip response time not analysed",
             "1 Hz, +/-2 K; stop at 45 C or +8 K", "Met (accuracy); response not verifiable at TRL 3"))

# ---------------------------------------------------------------- 6. Single fault (R9)
head("6. Single-fault currents (R9)")
R_WIRE = 0.030
CH_FUSE = 3.0
for r, v in ((0.060, 3.6), (0.418, 3.6), (0.418, 2.8)):
    i = v / (r + R_SHUNT + R_WIRE)
    out(f"shorted MOSFET, cell {r * 1000:.0f} mOhm at {v} V: current", i, "{:.1f}", f"A, {i / CH_FUSE:.1f} x fuse")
I_SC_MIN = 2.8 / (0.418 + R_SHUNT + R_WIRE)
V_CHG_MAX = 4.20 * 1.01
out("charger module voltage limit, +1 %", V_CHG_MAX, "{:.3f}", "V")
rows.append(("R9", f"Met on FMEA with watchdog, UV comparators and {CH_FUSE:.0f} A channel fuses "
             f"(short gives at least {I_SC_MIN:.1f} A); detached thermistor is a residual risk",
             "No single fault: >4.25 V, >60 C or <2.5 V", "Met (analysis)"))

# ---------------------------------------------------------------- 7. Containment (R10)
head("7. Containment (R10)")
tray_area = (P["tray_l"] * P["tray_w"] + 2 * (P["tray_l"] + P["tray_w"]) * P["tray_h"]) / 1e6
M_TRAY = tray_area * P["tray_t"] / 1000 * RHO_STEEL
out("tray sheet area", tray_area, "{:.3f}", "m2")
out("tray mass", M_TRAY, "{:.2f}", "kg")
Q_RUNAWAY = 100e3   # J, assumed total heat from one 21700 in runaway incl. burning vent gas (to be sourced)
dT_TRAY = Q_RUNAWAY / (M_TRAY * 490.0)
out("mean tray rise if it absorbed all of it", dT_TRAY, "{:.0f}", "K")
rows.append(("R10", f"Mean tray rise {dT_TRAY:.0f} K for an assumed 100 kJ event; jets, hot spots and flame not analysable on paper",
             "Hold one venting 21700 within the tray", "Not verifiable at TRL 3"))

# ---------------------------------------------------------------- 8. Size and mass (R11)
head("8. Size and mass (R11)")
e = envelope()
DIMS = (e[1] - e[0], e[3] - e[2], e[5] - e[4])
out("grader envelope L", DIMS[0], "{:.0f}", "mm")
out("grader envelope W", DIMS[1], "{:.0f}", "mm")
out("grader envelope H", DIMS[2], "{:.0f}", "mm")
M_PLATE = P["plate_l"] * P["plate_w"] * P["plate_t"] / 1e9 * RHO_AL
spine = (hx1 - hx0) * P["spine_t"] * P["fin_h"]
fins = nf * P["fin_t"] * P["fin_depth"] * P["fin_h"]
M_HS = (spine + fins) / 1e9 * RHO_AL
M_SHROUD = ((hx1 - hx0) * P["fan"] + (hx1 - hx0) * P["fin_depth"]) * P["shroud_t"] / 1e9 * RHO_AL
gx = (N - 1) * P["pitch"] + 2 * P["guard_margin_x"]
gy = 2 * P["guard_margin_y"]
gz = P["cell_axis_h"] + P["cell_r"] + P["guard_clear"]
M_GUARD = (gx * gy + 2 * gx * gz + 2 * gy * gz) / 1e6 * GUARD_T * RHO_STEEL * (1 - GUARD_OPEN)
M_LINER = (P["tray_l"] * P["tray_w"]) / 1e6 * P["liner_t"] / 1000 * RHO_LINER
masses = {"steel tray": M_TRAY, "base plate": M_PLATE, "heatsink": M_HS, "fan shroud": M_SHROUD,
          "guard": M_GUARD, "liner": M_LINER, **BOUGHT}
for k_, v_ in masses.items():
    out(k_, v_, "{:.3f}", "kg")
M_TOTAL = sum(masses.values())
out("total without adapter", M_TOTAL, "{:.2f}", "kg")
r11_ok = DIMS[0] <= 500 and DIMS[1] <= 320 and DIMS[2] <= 120 and M_TOTAL <= 5.0
rows.append(("R11", f"{DIMS[0]:.0f} x {DIMS[1]:.0f} x {DIMS[2]:.0f} mm; {M_TOTAL:.2f} kg",
             "500 x 320 x 120 mm; 5 kg", ("At risk" if M_TOTAL > 4.75 else "Met") if r11_ok else "Not met"))

# ---------------------------------------------------------------- 9. Grading and matching (R15)
head("9. Grading and matching on synthetic cells (R15)")
rng = random.Random(2026)
RATED = 2.2
cells = []
for n in range(150):
    c = min(max(rng.gauss(1.62, 0.53), 0.04), 2.50)
    r = min(math.exp(rng.gauss(math.log(0.075), 0.45)), 0.418)
    cells.append((f"C{n:03d}", c, r))


def grade(c, r):
    s = c / RATED
    if s >= 0.80 and r <= 0.060:
        return "A"
    if s >= 0.65 and r <= 0.100:
        return "B"
    if s >= 0.50 and r <= 0.150:
        return "C"
    return "Reject"


graded = {}
for cid, c, r in cells:
    graded.setdefault(grade(c, r), []).append((cid, c, r))
for g in ("A", "B", "C", "Reject"):
    out(f"grade {g}", len(graded.get(g, [])), "{:.0f}", "cells")


def match(pool, s, p_):
    """Pick the S x P cells with the narrowest capacity window, serpentine them into S groups,
    then improve with pairwise swaps. Returns (groups, max deviation from the mean)."""
    need = s * p_
    pool = sorted(pool, key=lambda x: x[1])
    best = min(range(len(pool) - need + 1), key=lambda i: pool[i + need - 1][1] - pool[i][1])
    pick = sorted(pool[best:best + need], key=lambda x: -x[1])
    groups = [[] for _ in range(s)]
    for i, cell in enumerate(pick):
        rnd, pos = divmod(i, s)
        groups[pos if rnd % 2 == 0 else s - 1 - pos].append(cell)

    def dev(gs):
        tot = [sum(c[1] for c in g) for g in gs]
        mean = sum(tot) / len(tot)
        return max(abs(t - mean) for t in tot) / mean
    d0 = dev(groups)
    improved = True
    while improved:
        improved = False
        for a in range(s):
            for b_ in range(a + 1, s):
                for i in range(p_):
                    for j in range(p_):
                        groups[a][i], groups[b_][j] = groups[b_][j], groups[a][i]
                        if dev(groups) < d0 - 1e-12:
                            d0 = dev(groups); improved = True
                        else:
                            groups[a][i], groups[b_][j] = groups[b_][j], groups[a][i]
    return groups, d0


pool = graded.get("A", []) + []
use = "A" if len(pool) >= 24 else "B"
pool = graded[use]
g_, d_serp = match(pool, 4, 6)
tots = [sum(c[1] for c in g) for g in g_]
print(f"  4S6P from grade {use}: parallel group capacities (Ah)       " + ", ".join(f"{t:.3f}" for t in tots))
out("max deviation from the mean", d_serp * 100, "{:.3f}", "%")
MATCH_DEV = d_serp
rows.append(("R15", f"4S6P from {len(pool)} grade {use} synthetic cells: max group deviation {d_serp * 100:.2f} %",
             "Configurable grades; groups within +/-1 %", "Met (synthetic data)" if d_serp <= 0.01 else "Not met"))

# ---------------------------------------------------------------- 10. Second-life SwapCell variant (study)
head("10. Second-life SwapCell variant (study, DDR item 1)")
S_ = 13
P_ = 4
C_A = 0.8 * RATED
pack_ah = P_ * C_A
pack_wh = S_ * V_DIS_MEAN * pack_ah
I_MAX_A = 0.5 * pack_ah
out("13S4P of grade A cells at 80 % of 2.2 Ah: capacity", pack_ah, "{:.2f}", "Ah")
out("energy", pack_wh, "{:.0f}", "Wh")
out("current limit at 0.5C", I_MAX_A, "{:.2f}", "A")
out("power at 0.5C and 46.8 V", I_MAX_A * 46.8, "{:.0f}", "W")
out("PowerBox 300 W inverter draw at 39 V and 88 %", 300 / 0.88 / 39.0, "{:.1f}", "A")
out("PowerBox reference evening from the pack (PBX-CAL-001)", 224.8, "{:.1f}", "Wh")
out("evenings per pack", pack_wh * 0.9 / 224.8, "{:.2f}")
cells_fit = (330 // 65) * (84 // 18.5) * (74 // 18.5)
out("18650 cells in an assumed 330 x 84 x 74 mm cell space", cells_fit, "{:.0f}")
SL_WH, SL_I = pack_wh, I_MAX_A

# ---------------------------------------------------------------- 11. Cost (R12)
head("11. Cost (R12)")
bom = list(csv.DictReader((ROOT / "bom/bom.csv").open()))
COST = sum(int(r["qty"]) * float(r["unit_cost_usd"]) for r in bom)
BUDGET, BUDGET_REC = 160.0, 175.0
out("BOM lines", len(bom), "{:.0f}")
out("parts cost", COST, "{:.2f}", "USD")
out("against project.yaml budget $160", COST - BUDGET, "{:+.2f}", "USD")
out("against recommended budget $175 (awaiting Amish)", COST - BUDGET_REC, "{:+.2f}", "USD")
rows.append(("R12", f"${COST:.2f}; ${COST - BUDGET:+.2f} against $160; ${COST - BUDGET_REC:+.2f} against the recommended $175",
             "$160 or less (project.yaml)", "Not met" if COST > BUDGET else "Met"))

# ---------------------------------------------------------------- 12. Design review items
rows += [
    ("R1", "8 channels; holders for 18650 and 21700 (cell to 70 mm long, 21.0 mm diameter)",
     "18650 and 21700, 8 channels or more", "Met (design review)"),
    ("R14", "Rest stage unattended (no current); charge and discharge attended (DDR item 2)",
     "Rest stage unattended; current stages attended (redefined v0.3)", "Met (design review)"),
    ("R16", "CSV per cell; group and reject lots map to the ReflowEconomy passport v0.2 (two schema gaps)",
     "CSV per cell; local export; no cloud", "Met (design review)"),
    ("R17", "Modules and through-hole parts; CERN-OHL-S-2.0 and MIT", "Off-the-shelf; open licences",
     "Met (design review)"),
]

order = {"Not met": 0, "At risk": 1, "Not verifiable at TRL 3": 2}
rows.sort(key=lambda r: (order.get(r[3].split(" (")[0], 3), int(r[0][1:])))
head("Results")
for r in rows:
    print(f"  {r[0]:4s} {r[3]:48s} {r[1]}")
with (Path(__file__).parent / "results.csv").open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "value", "target", "status"])
    w.writerows(rows)
print("\nwrote docs/04-calcs/results.csv")
