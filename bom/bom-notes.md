# BOM notes

- Prices are indicative US dollar prices for single units from general electronics distributors, online marketplaces and hardware stores in 2026. They are estimates, not quotes.
- Line numbers 1 to 15 and 18 match the callouts in `media/exploded.png`, the parts in `cad/src/model.py` and the general arrangement CCK-DWG-001. Lines 16 and 17 are not modelled.
- Total at quantity one: **$164.00** (checked by `docs/04-calcs/sizing.py`, CCK-CAL-001 section 11). Cells are not included.
- Against the `project.yaml` budget of $175 the BOM is $11.00 under, so R12 is met. Amish raised the budget from $160 to $175 on 2026-09-25 (CCK-DDR-001 item 4, CCK-DDR-002); against $160 the BOM was $4.00 over.
- Line 18 (hardware watchdog and undervoltage comparators, $5.00) is new at TRL 3 and closes R9 on paper (CCK-DDR-001 item 3). Line 16 includes the 3 A per-cell fuses that the single-fault analysis relies on.
- Module choices (charger, current monitor, controller) were decided by Amish on 2026-09-25 (CCK-DDR-001 item 6). Purchasing is TRL 4 work and on hold.
- Buy only a certified mains adapter (line 14). CellCheck has no mains wiring of its own.
