# BOM notes

- Prices are indicative US dollar prices for single units from general electronics distributors, online marketplaces and hardware stores in 2026. They are estimates, not quotes.
- Line numbers 1 to 15, 18 and 21 match the callouts in `media/exploded.png`, the parts in `cad/src/model.py` and the general arrangement CCK-DWG-001. Line 19 (rubber feet) is drawn with the tray and line 20 (fixings) with the parts it holds. Lines 16 and 17 are not modelled.
- Total at quantity one: **$172.40** (checked by `docs/04-calcs/sizing.py`, CCK-CAL-001 section 11). Cells are not included.
- Against the `project.yaml` value-engineering target of $175 (a hypothetical control target, not a limit) the estimated cost is $2.60 under, so R12 is within the target. Amish raised the target from $160 to $175 on 2026-09-25 (CCK-DDR-001 item 4, CCK-DDR-002); against $160 the BOM was $4.00 over.
- Line 18 (hardware watchdog and undervoltage comparators, $5.00) is new at TRL 3 and closes R9 on paper (CCK-DDR-001 item 3). Line 16 includes the 3 A per-cell fuses that the single-fault analysis relies on.
- Module choices (charger, current monitor, controller) were decided by Amish on 2026-09-25 (CCK-DDR-001 item 6). Purchasing is TRL 4 work and on hold.
- Buy only a certified mains adapter (line 14). CellCheck has no mains wiring of its own.
- Lines 19 (rubber feet with M4 studs), 20 (fixings) and 21 (12 V to 5 V converter) and the respecified lines 1 to 5, 7 to 10, 12, 13 and 16 come from the design for construction (CCK-DDR-003, 2026-10-01); the making sketches are CCK-DWG-101 to 110 and the build plan is CCK-BLD-001.
- Decided by Amish on 2026-10-02 (CCK-DEC-001): fan finger guards go into line 10 with an estimated price (item 9); high-temperature silicone for sealing the wire slots goes into line 16 (item 2); the matched-group bins stay out of the BOM until TRL 4 purchasing (item 8); the guard stays round-hole perforated 0.8 mm steel (item 10); the tray stays 1.5 mm steel (item 5). The line 10 and 16 changes and their prices are a follow-up and are not yet in the $172.40 total.
