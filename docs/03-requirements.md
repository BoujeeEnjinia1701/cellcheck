---
doc_id: CCK-REQ-001
title: CellCheck requirements
project: CellCheck
doc_type: Requirements
version: "0.8"
status: Draft
date: '2026-10-02'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Initial scaffold
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: First measurable requirements for TRL 2
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply CCK-DDR-001 (R14 redefined, R9 protection adopted, R3 calibration, R12 against both budgets); status table from CCK-CAL-001
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002). R12 target $175 and met; R4 met with the temperature-gated pulse; R6 read in the same channel; status table from CCK-CAL-001 v0.2
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: R11 and R12 values for the constructable design (CCK-DDR-003, CCK-CAL-001 v0.3); no status changed
- version: "0.6"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target; cost wording only, no number changed
- version: "0.7"
  date: '2026-10-02'
  author: Amish Chadha
  change: R5 and R11 status notes record the 2026-10-02 decisions (CCK-DEC-001, items 4 and 5); no status changed
- version: "0.8"
  date: '2026-10-02'
  author: Amish Chadha
  change: "R12 status changed from within to over the value-engineering target ($177.60, $2.60 over $175) and R11 mass 4.94 kg, after the fan finger guards and silicone were added to the BOM (CCK-CAL-001 v0.6)"
---

# CellCheck requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs, and will be revised with the first trial partner. Status in Table 2 comes from the calculation note CCK-CAL-001 v0.3. No requirement is failed outright; three are at risk (R5, R6 and R11), and R10 cannot be verified at TRL 3. R14 was redefined in v0.3 under CCK-DDR-001 item 2, and R12 was restated in v0.4 for the $175 value-engineering target; both follow decisions Amish accepted on 2026-09-25 (CCK-DDR-002).

Table 1. Requirements.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Test the common salvaged cell sizes | 18650 and 21700 cylindrical lithium-ion cells (LCO, NMC, NCA), one cell per channel, 8 channels or more | Design review of holders and profiles |
| R2 | Measure capacity accurately | ±2 % of reading at a constant 1.0 A discharge from 4.20 V to 2.80 V | Error budget; later comparison with a calibrated reference |
| R3 | Measure cell voltage accurately | ±10 mV from 2.0 to 4.3 V, after a one-time per-channel calibration at build | Data sheet error budget; later comparison with a calibrated meter |
| R4 | Measure DC internal resistance repeatably | Resolution 1 mΩ or better; repeatability ±3 mΩ or ±5 % of reading, whichever is larger, over 5 reinsertions of one cell | Error budget; later repeat test |
| R5 | Grade enough cells | 12 cells or more per attended 10 h day on typical 1.8 Ah cells | Cycle-time calculation |
| R6 | Detect self-discharge | Open-circuit voltage change over a 14-day rest measured to ±3 mV, with both readings in the same channel; cells dropping more than 50 mV (default) beyond the median of the same-day cohort flagged | Calculation; later repeat readings |
| R7 | Monitor cell temperature | Each cell measured at least once per second to ±2 K; channel stops above 45 °C or at a rise of more than 8 K above the bench | Design review; later bench test |
| R8 | Keep the unit cool at full load | Load MOSFET cases at 75 °C or less with all channels discharging at 1 A in a 35 °C room | Thermal calculation |
| R9 | Stay safe after a single fault | No single failure (controller crash, stuck-on load MOSFET, open thermistor, failed charger) lets a cell be charged above 4.25 V, heated past 60 °C, or discharged below 2.5 V | Failure mode and effects analysis |
| R10 | Contain a single cell failure | Tray, liner and guard hold ejecta and flame from one venting 21700 cell without spread beyond the tray | Analysis at TRL 3; physical test only at TRL 4 or later |
| R11 | Fit on a bench | 500 x 320 x 120 mm or smaller, 5 kg or less without the adapter | Massing model; later weighing |
| R12 | Stay within the value-engineering target | $175 or less in parts at quantity one, excluding cells (`project.yaml`, a hypothetical control target, not a limit). Restated in v0.4 from $160 (CCK-DDR-001 item 4, decided by Amish, 2026-09-25) | Priced BOM |
| R13 | Run from a safe supply | Certified 12 V DC adapter; nothing inside the unit above 13 V; no user mains wiring | Design review |
| R14 | Limit unattended operation to safe stages | The self-discharge rest (no current flowing) can run without a person present; charge, resistance pulse and discharge run only with a person present. Redefined in v0.3 from "grading can run overnight without a person present" (CCK-DDR-001 item 2) | Design review; safety review by Amish |
| R15 | Grade and match automatically | Grades per a configurable rule table; groups for any SxP pack with each parallel group's capacity within ±1 % of the mean | Run on sample data |
| R16 | Keep a record for every cell | CSV row per cell with ID, source, measurements, grade, group and dates; export over USB or local Wi-Fi with no cloud account | Design review of the file format |
| R17 | Be buildable and open | Off-the-shelf modules, no fine-pitch assembly; hardware CERN-OHL-S-2.0, software MIT | Design review of the parts list |

Table 2. Status at TRL 3 (CCK-CAL-001 v0.3, paper estimates; at risk first, no requirement failed outright).

| ID | Status | Basis |
| --- | --- | --- |
| R5 | **At risk** | 12.0 cells per attended day under the same-day rule decided on 2026-10-02 (CCK-DEC-001, item 4; the overnight pause, 12.8, is not used); 8.0 for 2.5 Ah cells; more channels left for a later version |
| R6 | **At risk** | ±2.3 mV in the same channel (±10.6 mV across channels, no longer allowed); cohort median cancels common relaxation, but the spread between cells is not bounded |
| R11 | **At risk** | 460 x 300 x 85 mm; 4.94 kg against 5 kg (constructable design, CCK-DDR-003, with the fan finger guards and silicone of 2026-10-02). Accepted for the prototype on 2026-10-02 with the 1.5 mm tray kept; weighed at TRL 4 (CCK-DEC-001, item 5) |
| R10 | Not verifiable at TRL 3 | Containment cannot be analysed credibly on paper; mean tray rise about 84 K for an assumed 100 kJ event |
| R1 | Met (design review) | Eight holders for 18650 and 21700 cells |
| R2 | Met | ±1.1 % without calibration, ±0.4 % with |
| R3 | Met (with per-channel calibration) | ±12.4 mV without calibration; ±4.8 mV after it |
| R4 | Met | 0.83 mΩ per count; repeatability ±2.09 mΩ worst case against ±3.0 mΩ at 60 mΩ, with the pulse started only within 1 K of the bench (was ±2.99 mΩ, at risk) |
| R7 | Met (accuracy) | ±1.0 K at 45 °C, 1 Hz sampling; clip response time not verifiable at TRL 3 |
| R8 | Met | MOSFET cases 58.7 °C with fans; about 99 °C if the fans stop, so the firmware stops discharges on a fan fault |
| R9 | Met (analysis) | Watchdog, undervoltage comparators, 3 A channel fuses and a series charge switch (CCK-CAL-001 Table 3); a detached thermistor is narrowed by a plausibility check but remains a residual risk |
| R12 | **Over the value-engineering target** | $177.60 estimated in parts, $2.60 over $175 (lines 19 to 21 added for construction, CCK-DDR-003; fan finger guards on line 10 and silicone on line 16 added on 2026-10-02, CCK-DEC-001 items 9 and 2) |
| R13 | Met (design review) | Certified 12 V adapter; 12.6 V highest inside; 42.5 W of 60 W |
| R14 | Met (design review) | As redefined in v0.3 |
| R15 | Met (synthetic data) | 0.006 % group deviation for a 4S6P pack from synthetic cells |
| R16 | Met (design review) | CSV per cell; lots map to the ReflowEconomy passport v0.2 with two schema gaps |
| R17 | Met (design review) | Module-based build; open licences |

## Assumptions

- A typical salvaged 18650 holds about 1.8 Ah as found and arrives at about 30 % charge.
- A 14-day rest after a recharge that stops at 4.10 V under current separates cells with a harmful self-discharge from healthy ones; the 50 mV threshold is a starting value to be tuned with real cells.
- Operators remove cells from packs by hand before grading; disassembly is outside the scope of this design.

> **Safety:** CellCheck charges and discharges salvaged lithium-ion cells, which can overheat, vent and burn. Charge and discharge run only with a person present. Meeting these requirements on paper does not make a unit safe, and grades do not certify any cell or pack.
