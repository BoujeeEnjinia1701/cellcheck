---
doc_id: CCK-DEC-001
title: CellCheck design decisions register
project: CellCheck
doc_type: Design decisions register
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
  - version: "0.1"
    date: '2026-10-01'
    author: Amish Chadha
    change: Register opened with the open decisions from the review note and decision records, the build plan work and every decision made so far
  - version: "0.2"
    date: '2026-10-01'
    author: Amish Chadha
    change: Budget treated as a value-engineering target
---

# CellCheck design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Decisions still to be made.*

| # | Decision needed | Options | Recommendation | Affects in the build | Source |
| --- | --- | --- | --- | --- | --- |
| 1 | How the guard is held down (part of the containment arrangement) | (a) two knurled thumb screws, as modelled; (b) two toggle latches; (c) a hinge at the back with one latch | (a) for the first prototype; decide for later units after the TRL 4 containment test | Guard flanges, rivet nuts (build plan sections 3.8 and step 11) | CCK-DDR-003, A1 |
| 2 | Whether the wire slots under the guard are sealed after wiring | (a) open with grommet strip, as modelled; (b) filled round the leads with high-temperature silicone | (b) | Wiring step 9 | CCK-DDR-003, A2 |
| 3 | First trial partner | Repair café, e-bike repair shop or battery collection point | None stated | Not part of the build; sets the cells used at TRL 4 | CCK-DDR-001, item 10 |
| 4 | Scheduling rule for the attended day | (a) start a current stage only if it finishes the same day (12.0 cells per day); (b) pause overnight with the unit off (12.8 cells per day) | None made; (b) adds an unquantified capacity error | Firmware sketch only | CCK-DDR-001, item 12 |
| 5 | Responses to the requirements at risk, R11 (mass, 4.91 kg against 5 kg) and R5 (throughput) | For R11: accept and weigh at TRL 4, or a 1.2 mm tray (saves about 0.49 kg but thins the containment); for R5: scheduling rule, more channels later | None made | Tray thickness if R11 changes | CCK-DDR-001, item 14; CCK-CAL-001 section 8 |
| 6 | Grade A resistance limit per cell model (60 mΩ default) | Values per cell model from named data sheets | None; needs data sheets | Grading table only | CCK-DDR-001, item 16 |
| 7 | 18650 cells shown in the product renders where the model uses the 21700 envelope | Accept for the renders, or render 21700 cells | Accept; the model keeps the 21700 envelope for clearance checks | None | REVIEW 2026-09-26 |
| 8 | Bins for matched groups A, B and C shown in the renders | (a) render context only; (b) a BOM line for three bins, costed against the value-engineering target | (a) now; decide (b) with TRL 4 purchasing | None now | REVIEW 2026-09-26 |
| 9 | Fan finger guards shown in the renders | Add to BOM line 10 at TRL 4 and cost them then, or leave out | Add at TRL 4 | Fans (step 7) | REVIEW 2026-09-26 |
| 10 | Guard perforation drawn as slots and 1.0 mm sheet in the renders | Accept as appearance, or redraw with round holes and 0.8 mm | Accept; the BOM specification stays as written | None | REVIEW 2026-09-26 |
| 11 | Second-life SwapCell pack for PowerBox (low-current storage, about 334 Wh, 165 W) | Agree with the SwapCell and PowerBox projects, or not | Raise with those projects (cross-repo action) | None | CCK-DDR-001, item 1; CCK-CAL-001 section 10 |

## To confirm when parts are bought

*Table 2. Items to check against the parts before building.*

| # | What to confirm | Why it matters | Source |
| --- | --- | --- | --- |
| 1 | The steel tray is plain steel, about 460 x 300 x 45 mm with 1.5 mm walls, and its flat floor is at least 457 x 297 mm inside | The liner, plate and containment estimate assume it | CCK-DDR-003, P1 |
| 2 | The rubber feet have M4 studs about 8 mm long | The stud must pass the 1.5 mm floor and engage the standoff | CCK-DDR-003, P1 |
| 3 | The M4 rivet nuts grip 1.5 mm sheet and their heads are under 1 mm thick | The guard flange sits round the head | CCK-DDR-003, P4 |
| 4 | The cell holders have two M3 fixing holes in their base and take 18650 and 21700 cells up to 70 mm | Holder screws and the 84 mm holder length | CCK-DDR-003, P3 |
| 5 | The charger modules, current monitor breakouts, controller and converter have M3 mounting holes (or are fixed to a small perfboard that has them) | Each board stands on two nylon standoffs | CCK-DDR-003, P5 |
| 6 | The 2.8 in display module is about 86 x 50 mm with four corner holes | Display stand size | CCK-DDR-003, P6 |
| 7 | The heatsink spine is 6 mm thick, 50 mm tall, and has a fin gap at 20 mm from the left end and every 40 mm after it | MOSFET screws go between fins; plate and shroud screws are tapped into the spine | CCK-DDR-003, P7 |
| 8 | The fans have a 50 mm square screw pattern | Shroud holes | CCK-DDR-003, P8 |
| 9 | The DC jack, fuse holder and rocker switch cut-out sizes against the inlet housing (11.2 mm, 12 mm, 12 x 16 mm) | Inlet housing holes | CCK-DDR-003, P10 |
| 10 | A sourced figure for the heat released by one 21700 cell in thermal runaway, to replace the assumed 100 kJ | Containment estimate before any TRL 4 work | CCK-CAL-001 section 7 |

## Value engineering

Value-engineering target: USD 175.00 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 172.40 (USD 2.60 under the target).

Main cost drivers (CCK-CAL-001, section 11): the per-channel parts, which are bought eight times (cell holder with four-wire contacts, charger module, channel board, load MOSFET and op-amp loop, thermistor: about $66 for the eight channels), the mains adapter ($15), the steel tray with liner ($12) and the controller board ($10). The parts added for construction (lines 19 to 21) cost $8.40.

Savings worth trying, should indicative prices rise above the target:

- Leave the matched-group bins and the fan finger guards out of the BOM until TRL 4 purchasing (open decisions 8 and 9).
- Look for a cheaper cell holder or charger module, since each saving is multiplied by eight.

## Decisions made

*Table 3. Decisions made, with dates and records.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | Keep SwapCell in the pitch and plan a second-life variant; charge and discharge attended only (rest stage may be left); hardware watchdog and undervoltage comparators; grading thresholds, 14-day rest and ±1 % group tolerance as starting values; TP5100, INA226 and ESP32-S3 class modules; eight channels with a linear load; LFP profile later; per-cell CSV mapped to the ReflowEconomy passport (items 1 to 3 and 5 to 9) | Amish: "i accept all your recommendations, go with them across all repos." | CCK-DDR-001, CCK-DDR-002 |
| 2026-09-25 | Budget raised from $160 to $175 (item 4) | Amish, same instruction | CCK-DDR-001, CCK-DDR-002 |
| 2026-09-25 | DC four-wire resistance and a 14-day rest (item 11); firmware and build rules: same-channel cohort self-discharge reading, temperature-gated resistance pulse, per-channel calibration, fan-fault stop, detached-thermistor check (item 13); raise the passport gaps with ReflowEconomy (item 15) | Amish, same instruction | CCK-DDR-001, CCK-DDR-002 |
| 2026-10-01 | Design for construction: feet and standoffs, 1.5 mm plate on six standoffs, holder fixings and wire slots, folded guard with thumb screws, board standoffs, larger display stand, heatsink and shroud fixings, thermistor C-clips, inlet housing, 5 V converter and channel boards (P1 to P12) | Made under Amish's 2026-09-30 instruction: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." Open for his review | CCK-DDR-003 |
