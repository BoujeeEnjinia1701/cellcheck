---
doc_id: CCK-DDR-001
title: CellCheck TRL 2 review decisions
project: CellCheck
doc_type: Design decision record
version: "0.1"
status: Draft
date: '2026-09-25'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-09-25'
  author: Amish Chadha
  change: Record the TRL 2 review items adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review, and the items that stay open
---

# 0001: TRL 2 review decisions

- **Date:** 2026-09-25
- **Status:** proposed. The recommendations in items 1 to 3 and 5 to 9 are adopted for TRL 3 work pending Amish's review; items 4 and 10 to 16 remain proposed, awaiting Amish.

## Context

The TRL 2 review note (`docs/REVIEW.md`, session of 2026-09-25) listed ten items as "Proposed, awaiting Amish", nine of them with a recommendation. On 2026-09-25 Amish asked for this batch of repos to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the CellCheck items one by one. Under that instruction, each item that has a recommendation is adopted as recommended for TRL 3, open for his review; items without a recommendation stay open. Budgets are not changed in `project.yaml`: a recommended budget is recorded here as awaiting Amish. TRL 4 is on hold by Amish's instruction.

## Options considered

The options for each item are in `docs/REVIEW.md` (TRL 2 session) and CCK-PRC-001 v0.2. They are not repeated here.

## Decision

*Table 1. Items adopted for TRL 3 work.*

| # | Item | Status and content | Where it now lives |
| --- | --- | --- | --- |
| 1 | SwapCell link (affects the pitch) | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Option (a): keep the pitch and plan a second-life SwapCell variant, agreed with the SwapCell project. The TRL 3 study (CCK-CAL-001 section 10) finds a low-current 13S4P storage pack for PowerBox feasible at about 334 Wh and 165 W; e-bike use is ruled out. No pitch rewording was recommended, so `project.yaml` and the README keep their pitch and problem lines | CCK-PRC-001 v0.3, CCK-PRB-001 v0.3, CCK-CAL-001 section 10, README |
| 2 | Unattended operation (safety trade-off) | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Charge and discharge are attended only; the rest stage (no current flowing) may be left unattended | CCK-REQ-001 v0.3 R14 (redefined), CCK-PRC-001 v0.3 safety, README |
| 3 | Single-fault protection | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. A hardware watchdog removes all charge enables and load gate drive when the controller stops, and a per-channel undervoltage comparator removes load gate drive below 2.5 V, about $5. The budget change that came with this recommendation is item 4 | `bom/bom.csv` line 18, `cad/src/model.py` part 18, CCK-CAL-001 section 6, CCK-REQ-001 v0.3 R9 |
| 5 | Grading thresholds, 14-day rest with a 50 mV limit, ±1 % group tolerance | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Starting values, to be tuned with the first 100 real cells | CCK-PRC-001 v0.3 Table 2, CCK-REQ-001 v0.3 R6 and R15 |
| 6 | Module choices | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. TP5100-class charger, INA226-class monitor with a 25 mΩ shunt, ESP32-S3 class controller | CCK-PRC-001 v0.3 Table 1, `bom/bom.csv` lines 6, 7 and 11 |
| 7 | Channel count and load type | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Eight channels with a linear load; 16 channels and regenerative discharge are later variants | CCK-PRC-001 v0.3 |
| 8 | LFP profile | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. Later, after the lithium-ion profile is proven | CCK-PRC-001 v0.3, CCK-PRB-001 v0.3 |
| 9 | Record format | Adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. The per-cell CSV stays the primary record; each matched group and each reject lot maps to ReflowEconomy's material passport v0.2 (two schema gaps, see item 15) | CCK-CAL-001 section 13, CCK-PRC-001 v0.3 |

### Items that remain open

*Table 2. Items still Proposed, awaiting Amish.*

| # | Item | Status |
| --- | --- | --- |
| 4 | Budget | Proposed, awaiting Amish. Recommendation (a): raise `budget_usd` to $175. `budget_usd` stays at $160 in `project.yaml`. CCK-CAL-001 states the cost against both figures: $164 is $4 over $160 and $11 under $175 |
| 10 | First trial partner: a repair café, an e-bike repair shop or a battery collection point | Proposed, awaiting Amish. No preference stated |
| 11 | DC four-wire resistance rather than 1 kHz AC impedance, and the 14-day (rather than 7-day) rest | Proposed, awaiting Amish. The precis recommends DC and 14 days; these were not separate items in the TRL 2 review, so they are not adopted here. CCK-CAL-001 uses DC and 14 days as its working basis |
| 12 | Scheduling rule for the attended day: current stages start only if they finish the same day (12.0 cells per day), or pause overnight with the unit switched off (12.8) | Proposed, awaiting Amish. No recommendation was made; the pause rule adds an unquantified capacity error |
| 13 | TRL 3 engineering proposals from CCK-CAL-001: read self-discharge in the same channel and against the median of the same-day cohort (R6); start the resistance pulse only within 1 K of the bench (R4); per-channel two-point voltage calibration at build (R3); stop discharges on a fan or heatsink fault (R8); a plausibility check for a detached thermistor (R9) | Engineering proposals, awaiting Amish's confirmation |
| 14 | Responses to the requirements CCK-CAL-001 finds not met or at risk: R12 (cost, depends on item 4), R11 (mass; a 1.2 mm tray saves about 0.49 kg but thins the containment), R5 (throughput) | Proposed, awaiting Amish. No choice has been made |
| 15 | ReflowEconomy passport gaps: no `product_form` for graded cells and no electrical test in `identification.method` | Raised for the ReflowEconomy project; this repo does not edit that schema |
| 16 | Grade A resistance limit per cell model (60 mΩ default) | Open; needs named cell data sheets, not done at TRL 3 |

## Consequences

- R9 is met on analysis, and R14 is met by design as redefined. The original R14 target (overnight grading without a person present) is superseded, not met.
- Parts cost rises to $164. R12 is not met against the $160 in `project.yaml` and would be met against the recommended $175.
- Attended-only operation makes throughput depend on scheduling; R5 is at risk at exactly 12.0 cells per day.
- The second-life SwapCell variant needs the SwapCell project's agreement and a pack design of its own. CellCheck supplies graded cells and records only.
- TRL 4 is on hold by Amish's instruction.
