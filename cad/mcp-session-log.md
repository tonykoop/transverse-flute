# MCP Session Log

This log is intentionally present for the V5 provenance contract. No live MCP
tool sessions were run in this Round 30 lane, so no generated render, Adobe,
Blender, Illustrator, Photoshop, or image-gen artifact is claimed here.

| timestamp_utc | mcp_tool | session_id | artifact | parent_artifact | authority_role | notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-05-18T00:00:00Z | none | not-run-round30 | cad/slip_cast_transverse_flute_body.scad | data/fired-dimension-targets.csv | local-cad-starter | Existing OpenSCAD starter reconciled to the G4 first-pass target; not a measured or runtime-generated MCP artifact. |
| 2026-07-01T00:00:00Z | claude-code (Fable 5) | fable-v5-refresh-2026-07-01 | Slip-Cast-Transverse-Flute-Family.xlsx, data/hole-schedule.csv, data/fired-dimension-targets.csv | Slip-Cast-Transverse-Flute-Family.xlsx | packet_refresh (authority_result=fabrication, review_status=self_checked) | V5 refresh pass; tabular packet data (workbook + hole schedule + fired-dimension targets) reviewed against design table. No dimension changes made. Provenance rows added to satisfy V5 fabrication-artifact logging. |
| 2026-07-01T00:00:00Z | claude-code (Fable 5) + OpenSCAD CLI | fable-v5-refresh-2026-07-01 | cad/slip_cast_transverse_flute_body.scad | data/fired-dimension-targets.csv | cad_authoring (authority_result=pending_measurement, review_status=self_checked) | Existing parametric body-envelope master (kept, not rewritten). openscad render check: pass (openscad -o STL, exit 0). |
| 2026-07-01T00:00:00Z | claude-code (Fable 5) | fable-v5-refresh-2026-07-01 | transverse-flute-starter.wl | Slip-Cast-Transverse-Flute-Family.xlsx | analysis_source (authority_result=derived_preview, review_status=unreviewed) | Wolfram/physics starter; source-only (not executed). L2 evidence. |
