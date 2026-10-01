---
doc_id: CCK-CAL-001
title: CellCheck sizing calculations
project: CellCheck
doc_type: Calculation note
version: "0.3"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: First TRL 3 sizing note (cycle time and throughput, power, heatsink, measurement error budgets, single-fault analysis, containment, mass, grading on synthetic data, second-life SwapCell study, cost)
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). Budget $175 (R12 met); temperature-gated resistance pulse (R4 met); same-channel, cohort-median self-discharge reading (R6)
- version: "0.3"
  date: '2026-10-01'
  author: Amish Chadha
  change: Design made constructable (CCK-DDR-003). Size and mass (section 8) and cost (section 11) rerun for the 1.5 mm base plate on six standoffs, rubber feet, folded guard and shroud, fixings and the 5 V converter
---

# CellCheck sizing calculations

On paper, CellCheck meets 13 of its 17 requirements, and no requirement is failed outright. Version 0.2 applies the decisions Amish accepted on 2026-09-25 (CCK-DDR-002): the budget in `project.yaml` is now $175, so the parts cost meets **R12** (it was $4 over the former $160), and the resistance pulse now starts only within 1 K of the bench reading, so **R4** is met at ±2.09 mΩ against ±3.0 mΩ (it was ±2.99 mΩ, at risk). Three requirements remain **at risk**: R5 (throughput is exactly 12 cells per attended day), R6 (self-discharge reading) and R11 (mass is 4.91 kg against 5 kg). R10 (containment) cannot be verified at TRL 3. The TRL 2 figures change in several places: time per cell falls from about 6.5 to 6.33 h, capacity error without calibration is ±1.1 % rather than ±2 %, voltage error without calibration is ±12.4 mV rather than ±10 mV, and the unit is 85 mm high and 4.91 kg rather than 90 mm and 3.5 kg. The heatsink fins in the TRL 2 massing model ran across the fan airflow; they are now vertical plates in line with it. Version 0.3 reruns size, mass and cost for the constructable design of CCK-DDR-003 (feet, a thinner base plate on six standoffs, fixings and a 5 V converter): 85 mm high, 4.91 kg and $172.40, so R11 stays at risk and R12 stays met with $2.60 of margin. No other result changes.

Every number here is printed by `docs/04-calcs/sizing.py` (run from the repo root: `python docs/04-calcs/sizing.py`), which also writes `docs/04-calcs/results.csv`. The script reads the geometry from `cad/src/model.py` and the costs from `bom/bom.csv`. All values are first-principles estimates; nothing is measured.

## 1. Assumptions

*Table 1. Inputs. All are assumptions for a paper design.*

| Input | Value | Basis |
| --- | --- | --- |
| Typical cell | 18650, 1.8 Ah as found, arriving at 30 % state of charge; also 2.5 Ah (healthy laptop cell) and 4.5 Ah (salvaged 21700) | Near the 1.62 Ah mean in Olivero-Ortiz et al. (2026), cited in CCK-PRB-001 |
| Charge | 1.0 A CC to 80 % state of charge, then CV at 4.20 V with an exponential decay to 0.1 A | Typical at about 0.5C |
| Recharge for the rest | 1.0 A CC until the terminal reads 4.10 V under current, about 80 % state of charge | Charger modules are fixed at 4.20 V, so the firmware stops them |
| Discharge | 1.0 A to 2.80 V; delivered capacity equals the as-found capacity | |
| Rests, pulse, handling | 0.5 h and 0.25 h rests; 11 s resistance pulse; 0.5 h channel idle per cell for handling and 0.02 h for the day-14 reading | Handling allowance is conservative |
| Attended day | 10 h; charge, pulse, discharge and handling need a person present; rests do not | CCK-DDR-001 item 2 |
| Mean cell voltage | 3.90 V on charge, 3.65 V on discharge, 4.20 V worst case at the start of discharge | |
| Efficiencies | Charger module 85 %; adapter 88 %; controller, display and fans 3 W | |
| Monitor (INA226 class) | Shunt offset 10 µV; gain error 0.1 %; bus offset 7.5 mV; bus gain error 0.1 %; bus resolution 1.25 mV | Typical data sheet maximums; to be confirmed against the chosen part |
| Shunt | 25 mΩ, 0.5 %, 100 ppm/K over a 20 K swing | |
| Calibration | Two-point voltage calibration per channel against a meter of 0.05 % + 2 counts (1 mV); current gain calibrated to 0.1 % | One-time, at build |
| Cell behaviour | Near the 2.80 V cut-off, 1 % of capacity per 50 mV; resistance changes 1.5 %/K; open-circuit voltage changes 0.2 mV/K | Assumptions for a generic lithium-ion cell |
| Resistance pulse start | Only when the cell reads within 1 K of the bench thermistor, so reinsertions differ by 1 K at most | Firmware rule, CCK-DDR-002 item 13 |
| Temperature sensing | 10 kΩ NTC, B 3950, 1 %, 10 kΩ divider from 3.3 V; ADC error 20 mV after factory calibration; 0.3 K for part tolerance | ESP32-class ADC; assumption |
| Heatsink | 40 aluminium fins, 1.6 x 30 x 50 mm at 8 mm pitch on a 320 x 6 x 50 mm spine; case to sink 1.0 K/W through an insulating pad; junction to case 1.0 K/W | `cad/src/model.py` |
| Fans | 60 mm, 8 L/s free air each, half of that through the fins; Nusselt number 10 in the fin channels; 5 W/(m² K) effective with the fans stopped | Assumptions |
| Materials | Steel 7,850 kg/m³; aluminium 2,700 kg/m³; ceramic fibre sheet 128 kg/m³ | |
| Bought parts | Masses in `sizing.py` section 8 (holders 35 g each, modules 8 to 12 g, wiring 200 g) | Assumptions |

## 2. Cycle time and throughput (R5)

A typical 1.8 Ah cell occupies a channel for **6.33 h**: charge 0.90 h CC plus 0.92 h CV, rest 0.5 h, pulse, discharge 1.80 h, rest 0.25 h, recharge 1.44 h and 0.52 h of handling. A 2.5 Ah cell takes 8.30 h and a 4.5 Ah 21700 takes 13.93 h. The TRL 2 figure of about 6.5 h underestimated the CV phase and overestimated the recharge.

Because charge and discharge must be attended (CCK-DDR-001 item 2), throughput depends on the scheduling rule. A day-by-day simulation of the eight channels gives:

*Table 2. Cells finished per day, steady state, eight channels.*

| Rule | 1.8 Ah | 2.5 Ah | 4.5 Ah |
| --- | --- | --- | --- |
| A stage with current starts only if it finishes within the 10 h day | 12.0 | 8.0 | 4.8 |
| Current stages pause overnight with the unit switched off, and resume | 12.8 | 9.6 | 5.6 |
| Reference only: running 24 h, handling in attended hours (not allowed) | 16.0 | 16.0 | 8.0 |

On the first rule the grader finishes exactly 12 typical cells a day, so **R5 is at risk** with no margin, and it is not met on healthier 2.5 Ah cells. The pause rule gains 0.8 cells a day, but a discharge interrupted overnight lets the cell recover and adds a small capacity error that is not quantified here. One 4S6P pack needs about 36.4 candidates at the 66 % yield assumed in the flow diagram, so about 3.0 attended days plus the 14-day rest.

## 3. Power and energy (R13)

With all eight channels charging at 4.2 V and 1 A, the adapter supplies **42.5 W** (71 % of 60 W), or 3.54 A at 12 V; the 6.3 A main fuse is 1.78 times that. With the adapter at +5 % the highest voltage inside the unit is **12.6 V**, under the 13 V of R13.

Each typical cell takes 4.91 Wh on its first charge and 5.62 Wh on its recharge, plus 2.38 Wh of overhead, for **16.8 Wh** from the mains (about $0.0025 at $0.15/kWh). The load burns 6.57 Wh per cell as heat.

## 4. Heatsink and MOSFET temperature (R8)

At full discharge load the eight MOSFETs dissipate **29.2 W** on average and **33.6 W** at the start (4.2 V x 1 A x 8). To keep the MOSFET cases at 75 °C in a 35 °C room, the heatsink must reach **1.07 K/W** or better.

The fans push air into the back of the fin channels through a shroud, and the air leaves through the open tops. With 8.0 L/s through 39 channels the air speed is 0.64 m/s, the heat transfer coefficient is 20.3 W/(m² K) on 0.120 m² of fin area, and the fin efficiency is 0.964. Adding half of the 3.6 K air temperature rise and 0.10 K/W of spreading in the spine gives **0.58 K/W**. The MOSFET cases then reach **58.7 °C** and the junctions 62.9 °C, so **R8 is met**. If both fans stop, the heatsink falls to about 1.78 K/W and the cases would settle near **99 °C**, so the firmware must stop all discharges when the fan tachometer or a heatsink thermistor reports a fault. The 2.0 A resistance pulse adds 8.4 W to one MOSFET for 1 s, which is small against its thermal mass.

Cell heating at 1 A is small: 0.06 W and about 1.4 K for a 60 mΩ cell, 3.6 K at the 150 mΩ grade C limit and 10.0 K for the worst 418 mΩ cell reported by Olivero-Ortiz et al. (2026). The 8 K rise limit therefore flags high-resistance cells without tripping on healthy ones.

## 5. Measurement error budgets (R2, R3, R4, R6, R7)

**Capacity (R2).** Without calibration the worst case is the sum of the shunt tolerance (0.5 %), monitor gain (0.1 %), current offset (0.04 % at 1 A), shunt temperature drift (0.2 %) and the cut-off voltage error (12.4 mV, worth 0.25 % of capacity): **±1.09 %**. After calibration it is **±0.44 %**. R2 (±2 %) is met.

**Voltage (R3).** Without calibration the worst case is 7.5 mV offset, 4.3 mV gain error at 4.3 V and half a count: **±12.4 mV**, which does not meet ±10 mV. After a two-point calibration of each channel against a 0.05 % meter it is **±4.8 mV**. R3 is met only with the per-channel calibration, which is now part of the design.

**DC resistance (R4).** A 1.25 mV count over the 1.5 A current step gives **0.83 mΩ per count**. For a 60 mΩ cell, the repeatability over reinsertions sums to **±2.09 mΩ** worst case (0.83 mΩ quantization, 0.36 mΩ gain, 0.90 mΩ from a 1 K cell temperature difference) and ±1.28 mΩ RSS, against a limit of ±3.0 mΩ. Offsets cancel in the difference, and the four-wire contacts keep contact resistance out. The firmware starts the pulse only when the cell is within 1 K of the bench reading (CCK-DDR-002 item 13); version 0.1 allowed 2 K and found ±2.99 mΩ, at risk. **R4 is met** on the error budget. The 30 min rest before the pulse is normally enough for a cell that warmed by about 1.4 K on charge; a warmer cell waits longer, which this note does not add to the cycle time.

**Self-discharge (R6).** If the day-14 reading is taken in a different channel from the day-0 reading, the two calibrated readings and a 5 K room change give **±10.6 mV** worst case (±6.8 mV RSS) against ±3 mV. In the same channel, offset and gain cancel and the error falls to **±2.3 mV**. In addition, a cell whose charge stops under current relaxes by an amount this note cannot bound. Under CCK-DDR-002 item 13 each cell now returns to the channel it was graded in, so the reading error is **±2.3 mV**, inside ±3 mV, and its drop is judged against the median drop of the cells charged on the same day, which cancels the common part of relaxation and room temperature. The spread of relaxation between cells is still not bounded on paper, so **R6 remains at risk**.

**Temperature (R7).** The divider gives 27.2 mV/K at 45 °C; a 20 mV ADC error plus 0.3 K of part tolerance is **±1.04 K**, inside ±2 K. Sampling at 1 Hz is a firmware setting. The thermal lag of the clip is not analysed and is not verifiable at TRL 3.

## 6. Single-fault analysis (R9)

This is the failure mode and effects analysis called for at TRL 2, with the hardware watchdog and undervoltage comparators adopted in CCK-DDR-001 item 3. The watchdog removes every charge enable and every load gate drive when the controller stops refreshing it. Each channel's comparator removes that channel's load gate drive below 2.5 V. Each cell has a 3 A fast fuse in its positive lead, and the charge switch is in series between the charger and the cell.

*Table 3. Single faults against the R9 limits (above 4.25 V, above 60 °C, below 2.5 V).*

| Single fault | Effect without protection | What stops it | Result |
| --- | --- | --- | --- |
| Controller crash or firmware hang | Charger and load stay as last set; temperature limits lost | Watchdog opens all charge switches and removes all load gate drive | Safe |
| Load MOSFET fails short | Cell discharges through the channel | Short current is 31.3 A for a 60 mΩ cell and at least 5.9 A for a 418 mΩ cell at 2.8 V, 2.0 times the 3 A fuse or more; the fuse opens | Safe; cell rejected |
| Op-amp or gate drive stuck on | Load runs past the cut-off | Undervoltage comparator removes the gate drive at 2.5 V | Safe |
| Charger output regulates high (failed feedback) | Cell charged above 4.20 V | Firmware reads the monitor and opens the series charge switch at 4.25 V; current above 1.2 A also opens it | Safe |
| Charge switch fails short | Charger stays connected | Charger module limits the cell to 4.242 V (4.20 V + 1 %) | Safe |
| Thermistor open or shorted | Temperature reads out of range | Firmware treats a reading outside -20 to 80 °C as a fault and stops the channel | Safe |
| Thermistor clip detached | Reads the air, not the cell | Not detected; charger voltage limit still holds | **Residual risk** |
| Fan stops | MOSFETs could reach about 99 °C | Firmware stops discharges on a tachometer or heatsink fault | Safe (firmware) |
| Adapter output high | Bus voltage rises | Certified adapter; charger modules regulate their own output | Safe for R9; R13 depends on the adapter |

**R9 is met on analysis** for the faults it lists. The detached thermistor is a residual risk that R9 does not name; a plausibility check (cell temperature must rise slightly during discharge) narrows it and is now part of the firmware rules (CCK-DDR-002 item 13), but it is not verified at TRL 3. The fuses and comparators are not verified by test at TRL 3.

## 7. Containment (R10)

The 1.5 mm steel tray has 0.206 m² of sheet and weighs **2.43 kg**. If a 21700 cell in thermal runaway released 100 kJ in total, including burning vent gas (an assumption that must be replaced by a sourced figure before TRL 4), the mean tray temperature would rise about **84 K** if the tray absorbed all of it. Mean temperature says little about jets, hot spots on the bench under the tray, or flame through the perforated guard, and none of these can be analysed credibly on paper. **R10 is not verifiable at TRL 3.** The fan intake slots in the back wall (56 x 22 mm each) are a new path out of the tray and are noted for the containment review.

## 8. Size and mass (R11)

The model envelope is **460 x 300 x 85 mm** (the display stand and the 8 mm rubber feet set the height), inside 500 x 320 x 120 mm. The mass without the adapter is **4.91 kg**: tray 2.43 kg, base plate 0.47 kg, heatsink 0.52 kg, guard 0.24 kg, shroud 0.06 kg, liner 0.05 kg, and 1.14 kg of bought parts, fixings and wiring. **R11 is at risk** with 0.09 kg of margin. In version 0.2 the unit was 75 mm and 4.97 kg; the constructable design (CCK-DDR-003) adds feet, fixings, guard flanges and a 5 V converter (about 0.12 kg) and takes 0.16 kg off by making the base plate 1.5 mm thick on six standoffs instead of 2 mm on four. With six supports the plate spans at most 165 mm between standoffs, so it stays stiff. A 1.2 mm tray would save about 0.49 kg; no response has been chosen and it stays Proposed, awaiting Amish (item 14), because the tray is also the containment.

## 9. Grading and matching on synthetic data (R15)

The grading rules (CCK-PRC-001 Table 2) and the matching method were run on 150 synthetic cells drawn from a seeded random generator: capacity normal with mean 1.62 Ah and standard deviation 0.53 Ah (clipped to 0.04 to 2.50 Ah, the figures reported by Olivero-Ortiz et al., 2026), resistance log-normal with a 75 mΩ median (an assumption), and 2.2 Ah rated capacity. They produce 15 grade A, 47 grade B, 55 grade C and 33 rejected cells. For a 4S6P pack from grade B, the method picks the 24 cells with the narrowest capacity window, distributes them with a serpentine sort and then swaps cells between groups while that reduces the spread. The four parallel groups come out at 9.677 to 9.678 Ah, a **0.006 %** maximum deviation from the mean. R15 is met on synthetic data; real cells will be less tidy.

## 10. Second-life SwapCell variant (study)

CCK-DDR-001 item 1 keeps SwapCell in the pitch and asks for a second-life variant to be studied. A 13S4P pack of grade A laptop cells at 80 % of 2.2 Ah holds **7.04 Ah and about 334 Wh**, and at the 0.5C limit for grade A it can deliver **3.52 A**, about **165 W**. That covers PowerBox's reference evening of 224.8 Wh from the pack 1.34 times (PBX-CAL-001), but not its 300 W inverter, which draws about 8.7 A at 39 V. An assumed 330 x 84 x 74 mm cell space inside the SwapCell body holds up to 80 cells of 18650 size, so 52 cells fit before the BMS and wiring are placed. The study therefore supports a low-current storage variant for PowerBox with the AC output limited to about 150 W, or a DC-only PowerBox, and rules out e-bike use. Any variant needs the SwapCell project's agreement and its own pack design; it is not a CellCheck deliverable.

## 11. Cost (R12)

The 21 BOM lines total **$172.40**, $2.60 under the $175 in `project.yaml`. Amish accepted the $175 budget on 2026-09-25 (CCK-DDR-002 item 4). **R12 is met.** The increase over TRL 2 is line 18 (watchdog and comparators, $5.00); the increase over version 0.2 ($164.00) is lines 19 to 21, added for construction (rubber feet $2.40, fixings $4.00, 5 V converter $2.00).

## 12. Results against requirements

*Table 4. Requirement status (at risk first; no requirement is failed outright). Values from `results.csv`.*

| ID | Value | Target | Status |
| --- | --- | --- | --- |
| R5 | 12.0 cells per day if current stages finish the same day; 12.8 with an overnight pause; 8.0 for 2.5 Ah cells | 12 cells per attended day on 1.8 Ah cells | At risk |
| R6 | ±2.3 mV in the same channel, judged against the same-day cohort median (±10.6 mV across channels, no longer allowed); spread of relaxation not bounded | ±3 mV; flag above 50 mV | At risk |
| R11 | 460 x 300 x 85 mm; 4.91 kg | 500 x 320 x 120 mm; 5 kg | At risk |
| R10 | Mean tray rise 84 K for an assumed 100 kJ event; jets and flame not analysable | Hold one venting 21700 in the tray | Not verifiable at TRL 3 |
| R1 | Eight channels; holders for 18650 and 21700 cells up to 70 mm long | 18650 and 21700; 8 channels or more | Met (design review) |
| R2 | ±1.1 % uncalibrated; ±0.4 % calibrated | ±2 % | Met |
| R3 | ±12.4 mV uncalibrated; ±4.8 mV after per-channel calibration | ±10 mV | Met (with per-channel calibration) |
| R4 | 0.83 mΩ per count; ±2.09 mΩ worst case, ±1.28 mΩ RSS at 60 mΩ, pulse gated within 1 K | 1 mΩ; ±3 mΩ or ±5 % | Met |
| R7 | ±1.0 K at 45 °C; 1 Hz sampling | 1 Hz, ±2 K; stop at 45 °C or +8 K | Met (accuracy); response time not verifiable at TRL 3 |
| R8 | 58.7 °C case with fans (0.58 K/W); 99 °C if the fans stop | 75 °C or less at 35 °C | Met |
| R9 | Watchdog, undervoltage comparators, 3 A fuses; detached thermistor narrowed by a plausibility check, still residual | No single fault past 4.25 V, 60 °C or 2.5 V | Met (analysis) |
| R12 | $172.40; $2.60 under $175 | $175 or less (`project.yaml`) | Met |
| R13 | Certified 12 V adapter; 12.6 V highest; 42.5 W of 60 W | Certified 12 V; 13 V or less | Met (design review) |
| R14 | Rest stage unattended; current stages attended | As redefined in CCK-REQ-001 v0.3 | Met (design review) |
| R15 | 0.006 % group deviation on synthetic 4S6P | ±1 % | Met (synthetic data) |
| R16 | CSV per cell; group and reject lots map to the ReflowEconomy passport v0.2 with two gaps (section 13) | CSV per cell; local export | Met (design review) |
| R17 | Modules and through-hole parts; open licences | Buildable and open | Met (design review) |

## 13. Record mapping to the ReflowEconomy passport (R16)

CCK-DDR-001 item 9 (decided by Amish, CCK-DDR-002) maps the CellCheck record to ReflowEconomy's material passport schema v0.2. The per-cell CSV stays the primary record; one passport is issued per lot that leaves the bench.

*Table 5. Passport fields for a CellCheck lot.*

| Passport field | Matched group of graded cells | Lot of rejected cells |
| --- | --- | --- |
| `batch_id` | Group ID, for example `CCK-G-0007` | Reject lot ID |
| `product_form` | No suitable value (gap 1) | `export-lot` |
| `parent_batch_ids` | Intake batch IDs of the source packs | Same |
| `material` | Cell format and chemistry, for example `Li-ion 18650 NMC` | Same |
| `grade` | CellCheck grade A, B or C | `reject` |
| `mass_kg` | Cell count x measured or table mass | Same |
| `origin` | Collection point and country of the source packs | Same |
| `identification.method` | No suitable value (gap 2) | Same |
| `processed_by`, `process`, `date` | Workshop, `cellcheck-grade`, grading date | Same |

Gap 1: the schema has no `product_form` for graded cells. Gap 2: `identification.method` does not list an electrical test. Both are raised in `docs/REVIEW.md` for the ReflowEconomy project; this repo does not edit that schema.

## 14. Checks against earlier documents

*Table 6. TRL 2 figures corrected by this note.*

| Quantity | TRL 2 (CCK-PRC-001 v0.2) | This note | Where fixed |
| --- | --- | --- | --- |
| Time per cell | about 6.5 h | 6.33 h (typical); 8.30 h for 2.5 Ah | PRC v0.3, README |
| Throughput | about 12 per attended day | 12.0 (stage-boundary rule), at risk | PRC v0.3, REQ v0.3, README |
| Capacity error uncalibrated | about ±2 % | ±1.1 % | PRC v0.3, REQ v0.3 |
| Voltage error uncalibrated | about ±10 mV | ±12.4 mV; ±4.8 mV calibrated | PRC v0.3, REQ v0.3 |
| Heatsink needed and expected | 1.1 K/W; 0.5 to 0.8 K/W | 1.07 K/W; 0.58 K/W | PRC v0.3 |
| Heatsink fins | Plates across the fan airflow | Vertical plates in line with it | Model, PRC v0.3 |
| Energy per cell | about 18 Wh | 16.8 Wh | PRC v0.3 |
| Cell heating at 1 A | about 0.1 W, a few kelvin | 0.06 W and 1.4 K at 60 mΩ | PRC v0.3 |
| Height and mass | 90 mm; about 3.5 kg (tray 2.0 kg) | 85 mm; 4.91 kg (tray 2.43 kg); 75 mm and 4.97 kg in v0.2 | PRC v0.5, REQ v0.5, README |
| Parts cost | about $159 | $172.40; $164.00 in v0.2 | PRC v0.5, REQ v0.5, README, BOM notes |
| Rest voltage | "rest at 4.10 V" | Recharge stops at 4.10 V under 1 A, about 80 % state of charge | PRC v0.3 |

> **Safety:** These are paper calculations for a device that charges and discharges salvaged lithium-ion cells. The single-fault analysis and the containment estimate are not evidence that the unit is safe. Operate it only attended during charge and discharge, on a non-flammable surface with a smoke alarm and an extinguisher or sand bucket within reach. CellCheck is a research and prototype tool, and its grades do not certify any cell or pack as safe.
