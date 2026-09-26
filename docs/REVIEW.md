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

Status update: items 1 to 9 are Decided by Amish, 2026-09-25: go with recommendation (CCK-DDR-002); item 10 has no recommendation and stays Proposed, awaiting Amish.

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

## Session 2026-09-25: TRL 3

Amish asked for this batch to be taken through the usual process with the instruction "you know the drill, nothing gets past TRL 3". He has not reviewed the CellCheck TRL 2 items one by one, so each item with a recommendation is adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review. TRL 4 is on hold by Amish's instruction.

### What was done

- `docs/decisions/0001-trl2-review-decisions.md` (CCK-DDR-001 v0.1, status proposed): items 1 to 3 and 5 to 9 adopted for TRL 3 pending Amish's review; items 4 and 10 to 16 stay open.
- `docs/04-calcs/01-sizing.md` (CCK-CAL-001 v0.1) with `docs/04-calcs/sizing.py` and `results.csv`: cycle time and a day-by-day throughput simulation, power and energy, heatsink and MOSFET temperatures, error budgets for capacity, voltage, resistance, self-discharge and temperature, the R9 failure mode analysis, a containment estimate, size and mass, grading and matching on synthetic cells, a second-life SwapCell study, cost, and the mapping to ReflowEconomy's material passport.
- `cad/src/model.py`: parametric build123d model (tray with intake slots, base plate, eight four-wire holders, guard, module rows, heatsink with 40 vertical fins, fan shroud, controller, watchdog board, display, inlet, adapter, rest rack). Exports `cad/step/` and `cad/stl/` for the assembly, tray, heatsink, holders and rest rack; prints volumes and a clash check (no clashes).
- `cad/src/sheets.py` and `cad/drawings/CCK-DWG-001.svg`, `.pdf` and `.png`: general arrangement at Rev P1, "PRELIMINARY, NOT FOR FABRICATION". The concept sheet keeps CCK-DWG-010, so DWG-001 was the first free number.
- `bom/bom.csv`: 18 lines, all priced with supplier types; new line 18 (watchdog and undervoltage board, $5.00). `bom/bom-notes.md` updated.
- `cad/src/concept_media.py` now builds from `model.py`; `media/` refreshed (hero, blueprint, exploded with callout 18, flow, GLB and viewer). No cutaway, as at TRL 2: the unit is open-topped, so the kit's cutaway is not used. The flow diagram losses now sit under the stage that removes them. Temporary `media/_views*` folders deleted.
- Docs bumped to v0.3 with revision rows: CCK-PRB-001, CCK-PRC-001 (numbers from CAL-001, adopted choices, heatsink orientation, component 18), CCK-REQ-001 (R14 redefined, R3 calibration, R12 against both budgets, status table from CAL-001).
- `README.md`: TRL 3 badge, links to the drawing and CAL-001, numbers from CAL-001, SwapCell wording aligned with DDR item 1; the required sections are unchanged in order.
- `project.yaml`: `trl: 3`, `trl_target: 3`, evidence list. Pitch, problem and `budget_usd` unchanged.

### Requirements (CCK-CAL-001)

Met on paper: 11 of 17. Not met and at risk first:

| ID | Status | Value |
| --- | --- | --- |
| R12 | **Not met** | $164.00 against $160; $11.00 under the recommended $175 |
| R4 | At risk | ±2.99 mΩ worst case against ±3.0 mΩ; cell temperature dominates |
| R5 | At risk | 12.0 cells per attended day on the stage-boundary rule; 12.8 with an overnight pause; 8.0 for 2.5 Ah cells |
| R6 | At risk | ±10.6 mV across channels, ±2.3 mV in the same channel; relaxation after charge not bounded |
| R11 | At risk | 4.97 kg against 5 kg; 460 x 300 x 75 mm |
| R10 | Not verifiable at TRL 3 | Containment of a venting cell cannot be analysed credibly on paper |
| R1, R2, R3, R7, R8, R9, R13 to R17 | Met (R3 with per-channel calibration; R9 on analysis; R15 on synthetic data) | See CCK-CAL-001 Table 4 |

Key numbers: 6.33 h per 1.8 Ah cell; 42.5 W adapter load; 16.8 Wh per cell from the mains; 33.6 W peak heat, 0.58 K/W heatsink, MOSFET cases 58.7 °C (about 99 °C if both fans stop); capacity ±1.1 % uncalibrated; voltage ±12.4 mV uncalibrated and ±4.8 mV calibrated.

Corrections to TRL 2 figures: time per cell 6.5 to 6.33 h; voltage error ±10 to ±12.4 mV before calibration; capacity error ±2 to ±1.1 %; height 90 to 75 mm; mass 3.5 to 4.97 kg (the tray alone is 2.43 kg); cost $159 to $164. The TRL 2 massing model had heatsink fins across the fan airflow; they are now in line with it.

### Decisions recorded (CCK-DDR-001)

Status update: all of these are now Decided by Amish, 2026-09-25: go with recommendation (CCK-DDR-002). Originally adopted as recommended for TRL 3 under Amish's 2026-09-25 instruction, open for his review: (1) keep the pitch and plan a second-life SwapCell variant, studied in CAL-001 section 10 (low-current PowerBox storage pack, about 334 Wh and 165 W; e-bike use ruled out); (2) charge and discharge attended only, rest stage may be left, so R14 is redefined; (3) hardware watchdog and per-channel undervoltage comparators; (5) grading thresholds, 14-day rest with 50 mV limit and ±1 % group tolerance as starting values; (6) TP5100, INA226 and ESP32-S3 class modules; (7) eight channels with a linear load; (8) LFP profile later; (9) record mapped to ReflowEconomy's passport v0.2. No pitch or problem rewording was recommended, so both are unchanged.

### Items still awaiting Amish

- Budget: $175 recommended (item 4). Now Decided by Amish, 2026-09-25: go with recommendation; `budget_usd` is $175.
- First trial partner: repair café, e-bike repair shop or collection point; no preference stated (item 10).
- DC four-wire resistance and the 14-day rest (in the precis, not separate TRL 2 review items) (item 11). Now Decided by Amish, 2026-09-25: go with recommendation.
- Scheduling rule for the attended day: finish current stages the same day, or pause overnight with the unit off (item 12).
- Engineering proposals from CAL-001: same-channel and same-day cohort self-discharge reading, temperature-gated resistance pulse, per-channel calibration, fan-fault stop, detached-thermistor plausibility check (item 13). Now Decided by Amish, 2026-09-25: go with recommendation.
- Responses to R12, R11 (a 1.2 mm tray saves 0.49 kg but thins the containment) and R5 (item 14). R12 is resolved by item 4; R11 and R5 stay open.
- Grade A resistance limits per cell model need named data sheets (item 16).

### Cross-repo notes (not edited in the other repos)

- **ReflowEconomy:** the material passport v0.2 has no `product_form` for graded cells and no electrical test in `identification.method`. Raised here for the ReflowEconomy project (item 15).
- **SwapCell and PowerBox:** a second-life pack would limit discharge to about 3.5 A and charge to 0.5C, below PowerBox's 5.0 A charge and 300 W inverter; PowerBox would need a lower host charge limit and AC limit for that pack. Needs the SwapCell project's agreement.
- **CellGuard:** consistent. CellCheck assumes CellGuard's NMC-capable hardware with LFP firmware first, as adopted in CGD-DDR-001 item 7. No other shared component (FieldNode, MotionCore, ThermaCart, TwinKit, CalRig) is used.

### Safety concerns

- Salvaged cells can hide damage; charge and discharge now require a person present. The failure mode analysis covers the R9 faults on paper, but a detached thermistor clip goes undetected.
- If both fans stop, the MOSFET cases could approach 99 °C; the firmware must stop discharges on a fan or heatsink fault.
- Containment is unverified, and the new fan intake slots are an opening in the tray wall. The 100 kJ runaway figure in CAL-001 section 7 is an assumption with no source yet and must be replaced by a cited value.
- Grades must not be presented as a safety certification of any cell or pack.

### Citations and other checks

- No unchecked citations were listed in this note, so no WebFetch was needed. The INA226-class and ESP32-class figures in CAL-001 are typical data sheet values used as assumptions, not verified against a data sheet in this session.
- No TRL 4 material exists in the repo (`build-log/` holds only its README and `.gitkeep`; `firmware/` and `electronics/` are empty).

### Recommended next step

Amish to review CCK-DDR-001, decide the budget (item 4) and the trial partner (item 10), and confirm or change the adopted items and engineering proposals. TRL 4 is on hold by Amish's instruction. For reference only, TRL 4 would need: a built unit; bench test reports (TST, `environment: lab`) for capacity, voltage, resistance repeatability and self-discharge against a calibrated reference; a fault-injection test of the watchdog, comparators and fuses; a fan-failure thermal test; a containment test with a sourced cell failure method in a suitable facility; and dated build-log entries.

## Session 2026-09-25: recommendations accepted

On 2026-09-25 Amish wrote: "i accept all your recommendations, go with them across all repos." Every item above with a recommendation is now **Decided by Amish, 2026-09-25: go with recommendation**; where several options were offered, the recommended option is the decision. Items without a recommendation stay Proposed, awaiting Amish. The record is `docs/decisions/0002-recommendations-accepted.md` (CCK-DDR-002 v0.1); CCK-DDR-001 is updated to v0.2.

### Decisions applied and what changed

| DDR-001 item | Decision | Change (before to after) |
| --- | --- | --- |
| 4 | Budget raised (option a) | `budget_usd` $160 to $175; R12 target $160 to $175; R12 Not met ($4.00 over) to Met ($11.00 under) |
| 13 | Firmware and build rules from CCK-CAL-001 | Resistance pulse starts only within 1 K of the bench: R4 worst case ±2.99 to ±2.09 mΩ (RSS ±2.02 to ±1.28 mΩ), At risk to Met. Self-discharge read in the same channel against the same-day cohort median: R6 reading ±10.6 to ±2.3 mV, still at risk (relaxation spread not bounded). Fan-fault stop, per-channel calibration and a detached-thermistor plausibility check written into the precis |
| 11 | DC four-wire resistance and 14-day rest | Proposed to decided; no numbers change |
| 1 | Keep SwapCell in the pitch; plan a second-life variant (option a) | Wording only; pitch and problem unchanged; cross-repo action below |
| 2, 3, 5, 6, 7, 8, 9 | Attended charge and discharge; watchdog and comparators; grading thresholds; modules; eight linear channels; LFP later; passport mapping | Wording only; already implemented at TRL 3 |
| 15 | Raise passport gaps with ReflowEconomy | Listed under cross-repo actions |

Documents bumped with a revision row "Recommendations accepted by Amish (DDR-002)": CCK-PRB-001 v0.4, CCK-PRC-001 v0.4, CCK-REQ-001 v0.4, CCK-CAL-001 v0.2 (with `sizing.py` and `results.csv`), CCK-DDR-001 v0.2. `project.yaml` (budget, evidence list), `README.md` and `bom/bom-notes.md` updated. No part was added or resized, so `model.py`, STEP, STL and CCK-DWG-001 (Rev P1) are unchanged in geometry and notes; they, the concept media and all PDFs were regenerated. The README "What sparked the idea" section now traces the idea to IBM Research India's 2014 UrJar project.

### Requirement status (CCK-CAL-001 v0.2)

Met on paper: 13 of 17 (was 11). None is failed outright.

| ID | Status | Value |
| --- | --- | --- |
| R5 | At risk | 12.0 cells per attended day (stage-boundary rule); 12.8 with an overnight pause; 8.0 for 2.5 Ah cells |
| R6 | At risk | ±2.3 mV in the same channel against ±3 mV; spread of relaxation between cells not bounded |
| R11 | At risk | 4.97 kg against 5 kg; 460 x 300 x 75 mm |
| R10 | Not verifiable at TRL 3 | Containment of a venting cell cannot be analysed credibly on paper |
| R4 | Met | ±2.09 mΩ worst case against ±3.0 mΩ (was at risk) |
| R12 | Met | $164.00 against $175 (was not met against $160) |
| R1, R2, R3, R7, R8, R9, R13 to R17 | Met | Unchanged; see CCK-CAL-001 Table 4 |

### Items still awaiting Amish (no recommendation was made)

- First trial partner: repair café, e-bike repair shop or collection point (item 10).
- Scheduling rule for the attended day (item 12).
- Responses to R11 and R5 (item 14).
- Grade A resistance limit per cell model; needs named data sheets (item 16).

### Cross-repo actions (no other repo edited)

- **SwapCell and PowerBox:** agree the second-life low-current storage pack (about 334 Wh, 3.5 A discharge, 0.5C charge); PowerBox would need a lower host charge limit and an AC limit of about 150 W for that pack (item 1).
- **ReflowEconomy:** add a `product_form` for graded cells and an electrical test in `identification.method` to the material passport schema (item 15).
- **CellGuard:** none; consistent with CGD-DDR-001 item 7.

### Decided but on hold (TRL 4)

Tuning the grading thresholds on the first 100 real cells (item 5), buying modules (item 6), writing and testing the firmware rules and doing the per-channel calibration (item 13), and every test listed in the previous session. TRL 4 remains on hold by Amish's instruction; `trl` and `trl_target` stay at 3.

### Safety concerns

Unchanged from the TRL 3 session. The detached-thermistor plausibility check narrows but does not remove that residual risk, and the 100 kJ runaway figure in CCK-CAL-001 section 7 still needs a sourced value before any TRL 4 work.
