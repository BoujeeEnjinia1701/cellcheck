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

## Session 2026-09-26: product appearance model and photoreal renders

Amish chose this repo for the first batch of product renders on 2026-09-26. This session added an appearance model for photoreal product shots; it changes no design parameter.

### What was done

- `cad/src/product_model.py` (new): `product_parts()` returns 91 coloured, material-tagged parts (shell 16, internal 46, accessory 14, context 15) with BOM numbers and explode offsets, plus `TITLE` and `RENDER_VIEWS` (hero, exploded, detail). All dimensions come from `PARAMS`, `channel_x()` and `heatsink_extent()` in `cad/src/model.py`, which is unchanged.
- `README.md`: the hero image now points to `media/render-hero.png`, and the links line starts with the exploded render. Both files are produced later by the render pipeline.

What the appearance model adds:

- Steel tray with rounded corners, a rolled rim, rounded intake slots, a teal nameplate and a lithium warning label; ceramic fibre liner shown separately.
- Aluminium base plate with hex standoffs, fixing screws and printed channel numbers 1 to 8.
- Filleted cell holders with two nickel contacts at each end (force and sense) and solder tabs; 18650 cells with ID labels and insulator rings in six of the eight bays; saddle-shaped thermistor clips, with the two spare clips parked on the empty holders.
- Slotted perforated guard with foot flanges and screws.
- Populated charger modules, sense boards with lit status LEDs, TO-220 MOSFETs with clamp screws, the finned heatsink, fan shroud and two fans with blades, hubs and finger guards.
- Controller board, watchdog perfboard with DIP packages, a charcoal display stand with dark glass, lit channel rows and three buttons, and a power inlet with rocker switch, fuse holder, DC jack and power LED.
- Accessories: the rest rack with column numbers and resting cells, and the 12 V adapter with its rating label and cable to the inlet.
- Context: a silicone bench mat and three bins labelled A, B and C holding matched cells.

### Differences from model.py (Proposed, awaiting Amish)

- **18650 cells in the bays.** `model.py` draws 21700 cells (the largest accepted) in all eight bays; the render shows 18650 cells, the common salvaged size, in six bays with two bays empty so the contacts are visible. The thermistor clips sit lower to match. Recommendation: accept for the renders; the model keeps the 21700 envelope for clearance checks.
- **Matched group bins A, B and C.** These are not in `bom/bom.csv`. They show where graded cells go after matching. Options: (a) keep them as render context only, (b) add a BOM line for three printed or bought bins, costed against the $175 budget. Recommendation: (a) for now, and decide (b) with the rest of the TRL 4 purchasing.
- **Fan finger guards.** Not in the BOM; they sit 1 mm behind the fans and change no clearance. Recommendation: add them to BOM line 10 at TRL 4 and cost them then.
- **Perforation pattern.** The guard is drawn with slots at about 50 % open area instead of round holes, and the sheet is shown 1.0 mm thick instead of 0.8 mm. Recommendation: accept as an appearance choice; the BOM specification stays as written.
- **Channel status LEDs, labels and screws** are appearance details placed on existing BOM items (lines 2, 5, 7, 8 and 17).

### Status

This is an appearance model only: no tolerances, PCB layouts or fabrication detail. `trl` and `trl_target` stay at 3, and TRL 4 remains on hold.

## Session 2026-09-27: kit 1.5.0 and image quality

- Kit 1.5.0 synced: STANDARDS v1.5 (sections 12 to 15: product renders, storefront images and image quality, public release, authorship and signing), `.kit/cards.py`, `.kit/image_qc.py`, `.kit/release_gate.py`, issue templates, and the `/render-product` and `/release` commands. `CLAUDE.md` now matches `.kit/CLAUDE.md`.
- Every `media/render-*.png` recaptioned from its original render with the new layout: the title, concept label and repository sit in a band above the render and the view note in a band below it, each line wrapped to the image width, so no text overlaps other text or the render or runs off the image. `media/card.png` and `media/social-preview.png` regenerated with the same rules.
- `python .kit/image_qc.py` and `python .kit/release_gate.py` pass. trl stays 3.

## Session 2026-10-01: design made constructable and prototype build plan (kit 1.7.0)

Amish approved the build plan format on 2026-09-30 and asked for it across all repos, with outstanding decisions kept out of the build plan in a separate design decisions register. Kit 1.7.0 is installed (`.kit/`, `.claude/commands/`, root `CLAUDE.md`).

### What was done

- Constructability review with build123d of every part: what touches what, what holds it, and whether it can be made as described. `cad/src/model.py` now builds every component with its fixings and runs 129 constructability checks (`python cad/src/model.py --check`); all pass.
- `docs/decisions/0003-design-for-construction.md` (CCK-DDR-003 v0.1, Draft): every change, with the reason, made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review.
- `docs/05-build-plan.md` (CCK-BLD-001 v0.1): the illustrated build plan, with no open decisions in it.
- `docs/06-design-decisions.md` (CCK-DEC-001 v0.1): 11 open decisions, 10 items to confirm when parts are bought, and the decisions made.
- `cad/src/build_plan_media.py`: overview, 10 making sketches (`cad/drawings/CCK-DWG-101` to `110`), a plate hole layout, 7 joint close-ups, 11 step pictures and the block wiring diagram (the picture for step 9), all in `docs/05-build-plan/`.
- `bom/bom.csv`: lines 19 (rubber feet), 20 (fixings) and 21 (5 V converter) added; lines 1 to 5, 7 to 10, 12, 13 and 16 respecified. $172.40 estimated, $2.60 under the $175 value-engineering target.
- Recalculated: CCK-CAL-001 v0.3 (size, mass, cost), with `sizing.py` and `results.csv`; CCK-PRC-001 v0.5 and CCK-REQ-001 v0.5 updated to match.
- Regenerated: STEP and STL, the general arrangement CCK-DWG-001 at Rev P2, and the concept media (`hero.png`, `exploded.png`, `flow.png`, `concept-blueprint`, `model.glb`, `viewer.html`).
- `project.yaml`: `design_state: constructable`; the build plan, register and CCK-DDR-003 added to `trl_evidence`. `README.md`: links line and a "Building the prototype" section with the overview picture.

### Design changes made for construction (CCK-DDR-003)

1. Six rubber feet with M4 studs through the tray floor into six 12 mm hex standoffs on the bare steel; the plate screws onto them (the concept's four standoffs rested loose on the liner).
2. Base plate 1.5 mm on six standoffs instead of 2 mm on four; every screw reachable from above (two concept screws sat under the display and the inlet).
3. Two M3 screws per cell holder; two 16 x 5 mm wire slots per channel through the plate, leads run underneath.
4. Guard folded from one perforated steel blank with end flanges, held by two M4 thumb screws into rivet nuts in the plate; lifts off to change cells.
5. Every board on two 5 mm nylon standoffs; controller and watchdog board moved 10 mm right to clear the thumb screw.
6. Display stand enlarged to 88 x 62 mm to take a 2.8 in display module (the concept's 60 mm stand was too small); buttons in its foot.
7. Heatsink screwed to the plate from below; each MOSFET clamped with an insulated M3 screw.
8. Fan shroud folded with side flanges screwed to the spine ends; fans screwed from inside; the unfoldable top lip dropped.
9. Thermistor clip made a printed C-clip, in 21700 and 18650 sizes.
10. Inlet housing printed open-bottomed with the jack, fuse holder and switch on top (the concept's jack faced the tray wall 23 mm away).
11. Added the 5 V converter; the channel board now carries the charge switch, the load loop's op-amp and the 3 A fuse clips.
12. Cells rest in their holder grooves and touch both contacts.

### Key results

- Size 460 x 300 x 85 mm (was 75 mm high); mass 4.91 kg (was 4.97 kg); parts $172.40 (was $164.00).
- No requirement changed status: none not met; R5, R6 and R11 at risk (R11 margin now 0.09 kg); R10 not verifiable at TRL 3; 13 met on paper.

### Proposed, awaiting Amish

- Guard hold-down (thumb screws as modelled, toggle latches or a hinge); it is part of the containment arrangement (CCK-DDR-003 A1). Recommendation: thumb screws for the prototype.
- Seal the wire slots under the guard with high-temperature silicone after wiring (CCK-DDR-003 A2). Recommendation: seal.
- The earlier open items stay open and are listed in CCK-DEC-001.

### Stale media (made on Amish's Mac; not regenerated here)

The design changed visibly (feet, guard, display stand, inlet, shroud), so `cad/src/product_model.py`, `media/render-hero.png`, `media/render-exploded.png`, `media/render-detail.png`, `media/card.png` and `media/social-preview.png` are stale and should be regenerated on the Mac.

### Safety concerns

Unchanged in substance. The guard now lifts off by hand, which is what a cell change needs but makes its hold-down part of the containment question (A1). The wire slots open the guard space to the underside of the plate inside the tray (A2). The build plan sets safety stops S1 to S7 before cells, power, first charge, first discharge and any unattended period.

### Recommended next step

Amish to review CCK-DDR-003 and decide A1 and A2 in the register. TRL 4 (building to this plan) remains on hold by Amish's instruction.

## Session 2026-10-02: open decisions decided

On 2026-10-02 Amish approved every recommendation written for the open decisions: "i approve your recommendations for all 555 open decisions." trl stays 3; nothing was built or tested.

### Decisions recorded

11 decisions recorded in the design decisions register (CCK-DEC-001 v0.3, Decisions made, dated 2026-10-02): guard hold-down (1), wire slot sealing (2), first trial partner (3), scheduling rule (4), responses to R11 and R5 (5), grade A limit per cell model (6), 18650 cells in the renders (7), bins as render context (8), fan finger guards in BOM line 10 (9), guard perforation as appearance (10) and the second-life pack study sent to SwapCell and PowerBox (11). The partner in item 3 is the first candidate to approach, not an agreed partner.

### Documents changed

- `docs/06-design-decisions.md` (CCK-DEC-001 v0.3): all 11 open items moved to Decisions made; Open decisions now reads "None"; the value-engineering savings line updated for items 8 and 9.
- `docs/decisions/0003-design-for-construction.md` (CCK-DDR-003 v0.3): status line and Table 3 record A1 and A2 as accepted; consequence added; status stays Draft; Tables 1 and 2 still open for Amish's review at that point (see Points found in the review).
- `docs/decisions/0001-trl2-review-decisions.md` (CCK-DDR-001 v0.3): items 10, 12, 14 and 16 recorded as decided.
- `docs/decisions/0002-recommendations-accepted.md` (CCK-DDR-002 v0.2): the same four items recorded as decided in Table 3.
- `docs/01-problem.md` (CCK-PRB-001 v0.6): first trial partner named as the first candidate to approach.
- `docs/02-concept.md` (CCK-PRC-001 v0.7): throughput rule, grade A limit, containment hold-down and slot sealing, fan finger guards, pack study; open questions closed.
- `docs/03-requirements.md` (CCK-REQ-001 v0.7): R5 and R11 status notes; no status changed.
- `docs/04-calcs/01-sizing.md` (CCK-CAL-001 v0.5): R5 row of Table 4 names the decided rule, and section 8 the tray decision; no number changed.
- `docs/05-build-plan.md` (CCK-BLD-001 v0.2): step 9 seals the wire slots with high-temperature silicone; silicone and fan finger guards in the bought components.
- `bom/bom-notes.md`: the decided part and material choices noted; the line 10 and 16 changes are follow-ups.
- `README.md`: the register sentence and the SwapCell paragraph.
- PDFs re-rendered with `python .kit/render.py`; superseded versions removed.

No CAD model, BOM quantity or price, or picture was changed. Requirement status is unchanged: R5, R6 and R11 at risk, R10 not verifiable at TRL 3, 13 met on paper.

### Follow-up actions to carry approved decisions into the design

1. Decision 2 (bom): Add high-temperature silicone sealant to the specification of BOM line 16 (price unchanged or re-estimated).
2. Decision 2 (pictures): Show the sealed wire slots in the step 9 picture and the plate figures of the build plan (`cad/src/build_plan_media.py`).
3. Decision 9 (bom): Add two 60 mm fan finger guards to BOM line 10 with an estimated price.
4. Decision 9 (calcs): Update the cost in CCK-CAL-001 section 11 (`sizing.py`, `results.csv`), R12 in CCK-REQ-001 and the value-engineering figure in CCK-DEC-001, README and `bom/bom-notes.md` once lines 10 and 16 are repriced.
5. Decision 9 (model): Add the finger guards to the fans in `cad/src/model.py` and the exploded view so the model matches BOM line 10.
6. Decision 11 (docs): Send the second-life pack study (CCK-CAL-001 section 10) to the SwapCell and PowerBox repositories as a proposal.
7. Decision 7 (pictures): Regenerate the appearance model and photoreal renders on Amish's Mac to the constructable design (guard, display stand, inlet, feet), keeping 18650 cells and the slotted guard as accepted appearance.

### Points found in the review

- The register had no open row asking Amish to accept CCK-DDR-003 (P1 to P12), although the decisions-made table said it was open for his review; the recommendation was "accept". Amish accepted it later on 2026-10-02 (see the next session).
- Items 4 and 5 overlap: the throughput half of item 5 is the scheduling rule of item 4.
- The 60 mΩ grade A default should not be replaced with data sheet impedance figures, which are normally 1 kHz AC values and not comparable with the DC pulse measurement.
- The appearance model and renders still show the concept guard, display, inlet and no feet.

### Safety

The guard's two thumb screws and the silicone-sealed wire slots are now part of the containment arrangement, which is still not verifiable on paper. The TRL 4 containment test must be run with the guard held by the thumb screws exactly as in the build plan. The fan finger guards are decided but not yet in the BOM.

### Recommended next step

Carry out the follow-up actions above (Amish accepted CCK-DDR-003 Tables 1 and 2 later on 2026-10-02; see the next session). TRL 4 remains on hold by Amish's instruction.

## Session 2026-10-02: design-for-construction changes accepted

Amish, 2026-10-02: "APPROVED: Design-for-construction changes in 10 repos (CityTwin, CoolShade, PalletPilot, Heliolite, PotholeLog, EarthPress, ReadyKit, CellCheck, CargoMule and ThermaCart)". This accepts the design-for-construction changes P1 to P12 in Table 1 of CCK-DDR-003, with their knock-on changes in Table 2, which were left open for his review when the open decisions were decided earlier the same day. No other item is decided by it. trl stays 3; no build or test work was done, and the model, BOM, calculations and pictures are unchanged.

### Documents changed

- `docs/decisions/0003-design-for-construction.md` (CCK-DDR-003 v0.4, status Draft): status line now "accepted" with Amish's words.
- `docs/06-design-decisions.md` (CCK-DEC-001 v0.4): Decisions made row added, dated 2026-10-02; the 2026-10-01 row no longer calls the changes open for review.
- `docs/05-build-plan.md` (CCK-BLD-001 v0.3): section 2 says CCK-DDR-003 is accepted.
- PDFs regenerated.

### Recommended next step

No change: the follow-up actions of the previous session stand. TRL 4 remains on hold by Amish's instruction.

## Session 2026-10-02: approved follow-ups carried out

Amish approved on 2026-10-02 that every follow-up action from the open-decision sign-off be carried out. trl stays 3; nothing was built or tested.

### Follow-ups

1. Decision 2, BOM: done. High-temperature silicone sealant added to line 16 ($8.00 to $12.00; a 30 g tube, estimated at $4.00 for a small tube rated to about 260 C).
2. Decision 2, pictures: done. New step 9 picture (`docs/05-build-plan/step-09.png`) showing the 16 sealed slots; plate hole figure shades the slots as sealed; joint 6 shows a seal; the seals are in the model (16 plugs, BOM 16).
3. Decision 9, BOM: done. Line 10 now "Fan with shroud and finger guard", $2.60 each for two (guard $0.60, a typical marketplace price for a 60 mm wire grill); line 20 counts eight small screws for the guards at no price change.
4. Decision 9, calculations: done. `sizing.py` and `results.csv` rerun; CCK-CAL-001 sections 8 and 11, CCK-REQ-001, CCK-PRC-001, CCK-DEC-001, README and BOM notes brought into line. Mass 4.94 kg (4.91 kg before); cost $177.60.
5. Decision 9, model: done. Finger guards (and their screws) and silicone seals added to `cad/src/model.py`, the exploded view and the build plan pictures; 139 constructability checks pass (129 before); STEP and STL regenerated.
6. Decision 11, send the second-life pack study to SwapCell and PowerBox: not done here, it lives in other repos (see Cross-repo actions).
7. Decision 7, appearance and renders: appearance model updated and render scenes exported (hero, exploded, detail); photoreal renders, `media/card.png` and `media/social-preview.png` are made on Amish's Mac.

### Requirement status changes

- R12: from "within the value-engineering target" to "over the value-engineering target". Value-engineering target: USD 175.00. Estimated cost of the constructable design: USD 177.60 (USD 2.60 over the target). `budget_usd` is unchanged.
- R11: still at risk; 4.94 kg against 5 kg (0.06 kg of margin, was 0.09 kg).
- On paper 12 of 17 are met (was 13); none is failed outright.

### Proposed, awaiting Amish

- The $2.60 overshoot of the value-engineering target: accept it as a control target, not a limit (recommended for the paper design), look for $2.60 of savings, or raise the target. Recorded as open decision 1 in CCK-DEC-001.
- Appearance deviations in the appearance model: guard drawn slotted and 1.0 mm (accepted 2026-10-02), 18650 cells shown, rubber feet drawn as plain cylinders.

### Pictures regenerated

General arrangement CCK-DWG-001 Rev P3; making sketches CCK-DWG-101 to 110 (101 to 110 re-issued, notes added to 103 and 105); concept media (`media/hero.png`, exploded, flow, blueprint, viewer); build plan overview, plate hole figure, joints 1 to 7 (joint 4 redrawn from behind to show the guard), steps 1 to 12 (new step 9), wiring.

### Appearance model and render scenes

`cad/src/product_model.py` now has six feet and six standoffs, plate slots with silicone seals, the end-flanged guard with two thumb screws, boards lifted 5 mm, finger guards, and the unit lifted onto its feet, all dimensions from `cad/src/model.py`. Scenes exported to `/home/claude/renders/cellcheck`: hero, exploded and detail (one .npz and .json each, plus `cellcheck__jobs.json`).

### Cross-repo actions

- SwapCell and PowerBox: send the second-life pack study (CCK-CAL-001 section 10: 13S4P of grade A laptop cells, about 334 Wh, 165 W, low-current storage variant) as a proposal.

### Documents changed

CCK-CAL-001 v0.6, CCK-REQ-001 v0.8, CCK-PRC-001 v0.8, CCK-DEC-001 v0.5, CCK-DDR-003 v0.5, CCK-BLD-001 v0.4, CCK-DWG-001 Rev P3, `bom/bom.csv`, `bom/bom-notes.md`, README. PDFs re-rendered.

### Recommended next step

Decide the cost overshoot, render the photoreal images on the Mac, then ask Amish before any TRL 4 work.

## 2026-10-02: photoreal renders redone on the constructable design

Rendered with Blender Cycles on Amish's Mac from the updated appearance model; captioned with `.kit/photo_caption.py`; `media/card.png` and `media/social-preview.png` regenerated with `.kit/cards.py`. Views: hero, exploded, detail. image_qc passes. Appearance deviations are those logged above as proposed, awaiting Amish.
