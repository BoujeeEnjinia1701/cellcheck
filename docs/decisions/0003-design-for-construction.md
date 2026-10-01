---
doc_id: CCK-DDR-003
title: CellCheck design for construction
project: CellCheck
doc_type: Design decision record
version: "0.2"
status: Draft
date: '2026-10-01'
author: Amish Chadha
license: CERN-OHL-S-2.0
revisions:
- version: "0.1"
  date: '2026-10-01'
  author: Amish Chadha
  change: Changes that make the concept physically buildable, with the reason for each; made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review
- version: "0.2"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target; cost wording only, no number changed
---

# 0003: Design for construction

- **Date:** 2026-10-01
- **Status:** draft. The changes in Tables 1 and 2 were made under Amish's 2026-09-30 instruction to make the design physically buildable; open for his review. The items in Table 3 would touch the safety case and are Proposed, awaiting Amish.

## Context

On 2026-09-30 Amish asked for every repo to have an illustrated prototype build plan and wrote: "If you are realising that the design cannot be built as per concept - fix the design assumptions to match and be physically feasible as you draw the illustrations." The CellCheck model of CCK-DDR-001 and CCK-DDR-002 showed what the grader does, and its parts did not overlap, but most of them had no fixing, two had no room for the parts that go in them, and three parts the electronics need were missing. Checking the model with build123d (contacts, overlaps and clearances between every pair of parts) found the problems in Table 1.

The changes keep what CellCheck does: eight channels at the same 40 mm pitch, the same cells, holders, guard size, heatsink, fans, modules, grading method, 12 V input and steel tray. The tray, its liner and the guard keep their materials and thicknesses, so the containment arrangement is unchanged. Every change is in `cad/src/model.py`, which now runs 129 constructability checks (`python cad/src/model.py --check`): parts that must touch do touch, and parts that must stay apart are apart by at least the stated clearance. All 129 pass.

## Decision

*Table 1. Changes made to the model, the BOM and the calculations.*

| # | Problem in the concept | Change made | Why this way |
| --- | --- | --- | --- |
| P1 | The base plate stood on four standoffs resting on the soft ceramic fibre liner, with nothing holding the standoffs or the plate to the tray. | Six rubber feet with M4 studs under the tray (new BOM line 19). Each stud passes up through a 4.5 mm hole in the tray floor into a 12 mm hex standoff standing on the bare steel through a 12 mm hole in the liner; the plate screws down onto the standoffs with six M4 screws. The tray now stands 8 mm off the bench. | One part does two jobs: the foot is also the fixing, so no screw head sits under the tray. The standoffs bear on steel, not on compressible fibre. Lifting the tray off the bench also keeps its hot floor off the bench surface. |
| P2 | The plate was 2 mm aluminium on four standoffs, two of whose screw heads sat under the display stand and the inlet, where they could not be reached. Adding fixings would have taken the mass past the 5 kg limit of R11. | The plate is 1.5 mm aluminium on six standoffs in three columns, 210 mm left, 45 mm left and 120 mm right of centre, 124 mm each side front to back; every screw is reachable from above once the plate is in the tray. | Six supports cut the longest unsupported span to 165 mm, so the thinner plate stays stiff; it saves 0.16 kg and keeps the plate top at the same height, so nothing above it moves. |
| P3 | The cell holders had no fixing, and the cell leads and thermistor leads had no way out from under the closed guard. | Two M3 screws from under the plate into each holder base. Two 16 x 5 mm slots per channel through the plate, edged with grommet strip: one just behind the holder, inside the guard, and one between the charger and the channel board. The leads run under the plate in the 9 mm space above the liner. | The guard stays closed on all four sides and the top, and the leads never cross its edge. |
| P4 | The guard was drawn as a frame of bars standing on the plate with no fixing, and it had to come off at every cell change. | A box folded from one 0.8 mm perforated steel blank, open at the bottom, with corner tabs riveted and an 18 mm flange folded outward at each end. Two M4 blind rivet nuts in the plate and two M4 knurled thumb screws hold the flanges; the guard lifts off after two thumb screws. | Sheet the builder can cut and fold by hand; nothing loose on the bench; no tool needed at a cell change. A rivet nut gives a lasting thread in 1.5 mm aluminium, which is too thin to tap. |
| P5 | The charger modules, channel boards, controller and watchdog board sat directly on the aluminium plate, where their solder joints would short to it, and the controller and watchdog board left only 3 mm beside the right-hand thumb screw. | Every board stands on two 5 mm nylon standoffs with M3 screws from under the plate. The controller and watchdog board move 10 mm to the right. | Insulation from the plate and room for fingers on the thumb screw. |
| P6 | The display stand was 60 mm wide and 55 mm tall, but a 2.8 in display module is about 86 x 50 mm. | A printed stand 88 mm wide with an upright 62 mm tall, at the front right corner of the plate in front of the guard's end flange; the three push buttons sit in 7 mm holes in its foot. | The bought module fits; the stand stays clear of the guard and of every plate screw. The stand's top, 77 mm above the bottom of the tray, is now the highest point; with the feet the unit is 85 mm tall, well inside R11's 120 mm. |
| P7 | The heatsink stood on the plate with no fixing, and the MOSFETs had no clamp to the spine. | Three M3 screws from under the plate into tapped holes in the spine's bottom edge. Each MOSFET is clamped to the spine by one M3 screw with an insulating pad and shoulder washer, into a tapped hole between two fins. | Standard TO-220 mounting; the spine is the only part thick enough to tap. |
| P8 | The fan shroud had no fixing, and its top lip at fin height could not be folded from the same sheet as its 60 mm back. | The shroud is a 1 mm aluminium back with two side flanges folded forward onto the ends of the spine, each held by two M3 screws into tapped holes. The fans screw to the back from the inside before the shroud is fitted. The top lip is dropped. | One folded part, fixed to the heatsink so the air path cannot shift. The calculation note already assumes only half of the fans' free air passes through the fins, so the heatsink result stands. |
| P9 | The thermistor clip was a block resting on top of the cell with nothing holding it. | A printed C-clip, 10 mm long, that springs over the cell and wraps 10 degrees past its sides, with a raised pad that holds the thermistor bead against the cell. One set of eight for 21700 cells and one for 18650. | A clip that holds itself; the bead touches the cell as R7 assumes. |
| P10 | The power inlet was a solid block with its DC jack facing the tray wall 23 mm away, too close for a plug. | An open-bottomed printed housing with the jack, fuse holder and rocker switch on its top face and two screw bosses; the adapter lead comes over the tray's right rim into the jack. | Room for the plug, and no new hole through the tray wall. |
| P11 | Three parts the electronics need had no place: a 5 V supply for the controller, display and channel boards (only 12 V comes in); a home for the op-amp of each load loop and for the series charge switch; and a reachable place for the 3 A channel fuses, which would otherwise have been under the plate. | A 12 V to 5 V buck converter (new BOM line 21) on standoffs in the right-hand bay. BOM line 7 becomes a channel board: the current monitor breakout on a small perfboard carrying the charge switch, the op-amp of the load loop and fuse clips for the 3 A channel fuse. | Parts that the single-fault analysis and the test sequence rely on now exist in the model and the BOM. The fuse can be checked and changed from above. |
| P12 | In the model each cell floated 0.5 mm above its holder groove and 1 mm short of each contact. | The cell rests in the groove and touches the force and sense contacts at both ends. | Matches how a spring holder holds a cell. |

*Table 2. Knock-on changes.*

| Item | Change | Reason |
| --- | --- | --- |
| Mass | 4.91 kg without the adapter (was 4.97 kg): feet, fixings, guard flanges and the converter add about 0.12 kg; the thinner plate takes off 0.16 kg. R11 stays at risk with 0.09 kg of margin. | CCK-CAL-001 v0.3 section 8 |
| Size | 460 x 300 x 85 mm (was 75 mm high): the display stand and the 8 mm feet set the height. | CCK-CAL-001 v0.3 section 8 |
| Cost | Lines 19 (rubber feet, $2.40), 20 (fixings, $4.00) and 21 (5 V converter, $2.00) added: $172.40 estimated, $2.60 under the $175 value-engineering target, so R12 stays within the target. Lines 1 to 5, 7 to 10, 12, 13 and 16 are respecified with the same prices. | CCK-CAL-001 v0.3 section 11 |
| Thermal | Unchanged: the heatsink, fans and fin airflow keep their size and place. | CCK-CAL-001 section 4 |
| Drawings | General arrangement CCK-DWG-001 Rev P2; making sketches CCK-DWG-101 to 110 added. | Follow the model |
| Documents | CCK-CAL-001 v0.3, CCK-PRC-001 v0.5, CCK-REQ-001 v0.5: mass, height and cost updated. No requirement changed status. | Follow the model |

*Table 3. Proposed, awaiting Amish.*

| # | Question | Options | Recommendation |
| --- | --- | --- | --- |
| A1 | How the guard is held down. It is part of the containment arrangement of R10, and it now lifts off after two thumb screws so that cells can be changed without tools. | (a) two knurled thumb screws, as modelled; (b) two over-centre toggle latches; (c) a hinge along the back edge with one latch at the front. | (a) for the first prototype, and decide for later units after the containment test at TRL 4. A hinge would swing onto the charger row. |
| A2 | The wire slots behind each holder open the space under the guard to the space under the plate. Both are inside the tray, so the tray still contains a venting cell, but hot gas could reach the underside of the electronics. | (a) leave the slots open with grommet strip, as modelled; (b) fill each slot round its leads with high-temperature silicone after wiring. | (b): no new part, about a dollar of sealant, and the guard space is closed again. |

## Consequences

- `design_state: constructable` in `project.yaml`. The build plan CCK-BLD-001 shows every component and step in pictures generated from the model (`cad/src/build_plan_media.py`).
- Requirement status is unchanged: none not met, three at risk (R5, R6, R11), 13 met on paper, R10 not verifiable at TRL 3 (CCK-CAL-001 v0.3).
- The appearance model `cad/src/product_model.py`, the photoreal renders (`media/render-*.png`), `media/card.png` and `media/social-preview.png` still show the concept guard, display, inlet and fixings and no feet; they need updating on Amish's Mac, where Blender is.
- The tray, modules, display and heatsink are chosen at TRL 4; the items in the "to confirm when parts are bought" table of the design decisions register CCK-DEC-001 must be checked then.
