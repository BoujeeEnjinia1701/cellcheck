---
doc_id: CCK-DDR-001
title: CellCheck TRL 2 review decisions
project: CellCheck
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review, and the items that stay open
- version: "0.2"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** decided for items with a recommendation. On 2026-09-25 Amish accepted all recommendations (CCK-DDR-002): items 1 to 9, 11, 13 and 15 are Decided by Amish, 2026-09-25: go with recommendation. Items 10, 12, 14 and 16 have no recommendation and remain Proposed, awaiting Amish.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25) listed ten items as "Proposed, awaiting Amish", nine of them with a recommendation. The TRL 3 session first adopted each recommended item for TRL 3 work, open for Amish's review, and added items 11 to 16. Later on 2026-09-25 Amish wrote "i accept all your recommendations, go with them across all repos." Each item that carries a recommendation is therefore decided as recommended; where several options were offered, the recommended option is the decision. What changed in the repo is listed in CCK-DDR-002. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 session) and CCK-PRC-001 v0.2. They are not repeated here.

## Decision

*Table 1. Decided items.*

| # | Item | Status and content | Where it now lives |
| --- | --- | --- | --- |
| 1 | SwapCell link (affects the pitch) | Decided by Amish, 2026-09-25: go with recommendation. Option (a): keep the pitch and plan a second-life SwapCell variant, agreed with the SwapCell project. The TRL 3 study (CCK-CAL-001 section 10) finds a low-current 13S4P storage pack for PowerBox feasible at about 334 Wh and 165 W; e-bike use is ruled out. No pitch rewording was recommended, so `project.yaml` and the README keep their pitch and problem lines. The agreement with SwapCell is a cross-repo action | CCK-PRC-001, CCK-PRB-001, CCK-CAL-001 section 10, README |
| 2 | Unattended operation (safety trade-off) | Decided by Amish, 2026-09-25: go with recommendation. Charge and discharge are attended only; the rest stage (no current flowing) may be left unattended | CCK-REQ-001 R14 (redefined), CCK-PRC-001 safety, README |
| 3 | Single-fault protection | Decided by Amish, 2026-09-25: go with recommendation. A hardware watchdog removes all charge enables and load gate drive when the controller stops, and a per-channel undervoltage comparator removes load gate drive below 2.5 V, about $5 | `bom/bom.csv` line 18, `cad/src/model.py` part 18, CCK-CAL-001 section 6, CCK-REQ-001 R9 |
| 4 | Budget | Decided by Amish, 2026-09-25: go with recommendation. Option (a): `budget_usd` raised from $160 to $175 for the watchdog and margin. The $164 BOM now meets R12 with $11 of margin | `project.yaml`, CCK-REQ-001 v0.4 R12, CCK-CAL-001 v0.2 section 11 |
| 5 | Grading thresholds, 14-day rest with a 50 mV limit, ±1 % group tolerance | Decided by Amish, 2026-09-25: go with recommendation. Starting values, to be tuned with the first 100 real cells; the tuning is TRL 4 work and on hold | CCK-PRC-001 Table 2, CCK-REQ-001 R6 and R15 |
| 6 | Module choices | Decided by Amish, 2026-09-25: go with recommendation. TP5100-class charger, INA226-class monitor with a 25 mΩ shunt, ESP32-S3 class controller | CCK-PRC-001 Table 1, `bom/bom.csv` lines 6, 7 and 11 |
| 7 | Channel count and load type | Decided by Amish, 2026-09-25: go with recommendation. Eight channels with a linear load; 16 channels and regenerative discharge are later variants | CCK-PRC-001 |
| 8 | LFP profile | Decided by Amish, 2026-09-25: go with recommendation. Later, after the lithium-ion profile is proven | CCK-PRC-001, CCK-PRB-001 |
| 9 | Record format | Decided by Amish, 2026-09-25: go with recommendation. The per-cell CSV stays the primary record; each matched group and each reject lot maps to ReflowEconomy's material passport v0.2 (two schema gaps, see item 15) | CCK-CAL-001 section 13, CCK-PRC-001 |
| 11 | DC four-wire resistance rather than 1 kHz AC impedance, and the 14-day (rather than 7-day) rest | Decided by Amish, 2026-09-25: go with recommendation. DC pulses and a 14-day rest, as recommended in the precis and used as the working basis of CCK-CAL-001 | CCK-PRC-001, CCK-CAL-001 |
| 13 | TRL 3 engineering proposals from CCK-CAL-001 | Decided by Amish, 2026-09-25: go with recommendation. Firmware and build rules: read self-discharge in the same channel and against the median of the same-day cohort (R6); start the resistance pulse only within 1 K of the bench (R4, now met at ±2.09 mΩ); per-channel two-point voltage calibration at build (R3); stop discharges on a fan or heatsink fault (R8); a plausibility check for a detached thermistor (R9). Writing and testing the firmware and doing the calibration are TRL 4 work and on hold | CCK-PRC-001 v0.4, CCK-CAL-001 v0.2 section 5, CCK-REQ-001 v0.4 |
| 15 | ReflowEconomy passport gaps: no `product_form` for graded cells and no electrical test in `identification.method` | Decided by Amish, 2026-09-25: go with recommendation. Raise with the ReflowEconomy project; listed under cross-repo actions in `docs/REVIEW.md`; this repo does not edit that schema | CCK-CAL-001 section 13, `docs/REVIEW.md` |

### Items that remain open

*Table 2. Items still Proposed, awaiting Amish (no recommendation was made).*

| # | Item | Status |
| --- | --- | --- |
| 10 | First trial partner: a repair café, an e-bike repair shop or a battery collection point | Proposed, awaiting Amish. No preference stated |
| 12 | Scheduling rule for the attended day: current stages start only if they finish the same day (12.0 cells per day), or pause overnight with the unit switched off (12.8) | Proposed, awaiting Amish. No recommendation was made; the pause rule adds an unquantified capacity error |
| 14 | Responses to the requirements at risk: R11 (mass; a 1.2 mm tray saves about 0.49 kg but thins the containment) and R5 (throughput). R12 is now met through item 4 | Proposed, awaiting Amish. No choice has been made |
| 16 | Grade A resistance limit per cell model (60 mΩ default) | Proposed, awaiting Amish. Needs named cell data sheets; no value was recommended |

## Consequences

- R9 is met on analysis, and R14 is met by design as redefined. The original R14 target (overnight grading without a person present) is superseded, not met.
- The budget is $175, so R12 is met at $164.
- The temperature-gated resistance pulse makes R4 met on the error budget (±2.09 mΩ against ±3.0 mΩ).
- Attended-only operation makes throughput depend on scheduling; R5 is at risk at exactly 12.0 cells per day, and the scheduling rule (item 12) is still open.
- The second-life SwapCell variant needs the SwapCell project's agreement and a pack design of its own. CellCheck supplies graded cells and records only.
- TRL 4 is on hold by Amish's instruction.
