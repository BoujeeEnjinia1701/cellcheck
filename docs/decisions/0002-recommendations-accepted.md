---
doc_id: CCK-DDR-002
title: CellCheck recommendations accepted
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
  change: Record Amish's acceptance of all recommendations and what changed in the repo
---

# 0002: Recommendations accepted

- **Date:** 2026-09-25
- **Status:** accepted by Amish. Every item with a recommendation in `docs/REVIEW.md` and CCK-DDR-001 is Decided by Amish, 2026-09-25: go with recommendation. Items without a recommendation stay Proposed, awaiting Amish.

## Context

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Before that, the CellCheck recommendations had been adopted for TRL 3 work only, open for his review (CCK-DDR-001 v0.1). This record lists each newly decided item, what changed in the repo because of it, and what stays open. Where a recommendation offered several options, the recommended option is the decision. The portfolio stays at TRL 3; work that needs a build, a test, firmware beyond a sketch or purchasing is recorded as decided but on hold, because TRL 4 is on hold by Amish's instruction.

## Decision

*Table 1. Items decided on 2026-09-25 and the resulting changes.*

| # (DDR-001) | Decision | What changed in the repo |
| --- | --- | --- |
| 1 | Keep SwapCell in the pitch and plan a second-life SwapCell variant (option a) | Wording in CCK-PRB-001 v0.4, CCK-PRC-001 v0.4 and the README changed from "adopted, open for review" to decided. Pitch and problem lines unchanged (no rewording was recommended). Agreement with SwapCell and PowerBox is a cross-repo action |
| 2 | Charge and discharge attended only; the rest stage may be left | Wording only; R14 as redefined in CCK-REQ-001 v0.3 stands |
| 3 | Hardware watchdog and per-channel undervoltage comparators | Wording only; BOM line 18 and model part 18 were already in place |
| 4 | Budget raised to $175 (option a) | `project.yaml` `budget_usd` 160 to 175; R12 target in CCK-REQ-001 v0.4 $160 to $175; R12 status Not met ($4.00 over) to Met ($11.00 under); CCK-CAL-001 v0.2 section 11 and `sizing.py`; README budget line; BOM notes |
| 5 | Grading thresholds, 14-day rest with 50 mV limit and ±1 % group tolerance as starting values | Wording only. Tuning with the first 100 real cells is TRL 4 work: decided, on hold |
| 6 | TP5100, INA226 and ESP32-S3 class modules | Wording only. Purchasing is TRL 4: on hold |
| 7 | Eight channels with a linear load | Wording only |
| 8 | LFP profile later | Wording only |
| 9 | Per-cell CSV mapped to ReflowEconomy's passport v0.2 | Wording only |
| 11 | DC four-wire resistance and a 14-day rest | Moved from "Proposed, awaiting Amish" to decided in CCK-PRC-001 v0.4; CCK-CAL-001 already used them |
| 13 | Firmware and build rules from CCK-CAL-001: same-channel, cohort-median self-discharge reading; resistance pulse only within 1 K of the bench; per-channel calibration; fan-fault stop; detached-thermistor plausibility check | `sizing.py` now uses a 1 K reinsertion difference (was 2 K): R4 repeatability ±2.99 to ±2.09 mΩ worst case (±2.02 to ±1.28 mΩ RSS), R4 At risk to Met. R6 is now evaluated in the same channel (±10.6 to ±2.3 mV) but stays at risk because the spread of relaxation is not bounded. The rules are written into CCK-PRC-001 v0.4 steps 3 and 6 and the safety section. Firmware, calibration and tests are TRL 4 work: decided, on hold |
| 15 | Raise the two passport schema gaps with ReflowEconomy | Listed under cross-repo actions in `docs/REVIEW.md`; no other repo edited |

No part was added or resized, so `cad/src/model.py`, the STEP and STL files and the general arrangement CCK-DWG-001 are unchanged in geometry and notes; the drawing stays at Rev P1 and was only re-rendered.

*Table 2. Requirement status after this record (CCK-CAL-001 v0.2).*

| Status | Requirements |
| --- | --- |
| Not met | None (R12 was not met before this record) |
| At risk | R5, R6, R11 |
| Not verifiable at TRL 3 | R10 |
| Met on paper | R1, R2, R3, R4, R7, R8, R9, R12, R13, R14, R15, R16, R17 (13 of 17; was 11) |

## Items still open

*Table 3. Items that had no recommendation and stay Proposed, awaiting Amish.*

| # (DDR-001) | Item |
| --- | --- |
| 10 | First trial partner: repair café, e-bike repair shop or battery collection point (no preference stated) |
| 12 | Scheduling rule for the attended day: finish current stages the same day, or pause overnight with the unit off |
| 14 | Responses to R11 (mass) and R5 (throughput) |
| 16 | Grade A resistance limit per cell model (needs named data sheets) |

## Consequences

- CellCheck has no requirement failed outright on paper. R5, R6 and R11 remain at risk and R10 cannot be verified before a physical test.
- Cross-repo actions (SwapCell and PowerBox for the second-life pack, ReflowEconomy for the passport gaps) are listed in `docs/REVIEW.md`; no other repo was edited.
- `trl` and `trl_target` stay at 3. TRL 4 is on hold by Amish's instruction.
