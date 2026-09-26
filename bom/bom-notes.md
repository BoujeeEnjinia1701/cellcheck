# BOM notes

- Prices are indicative US dollar prices for single units from general electronics distributors, online marketplaces and hardware stores in 2026. They are estimates, not quotes.
- Line numbers 1 to 15 and 18 match the callouts in `media/exploded.png`, the parts in `cad/src/model.py` and the general arrangement CCK-DWG-001. Lines 16 and 17 are not modelled.
- Total at quantity one: **$164.00** (checked by `docs/04-calcs/sizing.py`, CCK-CAL-001 section 11). Cells are not included.
- Against the `project.yaml` budget of $160 the BOM is $4.00 over, so R12 is not met. Against the recommended $175 (Proposed, awaiting Amish, CCK-DDR-001 item 4) it is $11.00 under. `budget_usd` has not been changed.
- Line 18 (hardware watchdog and undervoltage comparators, $5.00) is new at TRL 3 and closes R9 on paper (CCK-DDR-001 item 3). Line 16 includes the 3 A per-cell fuses that the single-fault analysis relies on.
- Module choices (charger, current monitor, controller) are adopted for TRL 3 under Amish's 2026-09-25 instruction, open for his review (CCK-DDR-001 item 6).
- Buy only a certified mains adapter (line 14). CellCheck has no mains wiring of its own.
