---
doc_id: CCK-PRB-001
title: CellCheck problem statement
project: CellCheck
doc_type: Problem statement
version: "0.6"
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
  change: Populate to TRL 2 (problem, prior work, users, context, constraints)
- version: "0.3"
  date: '2026-09-25'
  author: Amish Chadha
  change: Apply CCK-DDR-001 (second-life SwapCell variant, attended operation, budget note); open questions updated
- version: "0.4"
  date: '2026-09-25'
  author: Amish Chadha
  change: Recommendations accepted by Amish (DDR-002)
- version: "0.5"
  date: '2026-10-01'
  author: Amish Chadha
  change: Budget treated as a value-engineering target; cost wording only, no number changed
- version: "0.6"
  date: '2026-10-02'
  author: Amish Chadha
  change: First trial partner decided on 2026-10-02 (CCK-DEC-001, item 3)
---

# CellCheck problem statement

Salvaged lithium-ion cells from laptop, power tool and e-bike packs are cheap and often still usable, but each one is an unknown. Building a pack from untested cells mixes weak, high-resistance and self-discharging cells with good ones, which shortens pack life and raises the risk of a cell overheating. Small repairers and makers need a low-cost, open way to measure every cell and group the good ones into matched sets.

## The problem

Most cells in a discarded pack are not dead. A pack usually leaves service because one parallel group has faded, the pack's electronics have locked out, or the device it powered was retired. Two studies show the scale of the usable remainder:

- IBM Research India measured 32 discarded ThinkPad packs rated at 85 Wh and found a median residual capacity of 73 % of design capacity (mean 64 %), then built lights from the cells that still held a good voltage ([Chandan et al., UrJar, ACM DEV 2014](https://www.dgp.toronto.edu/~mjain/UrJar-DEV-2014.pdf)).
- A German study recovered 1,034 cells from 152 notebook packs and judged about 95.7 % of them free of damage and suitable for further testing, with an average of about 5.3 Wh per cell, roughly half the capacity of a new 18650 cell at the time ([Salinas et al., Journal of Energy Storage, 2019](https://www.sciencedirect.com/science/article/abs/pii/S2352152X18308399)).

The catch is spread. A 2026 study of 92 cells recovered from laptop packs in Colombia found capacities from 0.04 to 2.50 Ah (mean 1.62 Ah, standard deviation 0.53 Ah) and internal resistance up to 418 mΩ, and showed that clustering cells by measured capacity and resistance built a markedly better 24-cell pack than random selection ([Olivero-Ortiz et al., PLOS One, 2026](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0353394)). In a series string the weakest cell sets the capacity of the whole pack and is driven hardest at the end of each discharge, so an unmatched pack ages fast and puts its weakest cell under the most stress.

Meanwhile, the default path for these batteries is poor. The world generated 62 million tonnes of e-waste in 2022 and only 22.3 % was documented as collected and recycled; in Africa formal recycling was below 1 % ([UNITAR, Global E-waste Monitor 2024](https://unitar.org/about/news-stories/press/global-e-waste-monitor-2024-electronic-waste-rising-five-times-faster-documented-e-waste-recycling)). Lithium-ion batteries in the waste stream also start fires: the US EPA identified 245 fires at 64 waste facilities from 2013 to 2020 that were caused, or likely caused, by lithium-ion batteries ([US EPA, 2021](https://www.epa.gov/system/files/documents/2021-08/lithium-ion-battery-report-update-7.01_508.pdf)), and UK fire and waste bodies counted more than 1,200 battery fires in bin lorries and waste sites in the year to May 2024, up from about 700 in 2022 ([National Fire Chiefs Council and Material Focus, May 2024](https://nfcc.org.uk/over-1200-battery-fires-in-bin-lorries-and-waste-sites-across-the-uk-in-last-year/)).

What a cell rebuilder can use today falls into three groups:

1. **Single-cell hobby testers.** Open designs such as the [Ultimate Battery Tester](https://github.com/ArminJo/Ultimate-Battery-Tester) (Arduino, capacity and ESR) and the ESP32-based [DIY Smart Multipurpose Battery Tester](https://github.com/opengreenenergy/DIY-Smart-Multipurpose-Battery-Tester) (charge, discharge, capacity and internal resistance) test one or two cells at a time. They measure well but are too slow to sort the dozens of cells a pack needs.
2. **Closed multi-slot chargers and analyzers.** Four-slot consumer charger-analyzers report capacity and a resistance figure, but their methods, accuracy and data export are undocumented, and they do not track self-discharge or produce matched groups.
3. **Laboratory cyclers.** Multi-channel cyclers measure everything to standard methods, such as the two-pulse DC resistance test in IEC 61960 ([summary by Arbin Instruments](https://www.arbin.com/how-to-perform-internal-resistance-measurement-accroding-to-iec-61960-with-arbin.html)), but cost far more than a repair shop or makerspace can spend.

No open, garage-buildable tool covers the whole job: charge, measure capacity, measure resistance with four-wire contacts, record self-discharge after a rest, and turn the results into matched groups with a record for every cell.

## Users and context

| User | Need | Context |
| --- | --- | --- |
| Lab projects | A trusted source of graded cells and a record for each one | Lights and small DC storage packs; a second-life, low-current SwapCell variant for PowerBox (CCK-DDR-001 item 1, decided by Amish, 2026-09-25; needs the SwapCell project's agreement) |
| Repair shops and pack rebuilders | Sort cells from dead packs quickly, reject bad ones, build matched groups | E-bike, laptop and power tool repair; informal repair markets |
| Makerspaces, repair cafés and schools | A safe, documented way to reuse cells and teach battery basics | Supervised benches with basic fire precautions |
| Off-grid energy projects | Low-cost cells for lights, small storage and sensor nodes | Solar home systems, community storage pilots |
| Recyclers and collection points | Separate reusable cells from those that should go to recycling, with a record | Collection and pre-processing sites |

Operating context assumed for the concept: cylindrical 18650 and 21700 lithium-ion cells (LCO, NMC or NCA) and optionally LFP cells of the same sizes, one cell per channel, indoors on a bench at 15 to 35 °C (59 to 95 °F), powered from a certified 12 V DC adapter, with a person present while cells are charging or discharging. Only the self-discharge rest, with no current flowing, may run unattended (CCK-DDR-001 item 2).

## Constraints

- Garage-buildable prototype with a value-engineering target of about $175 USD in parts (`project.yaml`, a hypothetical control target, not a limit), excluding cells. The target was raised from $160 to cover single-fault protection (CCK-DDR-001 item 4, decided by Amish, 2026-09-25).
- Off-the-shelf modules and through-hole or large surface-mount parts only; no custom silicon, no fine-pitch assembly.
- Extra-low voltage only: a certified mains adapter supplies 12 V DC, and nothing inside the unit exceeds 13 V.
- Open hardware (CERN-OHL-S-2.0) and open software (MIT); grading thresholds and results in plain, readable files.
- Research, educational and prototype use. CellCheck is not a certified cell tester, and its grades do not certify a cell or pack as safe.

## Out of scope

- Pack disassembly tools (spot-weld removal and wrapping), covered only as a safety note.
- Pouch, prismatic and button cells; cells larger than 21700.
- Cell recovery by charging deeply discharged cells (below 2.0 V); these are rejected, not revived.
- Building or protecting packs; that is the job of the pack design and its BMS (for example CellGuard for LFP packs).
- Certification testing and any claim that a graded cell meets a safety standard.

## Open questions

- Graded cells in SwapCell packs: CCK-DDR-001 item 1 keeps SwapCell in the pitch and plans a second-life variant. The TRL 3 study (CCK-CAL-001 section 10) finds only a low-current storage pack for PowerBox feasible. Decided by Amish, 2026-09-25: go with recommendation; it needs the SwapCell project's agreement.
- Which partner should supply cells for first trials? Decided by Amish, 2026-10-02 (CCK-DEC-001, item 3): the first candidate to approach, not yet agreed, is a local Repair Café group that already passes laptop batteries to an e-waste or battery collection point, with that collection point as the source of trial cells.
- Unattended operation: charge and discharge attended only, the rest stage may be left (CCK-DDR-001 item 2). Decided by Amish, 2026-09-25: go with recommendation.

> **Safety:** Salvaged lithium-ion cells can hide damage and can overheat, vent and burn during charge or discharge. Any work on them needs a non-flammable surface, a smoke alarm, an extinguisher or sand bucket within reach and a person present while current flows.
