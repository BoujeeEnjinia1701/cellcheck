---
doc_id: CCK-PRC-001
title: CellCheck design precis
project: CellCheck
doc_type: Design precis
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
  change: Populate to TRL 2 (architecture, grading method, first-order numbers, safety, media)
---

# CellCheck design precis

## Summary

CellCheck is an eight-channel bench grader for salvaged 18650 and 21700 lithium-ion cells. Each channel charges one cell, measures its DC internal resistance with a two-step current pulse, discharges it at a constant 1 A to measure capacity, and recharges it for a 14-day self-discharge rest. Software then sorts the passing cells into grades and builds matched groups for a pack of a chosen series and parallel count, with a record for every cell. First-order numbers suggest about 6.5 h per cell, about 12 cells per attended 10 h day and about $159 in parts, just inside the $160 budget. Every figure below is an estimate for concept review and will be checked at TRL 3.

![CellCheck on a bench with its rest rack and a salvaged laptop pack](../media/hero.png)

*Figure 1. Concept massing model on a bench: steel tray with eight cell channels (center), rest rack for the self-discharge check (left), 12 V adapter (right) and a salvaged laptop pack (front) for scale.*

## How it works

1. **Intake (by hand).** The operator removes cells from a pack, rejects any with dents, torn wraps, leaks or corrosion, measures open-circuit voltage and rejects cells below 2.0 V. Each cell gets an ID label. Cells below 2.0 V are not revived: deep discharge can grow copper dendrites that cause internal shorts when the cell is charged again.
2. **Charge.** The cell goes into a channel. A 1 A CC-CV charger module brings it to 4.20 V and stops at 0.1 A. A thermistor clipped to the cell stops the channel if the cell passes 45 °C or rises more than 8 K above the bench.
3. **Rest and resistance.** After a 30 min rest the channel runs a DC resistance test in the pattern of IEC 61960: 0.5 A for 10 s, then 2.0 A for 1 s, with resistance taken as the change in voltage over the change in current ([test pattern summarized by Arbin Instruments](https://www.arbin.com/how-to-perform-internal-resistance-measurement-accroding-to-iec-61960-with-arbin.html)). IEC 61960 uses 0.2C and 1C; CellCheck uses fixed currents so results are comparable within a batch, not with data sheet values.
4. **Capacity.** A linear constant-current load discharges the cell at 1.0 A to 2.80 V while a current monitor integrates ampere-hours and watt-hours. Cell temperature is logged throughout; a cell that heats abnormally is flagged.
5. **Recharge for rest.** The charger brings the cell back to 4.10 V. The operator moves it to the printed rest rack, which holds 48 cells.
6. **Self-discharge check.** After 14 days the operator puts the cell back into any channel for a 10 s open-circuit reading. A drop of more than 50 mV marks the cell as rejected.
7. **Grade and match.** Software assigns a grade from capacity, resistance, heating and self-discharge (Table 2), then builds groups for the pack the user wants (for example 4S6P): cells of one grade are distributed with a serpentine sort so that each parallel group's total capacity is within ±1 % of the mean. Serpentine sorting of retired 18650 cells has been studied as a grouping method ([Xi et al., Batteries, 2026](https://www.mdpi.com/2313-0105/12/9/368)), and clustering by measured capacity and resistance produced a markedly better second-life pack than random selection in a recent study ([Olivero-Ortiz et al., PLOS One, 2026](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0353394)).
8. **Record.** Every cell gets a CSV row: ID, source pack, cell model if known, arrival voltage, capacity, resistance, temperature rise, self-discharge, grade, group and dates. Rejected cells are logged too and go to a battery collection point for recycling.

![Material flow per 100 salvaged cells](../media/flow.png)

*Figure 2. Material flow per 100 cells taken from salvaged packs (all values are estimates). The first loss draws on the 4.3 % of cells with surface damage found by [Salinas et al. (2019)](https://www.sciencedirect.com/science/article/abs/pii/S2352152X18308399) plus an assumed 5 % below 2.0 V; the other losses are assumptions to be checked with real cells.*

## Main components

Table 1. Main components, numbered as in the exploded view (Figure 3) and `bom/bom.csv`.

| # | Component | Proposed choice | Notes |
| --- | --- | --- | --- |
| 1 | Steel tray with liner | 460 x 300 x 45 mm steel tray, ceramic fibre sheet on the floor | Contains ejecta from a venting cell; the whole unit sits in it |
| 2 | Base plate | Aluminium or FR4 carrier on four standoffs | Carries all modules; standoffs keep it off the tray |
| 3 | Cell holders | Eight holders for 18650 and 21700 with spring contacts, separate force and sense contacts at each end (four-wire) | Kelvin sensing keeps contact resistance out of the reading |
| 4 | Temperature sensing | 10 kΩ NTC thermistor clipped to each cell | Read by the controller's ADC |
| 5 | Cell guard | Perforated steel cover over the cells | Stops loose ejecta; cells stay visible |
| 6 | Chargers | 1 A CC-CV buck charger module per channel, 4.20 V, fed from 12 V (TP5100 class) | Module sets its own voltage limit, independent of firmware |
| 7 | Sense and switch boards | INA226-class current and voltage monitor with a 25 mΩ shunt, plus a charger enable switch, per channel | 16-bit readings over I2C at addresses 0x40 to 0x47 |
| 8 | Load MOSFETs | Logic-level MOSFET in TO-220 with an op-amp loop per channel, constant current 0.5 to 2.0 A | Linear load; energy ends up as heat |
| 9 | Heatsink | Finned aluminium bar, about 320 mm long | All eight MOSFETs on one bar |
| 10 | Fans | Two 60 mm 12 V fans | Temperature-controlled |
| 11 | Controller | ESP32-S3 class board | Runs the test sequence, logs to microSD, serves a local web page |
| 12 | Display and buttons | 2.8 in display with three buttons | Channel status without a laptop |
| 13 | Power inlet | DC jack, 6.3 A main fuse, switch | Only 12 V DC enters the unit |
| 14 | Power supply | Certified 12 V 5 A mains adapter | No mains wiring inside CellCheck |
| 15 | Rest rack | 3D-printed rack for 48 cells, numbered slots | Holds cells for the 14-day check |

![Exploded view with BOM numbers](../media/exploded.png)

*Figure 3. Exploded view. Numbers match Table 1 and `bom/bom.csv`. Grey cells are not supplied.*

## Grading rules

Table 2. Proposed grades (thresholds are estimates for review; all live in a plain configuration file). Proposed, awaiting Amish.

| Grade | Capacity, share of rated | DC resistance (18650 default) | Other conditions | Suggested use |
| --- | --- | --- | --- | --- |
| A | 80 % or more | 60 mΩ or less | Temperature rise 8 K or less at 1 A; self-discharge 50 mV or less in 14 days | Storage packs at 0.5C or less |
| B | 65 % or more | 100 mΩ or less | As A | Storage and lighting packs at 0.3C or less |
| C | 50 % or more | 150 mΩ or less | As A | Low-drain uses only: lights, small sensor nodes |
| Reject | Below 50 % | Above 150 mΩ | Or any failed condition, arrival voltage below 2.0 V, or visible damage | Battery recycling |

Rated capacity comes from the cell model printed on the wrap, looked up in a cell table; if the model is unknown, the grade uses measured capacity only and the record says so. The 60 mΩ default for grade A is an assumption for a typical laptop 18650 in good health; it will be set per cell model at TRL 3.

## First-order numbers

All values are estimates for concept review and will be checked at TRL 3. Assumptions: a typical salvaged 18650 holds about 1.8 Ah as found (close to the 1.62 Ah mean reported by Olivero-Ortiz et al., 2026), arrives at about 30 % charge, has a mean voltage of about 3.65 V on discharge and about 3.9 V on charge; charger modules are about 85 % efficient and the adapter about 88 %; controller and fans draw about 3 W.

Table 3. First-order numbers.

| Quantity | Estimate | Basis | Requirement |
| --- | --- | --- | --- |
| Time per cell | about 6.5 h (6 to 8 h) | Charge 1.6 h, rest 0.5 h, discharge 1.8 h, rest 0.25 h, recharge to 4.10 V 1.8 h, handling about 0.5 h; a 2.5 Ah cell takes about 8 h | |
| Throughput | about 12 cells per attended 10 h day; about 28 per 24 h if run overnight | 8 channels, each started as soon as it is free | R5 met, thin margin |
| Cells for one 4S6P pack of grade A or B | about 36 candidates, about 3 attended days plus the 14-day rest | 24 cells at about 66 % yield (Figure 2) | |
| Capacity accuracy | about ±1 % after a one-time calibration, about ±2 % without | 25 mΩ shunt at 0.5 % tolerance, monitor gain error about 0.1 % | R2 met on estimate |
| Voltage accuracy | about ±10 mV worst case before calibration, better after | Typical current-monitor data sheet figures | R3 at risk until checked |
| Resistance resolution | about 0.8 mΩ per count; about ±3 mΩ repeatability expected | 1.25 mV voltage step over a 1.5 A current step, 16 readings averaged, four-wire contacts | R4 met on estimate, unverified |
| Heat at full discharge load | about 29 W average, about 34 W peak | 8 cells x 1.0 A x 3.65 V (4.2 V at start) | |
| Heatsink needed | 1.1 K/W or better to keep MOSFET cases at 75 °C or less in a 35 °C room | 34 W, about 2 K case-to-sink | R8 met on estimate with fans (about 0.5 to 0.8 K/W expected) |
| Adapter load, all channels charging | about 43 W of 60 W (about 71 %) | 8 x 4.2 V x 1 A / 0.85 + 3 W | |
| Energy per cell from the mains | about 18 Wh | (5.0 Wh first charge + 6.2 Wh recharge) / 0.85 + 2.4 Wh overhead, then / 0.88 | Cost well under $0.01 per cell at $0.15/kWh |
| Cell heating at 1 A | about 0.1 W per cell, a few kelvin | 1 A squared times about 0.1 Ω | An 8 K rise flags a fault |
| Size and mass | 460 x 300 x 90 mm with guard; about 3.5 kg without adapter | Tray 2.0 kg, heatsink 0.6 kg, plate and modules 0.9 kg | R11 met |
| Parts cost | about $159 | Indicative prices, see `bom/bom.csv` | R12 met, about $1 margin |

## Key design choices

- **Linear load, not energy recovery.** Discharge energy is burned in MOSFETs on one heatsink. Feeding it back to the 12 V bus or to a charging cell would save about 6.6 Wh per cell but adds a bidirectional converter per channel and costs more than the budget allows. Proposed, awaiting Amish; regenerative discharge is a possible later variant.
- **One cell per channel, eight channels.** Eight channels keep heat near 30 W and cost within budget while giving about 12 cells a day. A 16-channel version is an option for a busy repair shop. Recommendation: eight channels. Proposed, awaiting Amish.
- **Four-wire DC resistance, not 1 kHz AC impedance.** DC pulses need no signal generator and reflect how the cell behaves under load; AC readings from handheld meters are lower and not comparable. Recommendation: DC. Proposed, awaiting Amish.
- **Passive rest rack for self-discharge.** Holding cells in channels for 14 days would stall the grader, so cells rest in a rack and come back for a 10 s reading. Recommendation: 14 days (7 days is an option that catches only the worst cells). Proposed, awaiting Amish.
- **12 V DC input only.** A certified adapter keeps mains out of the unit, so builders never wire mains.
- **Local-first data.** Records stay on the microSD card and the local web page; no cloud account is needed. The CSV fields could map to ReflowEconomy's material passport at TRL 3. Proposed, awaiting Amish.
- **Lithium-ion first, LFP later.** The first release covers LCO, NMC and NCA cells at 4.20 V. LFP cells need a 3.65 V charger and a 2.5 V discharge limit; an LFP profile is an open question.

## Relation to other lab projects

- **SwapCell.** The pitch names SwapCell as a user of rebuilt packs. SwapCell's current precis specifies new, matched 5 Ah 21700 cells carrying 10 A continuous each in a 13S2P pack. Typical laptop cells are rated for far less current, so graded laptop cells cannot meet the SwapCell reference pack as specified. A second-life SwapCell variant (for example a low-current storage pack for PowerBox, or a pack of graded power tool cells) needs a decision by Amish and agreement with the SwapCell project. Proposed, awaiting Amish.
- **CellGuard.** Packs rebuilt from graded LFP cells would use CellGuard; lithium-ion packs depend on CellGuard's proposed NMC profile, which is itself awaiting Amish.
- **ReflowEconomy.** CellCheck is the grading step for the battery stream in ReflowEconomy's micro-factory, where cells that cannot be reused are exported for industrial recycling.

## Safety

> **Safety:** Salvaged lithium-ion cells can have hidden damage and can overheat, vent flammable and toxic gas, and burn. Work on a non-flammable surface, with a smoke alarm and a Class D or large dry-powder extinguisher or a sand bucket within reach, and never leave the grader running unattended until Amish has decided whether and how overnight operation is allowed.

- **Pack disassembly.** Removing spot-welded nickel strip can short cells or tear wraps. Use insulated tools, cut one strip at a time, wear eye protection and gloves, and tape exposed terminals.
- **Damaged and deeply discharged cells.** Reject cells with any visible damage and cells below 2.0 V. Do not try to revive them.
- **Charging.** Each charger module limits voltage to 4.20 V by itself; the firmware adds temperature and time limits. A cell that passes 45 °C or rises 8 K above the bench is disconnected and flagged; the operator moves it to a metal container of sand once it is cool.
- **Single faults.** A load MOSFET that fails short would drain its cell far below 2.0 V; the cell must then be rejected. A hardware watchdog that removes all load gate drive when the controller stops is proposed (R9).
- **Heat.** The heatsink can reach about 70 °C; the guard and layout keep it away from the cells, and the fans run whenever a load is on.
- **Containment.** The steel tray, ceramic fibre liner and steel guard are meant to hold ejecta from one venting cell. This has not been checked and must not be relied on.
- **Transport and storage.** Store graded cells at about 3.7 V in a non-flammable container with terminals covered. Rejected cells go to a battery collection point, never to household waste.
- **Scope.** CellCheck is a research and prototype tool. Its grades do not certify any cell or pack as safe.

## Open questions

- [ ] May graded cells ever go into SwapCell packs, and if so, which cell sources and current limits? Proposed, awaiting Amish.
- [ ] Can the grader run unattended overnight, and with what precautions (for example a fire-rated cabinet and a remote alarm)? Proposed, awaiting Amish.
- [ ] Grading thresholds, rest period and matching tolerance (Table 2 and item 7). Proposed, awaiting Amish.
- [ ] Should an LFP profile be in the first release? Proposed, awaiting Amish.
- [ ] Which partner should supply cells for first trials: a repair café, an e-bike repair shop or a collection point? Proposed, awaiting Amish.
- [ ] How does the grading record map onto ReflowEconomy's material passport? To be studied at TRL 3.
