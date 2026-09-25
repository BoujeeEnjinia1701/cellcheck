# CellCheck

![TRL 2](https://img.shields.io/badge/TRL-2%20of%209-0F766E) ![Hardware: CERN-OHL-S-2.0](https://img.shields.io/badge/hardware-CERN--OHL--S--2.0-111827) ![Software: MIT](https://img.shields.io/badge/software-MIT-111827)

**Area:** Circular Materials · **TRL:** 2 of 9 (concept formulated) · **Prototype budget:** about $160 USD · **Difficulty:** 3 of 5

A second-life battery cell grader: it measures capacity, internal resistance and self-discharge of salvaged lithium cells and sorts them into matched groups for rebuilt packs such as SwapCell.

## Concept rationale

Grading turns waste cells into a known resource and is the missing step between battery collection and safe reuse.

## Burning platform

Growing volumes of laptop, e-bike and power tool batteries are discarded with most of their cells still usable.

## Where it could be used

### By industry

| Industry | Use |
| --- | --- |
| _To be developed_ | |

### By country or region

| Country or region | Why it matters there |
| --- | --- |
| _To be developed_ | |

## What sparked the idea

It came out of a September 2026 review of Design Molecule's applied research areas against the open projects already in the lab. CellCheck was already planned as the companion to SwapCell and ReflowEconomy.

## Problem

Salvaged lithium cells are cheap but unknown; building packs from untested cells causes early failure and fires.

## Concept

A second-life battery cell grader: it measures capacity, internal resistance and self-discharge of salvaged lithium cells and sorts them into matched groups for rebuilt packs such as SwapCell.

Full design precis: [docs/02-concept.md](docs/02-concept.md)

## Key components

- Multi-channel charge and discharge board
- Internal resistance measurement circuit
- Cell holders for 18650 and 21700
- Temperature sensing per channel
- Controller and grading software
- Fire-resistant tray

The working bill of materials is in [bom/bom.csv](bom/bom.csv).

## Safety

> Lithium cells can overheat, vent and burn. Use protected cells or LiFePO4, fuse every pack, charge only within the cell maker's limits and never leave a first build charging unattended. Grade salvaged cells on a non-flammable surface and isolate any cell that heats or swells.

## Repository layout

| Folder | Contents |
| --- | --- |
| `docs/` | Problem, concept, requirements, calculations and design decisions |
| `cad/src/` | build123d Python source, the source of truth for all geometry |
| `cad/step/`, `cad/stl/` | Exported models for FreeCAD, other CAD tools and printing |
| `cad/drawings/` | 2D sketches and dimensioned drawings |
| `bom/` | Bill of materials |
| `electronics/` | KiCad schematics and PCB layouts |
| `firmware/` | Microcontroller code |
| `media/` | Renders, perspectives and photos |
| `build-log/` | Dated prototyping notes |

## Documentation

Controlled documents follow the portfolio [documentation standard](.kit/STANDARDS.md). Each carries a document ID (CCK-PRC-001 for the precis), a version and a revision history. Branded PDFs are built with `python .kit/render.py` and attached to GitHub Releases when a document is tagged, for example `CCK-PRC-001/v1.0`.

## Licenses

- **Hardware** (CAD, drawings, BOM, electronics): [CERN-OHL-S v2](LICENSE)
- **Software** (firmware, scripts, notebooks): [MIT](LICENSE-SOFTWARE)

A project of the [Design Molecule](https://designmolecule.com) lab. Extending strong areas set.
