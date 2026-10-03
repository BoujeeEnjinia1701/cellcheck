---
doc_id: CCK-DEC-001
title: CellCheck design decisions register
project: CellCheck
doc_type: Design decisions register
version: "0.5"
status: Draft
date: '2026-10-02'
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
  - version: "0.3"
    date: '2026-10-02'
    author: Amish Chadha
    change: Amish approved the recommendations of open items 1 to 11 on 2026-10-02; all moved to decisions made; value-engineering savings line updated
  - version: "0.4"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Design for construction (CCK-DDR-003, P1 to P12) accepted by Amish on 2026-10-02; the 2026-10-01 row no longer says open for review"
  - version: "0.5"
    date: '2026-10-02'
    author: Amish Chadha
    change: "Estimated cost updated to $177.60 ($2.60 over the target) after the fan finger guards and silicone were priced; open decision 1 added for the overshoot"
---

# CellCheck design decisions register

Every design decision still to be made, and every decision made, in one place. Each decision is argued in full in its decision record under `docs/decisions/`; this register is the index Amish works from. The build plan (`docs/05-build-plan.md`) describes the design as it stands and does not list open decisions.

## Open decisions

*Table 1. Open decisions.*

| # | Decision | Options | Recommendation |
| --- | --- | --- | --- |
| 1 | The estimated cost is $2.60 over the $175 value-engineering target once the fan finger guards (line 10, $1.20) and the silicone (line 16, $4.00) decided on 2026-10-02 are priced | (a) Accept the overshoot: the target is a control target, not a limit. (b) Look for savings of $2.60 or more, for example a cheaper holder or charger module (each saving is multiplied by eight). (c) Raise the target, which `budget_usd` would follow | (a) for the paper design; revisit with real quotes at TRL 4 purchasing. Proposed, awaiting Amish |

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

Value-engineering target: USD 175.00 (a hypothetical control target, not a limit). Estimated cost of the constructable design: USD 177.60 (USD 2.60 over the target).

Main cost drivers (CCK-CAL-001, section 11): the per-channel parts, which are bought eight times (cell holder with four-wire contacts, charger module, channel board, load MOSFET and op-amp loop, thermistor: about $66 for the eight channels), the mains adapter ($15), the steel tray with liner ($12) and the controller board ($10). The parts added for construction (lines 19 to 21) cost $8.40.

Savings worth trying, should indicative prices rise above the target:

- Leave the matched-group bins out of the BOM until TRL 4 purchasing (decided 2026-10-02). The fan finger guards (line 10, $1.20 for two) and the silicone for the wire slots (line 16, $4.00) decided on 2026-10-02 are now in the estimate; they are the reason it is over the target (open decision 1).
- Look for a cheaper cell holder or charger module, since each saving is multiplied by eight.

## Decisions made

*Table 3. Decisions made, with dates and records.*

| Date | Decision | Decided by | Record |
| --- | --- | --- | --- |
| 2026-09-25 | Keep SwapCell in the pitch and plan a second-life variant; charge and discharge attended only (rest stage may be left); hardware watchdog and undervoltage comparators; grading thresholds, 14-day rest and ±1 % group tolerance as starting values; TP5100, INA226 and ESP32-S3 class modules; eight channels with a linear load; LFP profile later; per-cell CSV mapped to the ReflowEconomy passport (items 1 to 3 and 5 to 9) | Amish: "i accept all your recommendations, go with them across all repos." | CCK-DDR-001, CCK-DDR-002 |
| 2026-09-25 | Budget raised from $160 to $175 (item 4) | Amish, same instruction | CCK-DDR-001, CCK-DDR-002 |
| 2026-09-25 | DC four-wire resistance and a 14-day rest (item 11); firmware and build rules: same-channel cohort self-discharge reading, temperature-gated resistance pulse, per-channel calibration, fan-fault stop, detached-thermistor check (item 13); raise the passport gaps with ReflowEconomy (item 15) | Amish, same instruction | CCK-DDR-001, CCK-DDR-002 |
| 2026-10-01 | Design for construction: feet and standoffs, 1.5 mm plate on six standoffs, holder fixings and wire slots, folded guard with thumb screws, board standoffs, larger display stand, heatsink and shroud fixings, thermistor C-clips, inlet housing, 5 V converter and channel boards (P1 to P12) | Made under Amish's 2026-09-30 instruction: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The changes themselves were accepted on 2026-10-02 (below) | CCK-DDR-003 |
| 2026-10-02 | Open item 1: the guard is held down by the two knurled M4 thumb screws for the first prototype, and the TRL 4 containment test is run with the guard held exactly that way; latches are revisited only if the test or users show the screws being left loose | Amish: "i approve your recommendations for all 555 open decisions." | CCK-DDR-003, A1 |
| 2026-10-02 | Open item 2: each wire slot under the guard is filled round its leads with high-temperature silicone after wiring, closing the guard space again | Amish: "i approve your recommendations for all 555 open decisions." | CCK-DDR-003, A2 |
| 2026-10-02 | Open item 3: first trial partner, the first candidate to approach (not yet agreed), is a local Repair Café group that already passes laptop batteries to an e-waste or battery collection point, with that collection point as the source of trial cells | Amish: "i approve your recommendations for all 555 open decisions." | CCK-DDR-001, item 10 |
| 2026-10-02 | Open item 4: scheduling rule for the attended day: a charge or discharge starts only if it will finish the same day (12.0 cells per day); no overnight pause | Amish: "i approve your recommendations for all 555 open decisions." | CCK-DDR-001, item 12 |
| 2026-10-02 | Open item 5: R11, the 4.91 kg mass is accepted with the 1.5 mm tray kept, and the prototype is weighed at TRL 4; R5, throughput rests on the same-day rule of item 4, and more channels are left for a later version | Amish: "i approve your recommendations for all 555 open decisions." | CCK-DDR-001, item 14; CCK-CAL-001 section 8 |
| 2026-10-02 | Open item 6: 60 mΩ stays the grade A default; per-model limits are added only for the few cell models most common in the partner's intake, set from DC resistance measured on known-good cells of each model, not from data sheet impedance | Amish: "i approve your recommendations for all 555 open decisions." | CCK-DDR-001, item 16 |
| 2026-10-02 | Open item 7: 18650 cells accepted in the product renders; the model keeps the 21700 envelope for clearance checks | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26 |
| 2026-10-02 | Open item 8: the matched-group bins are render context only for now; a BOM line is decided at TRL 4 purchasing | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26 |
| 2026-10-02 | Open item 9: fan finger guards are added to BOM line 10 now, with an estimated price, rather than at TRL 4 | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26 |
| 2026-10-02 | Open item 10: the guard's slotted perforation and 1.0 mm sheet in the renders are accepted as appearance only; the BOM keeps round holes in 0.8 mm sheet | Amish: "i approve your recommendations for all 555 open decisions." | `docs/REVIEW.md`, 2026-09-26 |
| 2026-10-02 | Open item 11: the second-life pack study (about 334 Wh, 165 W) is sent to the SwapCell and PowerBox projects as a proposal; no further CellCheck action | Amish: "i approve your recommendations for all 555 open decisions." | CCK-DDR-001, item 1; CCK-CAL-001 section 10 |
| 2026-10-02 | Design for construction accepted: the changes P1 to P12 and their knock-on changes, as made | Amish: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)" | [CCK-DDR-003](decisions/0003-design-for-construction.md), Tables 1 and 2 |
