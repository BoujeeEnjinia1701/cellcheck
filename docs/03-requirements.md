---
doc_id: CCK-REQ-001
title: CellCheck requirements
project: CellCheck
doc_type: Requirements
version: "0.2"
status: Draft
date: '2026-09-25'
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
---

# CellCheck requirements

These are first-pass requirements for the concept. Targets are proposals for review, not user-validated needs; they will be checked by calculation at TRL 3 and revised with the first trial partner. Status in Table 2 is judged against the estimates in CCK-PRC-001. Two requirements are not met at TRL 2 (R9 and R14) and three are at risk (R3, R10 and R13).

Table 1. Requirements.

| ID | Requirement | Target | Verification (TRL 3 or later) |
| --- | --- | --- | --- |
| R1 | Test the common salvaged cell sizes | 18650 and 21700 cylindrical lithium-ion cells (LCO, NMC, NCA), one cell per channel, 8 channels or more | Design review of holders and profiles |
| R2 | Measure capacity accurately | ±2 % of reading at a constant 1.0 A discharge from 4.20 V to 2.80 V | Error budget; later comparison with a calibrated reference |
| R3 | Measure cell voltage accurately | ±10 mV from 2.0 to 4.3 V | Data sheet error budget; later comparison with a calibrated meter |
| R4 | Measure DC internal resistance repeatably | Resolution 1 mΩ or better; repeatability ±3 mΩ or ±5 % of reading, whichever is larger, over 5 reinsertions of one cell | Error budget; later repeat test |
| R5 | Grade enough cells | 12 cells or more per attended 10 h day on typical 1.8 Ah cells | Cycle-time calculation |
| R6 | Detect self-discharge | Open-circuit voltage change over a 14-day rest measured to ±3 mV; cells dropping more than 50 mV (default) flagged | Calculation; later repeat readings |
| R7 | Monitor cell temperature | Each cell measured at least once per second to ±2 K; channel stops above 45 °C or at a rise of more than 8 K above the bench | Design review; later bench test |
| R8 | Keep the unit cool at full load | Load MOSFET cases at 75 °C or less with all channels discharging at 1 A in a 35 °C room | Thermal calculation |
| R9 | Stay safe after a single fault | No single failure (controller crash, stuck-on load MOSFET, open thermistor, failed charger) lets a cell be charged above 4.25 V, heated past 60 °C, or discharged below 2.5 V | Failure mode and effects analysis |
| R10 | Contain a single cell failure | Tray, liner and guard hold ejecta and flame from one venting 21700 cell without spread beyond the tray | Analysis at TRL 3; physical test only at TRL 4 or later |
| R11 | Fit on a bench | 500 x 320 x 120 mm or smaller, 5 kg or less without the adapter | Massing model; later weighing |
| R12 | Stay within the concept budget | $160 or less in parts at quantity one, excluding cells | Priced BOM |
| R13 | Run from a safe supply | Certified 12 V DC adapter; nothing inside the unit above 13 V; no user mains wiring | Design review |
| R14 | Operate without supervision | Grading can run overnight without a person present | Safety review by Amish |
| R15 | Grade and match automatically | Grades per a configurable rule table; groups for any SxP pack with each parallel group's capacity within ±1 % of the mean | Run on sample data |
| R16 | Keep a record for every cell | CSV row per cell with ID, source, measurements, grade, group and dates; export over USB or local Wi-Fi with no cloud account | Design review of the file format |
| R17 | Be buildable and open | Off-the-shelf modules, no fine-pitch assembly; hardware CERN-OHL-S-2.0, software MIT | Design review of the parts list |

Table 2. Status at TRL 2 (estimates).

| ID | Status | Basis |
| --- | --- | --- |
| R1 | Met by design | Eight holders for 18650 and 21700 |
| R2 | Met on estimate | About ±1 % after one-time calibration, about ±2 % without |
| R3 | **At risk** | About ±10 mV worst case from typical data sheet figures before calibration; unchecked |
| R4 | Met on estimate, unverified | About 0.8 mΩ per count; repeatability depends on contact force and cell temperature |
| R5 | Met, thin margin | About 12 cells per attended 10 h day |
| R6 | Met on estimate | 1.25 mV resolution; room temperature changes of a few kelvin shift readings by about 1 mV (assumption) |
| R7 | Met by design | NTC per cell, firmware limits; response time unverified |
| R8 | Met on estimate | Needs 1.1 K/W; a fan-cooled finned bar is expected to give about 0.5 to 0.8 K/W |
| R9 | **Not met** | Charger modules limit voltage independently, but a stuck-on load MOSFET can drain a cell below 2.5 V and temperature limits rely on firmware. A hardware watchdog and a per-channel undervoltage comparator are proposed, awaiting Amish |
| R10 | **At risk** | Containment concept only; no analysis yet |
| R11 | Met | About 460 x 300 x 90 mm, about 3.5 kg |
| R12 | Met, about $1 margin | About $159 in parts |
| R13 | **At risk** | Met by design only if the adapter is a certified unit; low-cost adapters without certification are common |
| R14 | **Not met** | The concept requires a person present while cells charge or discharge; whether and how overnight runs are allowed is a safety trade-off awaiting Amish |
| R15 | Met by design | Serpentine sort within a grade; tolerance to be confirmed on real cells |
| R16 | Met by design | CSV on microSD and local web page |
| R17 | Met by design | Module-based build |

## Assumptions

- A typical salvaged 18650 holds about 1.8 Ah as found and arrives at about 30 % charge.
- A 14-day rest at 4.10 V separates cells with a harmful self-discharge from healthy ones; the 50 mV threshold is a starting value to be tuned with real cells.
- Operators remove cells from packs by hand before grading; disassembly is outside the scope of this design.
