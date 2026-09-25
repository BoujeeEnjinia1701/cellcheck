# Review note: CellCheck

## Session 2026-09-25: /populate to a strong TRL 2

### What was done

- `docs/01-problem.md` (CCK-PRB-001 v0.2): problem with cited reuse potential, cell spread, e-waste and fire figures; prior work (single-cell open testers, closed analyzers, lab cyclers); users and context; constraints; out of scope; open questions.
- `docs/03-requirements.md` (CCK-REQ-001 v0.2): 17 measurable requirements (R1 to R17), a status table and assumptions.
- `docs/02-concept.md` (CCK-PRC-001 v0.2): eight-step test sequence, 15 numbered components, grading rules, first-order numbers with assumptions, design choices, relation to SwapCell, CellGuard and ReflowEconomy, safety, open questions.
- `cad/src/concept_media.py`: massing model of the eight-channel grader in its steel tray, with a 48-cell rest rack and a 12 V adapter, and a bench top and salvaged laptop pack as grey context for scale.
- `media/`: `hero.png`, `concept-blueprint.png`, `.pdf` and `.svg`, `exploded.png` with callouts 1 to 15, `flow.png` (material flow per 100 salvaged cells, estimates), `model.glb` and `viewer.html`. No cutaway: the unit is open-topped, so the hero and exploded views already show every internal part.
- `bom/bom.csv`: 17 lines with indicative prices, lines 1 to 15 matching the exploded view; `bom/bom-notes.md` updated.
- `README.md`: hero image and links line; concept rationale, burning platform, industry and region tables and origin expanded with cited sources; problem, concept, key components and safety brought in line with the precis.
- `docs/pdf/`: branded PDFs of the three controlled documents.

### Key results (estimates, to be checked at TRL 3)

| Quantity | Estimate | Requirement |
| --- | --- | --- |
| Channels and cells | 8 channels, 18650 and 21700 lithium-ion | R1 met |
| Time per cell | about 6.5 h (6 to 8 h) | |
| Throughput | about 12 cells per attended 10 h day; about 28 per 24 h if run overnight | R5 met, thin margin |
| Capacity accuracy | about ±1 % calibrated, ±2 % uncalibrated | R2 met on estimate |
| Resistance resolution | about 0.8 mΩ per count, ±3 mΩ repeatability expected | R4 met on estimate |
| Heat at full discharge load | about 29 W average, 34 W peak | R8 met on estimate |
| Yield of graded cells | about 66 per 100 salvaged cells (assumption) | |
| Size and mass | 460 x 300 x 90 mm, about 3.5 kg without adapter | R11 met |
| Parts cost | about $159 against $160 | R12 met, about $1 margin |

Requirements not met or at risk:

- **R9 (single-fault safety) not met:** charger modules limit voltage on their own, but a stuck-on load MOSFET can drain a cell below 2.5 V, and temperature cutoffs rely on firmware.
- **R14 (unattended operation) not met:** the concept requires a person present while cells charge or discharge.
- **R3 at risk:** voltage accuracy before calibration is about ±10 mV from typical data sheet figures, unchecked.
- **R10 at risk:** tray, liner and guard containment of a venting cell is a concept only.
- **R13 at risk:** depends on the builder using a certified adapter.

### Proposed, awaiting Amish

1. **SwapCell link (affects the pitch).** SwapCell's precis and BOM specify new, matched 5 Ah 21700 cells at 10 A each, which typical laptop cells cannot meet. Options: (a) keep the pitch and plan a second-life SwapCell variant (graded power tool cells, or a low-current storage pack for PowerBox), agreed with the SwapCell project; (b) reword the pitch to "rebuilt packs for lights and small storage" and drop the SwapCell example; (c) leave both unchanged. Recommendation: (a), with the variant studied at TRL 3. The README notes that SwapCell use is not yet settled; `project.yaml` pitch and problem were not changed.
2. **Unattended overnight operation (safety trade-off).** Options: never; allowed only inside a fire-rated metal cabinet with a remote smoke alarm; allowed only for the rest-rack stage (no current flowing). Recommendation: attended only for charge and discharge; rest rack may be left.
3. **Single-fault protection.** Add a hardware watchdog that removes load gate drive when the controller stops, plus a per-channel undervoltage comparator, about $5 in total, to meet R9. This would take the BOM to about $164. Recommendation: add, with a budget change to $175 (see item 4).
4. **Budget.** `budget_usd` is unchanged at $160 and the BOM is at about $159. Options: (a) raise to $175 for the watchdog and margin; (b) keep $160 and add the watchdog by dropping the display (web page only). Recommendation: (a).
5. **Grading thresholds** (Table 2 of the precis), the 14-day rest at 4.10 V with a 50 mV limit, and the ±1 % group tolerance. Recommendation: adopt as starting values and tune with the first 100 real cells.
6. **Module choices:** TP5100-class charger, INA226-class monitor with a 25 mΩ shunt, ESP32-S3 class controller. Recommendation: as listed.
7. **Eight channels with a linear load** rather than 16 channels or regenerative discharge. Recommendation: eight, linear.
8. **LFP profile** in the first release or later. Recommendation: later, after the lithium-ion profile is proven.
9. **Record format:** map the CSV to ReflowEconomy's material passport at TRL 3. Recommendation: yes.
10. **First trial partner:** a repair café, an e-bike repair shop or a battery collection point.

### Safety concerns

- Salvaged cells can hide internal damage; charging them can lead to venting and fire. The documents require rejection of damaged and deeply discharged cells, per-cell temperature cutoffs, a steel tray and guard, and attended operation.
- Pack disassembly (cutting nickel strip) can short cells; covered as a safety note, not designed here.
- No independent second layer against load faults yet (R9).
- Heatsink surfaces up to about 70 °C.
- Grades must not be presented as a safety certification of any cell or pack.

### Recommended next step

Review this note and the media, and decide items 1 to 4. If approved, run `/advance-trl3` to check the thermal budget, measurement error budgets and cycle time by calculation, write the failure mode analysis for R9, and produce the parametric model and drawing sheet.
