#!/usr/bin/env python3
"""Generate the slip-cast transverse flute family build packet.

The packet is intentionally data-backed and repeatable: the same calculated
dimensions drive CSVs, drawings, and the lightweight XLSX workbook.
"""

from __future__ import annotations

import csv
import math
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-05-02"
SPEED_SOUND_IN_S = 13552.0
A4_HZ = 440.0
SHRINK_X = 0.12
SHRINK_Y = 0.12
SHRINK_Z = 0.12

NOTE_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
MAJOR_INTERVALS = [2, 4, 5, 7, 9, 11]
HOLE_RATIOS = [0.34, 0.36, 0.38, 0.40, 0.43, 0.46]

FAMILY = [
    {
        "id": "SCF-D4-01",
        "variant": "Low D reference",
        "midi": 62,
        "bore": 0.748,
        "wall": 0.140,
        "body": "Cone 6 stoneware",
        "profile": "cylindrical baseline",
    },
    {
        "id": "SCF-F4-01",
        "variant": "F middle",
        "midi": 65,
        "bore": 0.669,
        "wall": 0.135,
        "body": "Cone 6 stoneware",
        "profile": "cylindrical baseline",
    },
    {
        "id": "SCF-G4-01",
        "variant": "G middle",
        "midi": 67,
        "bore": 0.669,
        "wall": 0.130,
        "body": "Cone 6 stoneware",
        "profile": "cylindrical baseline",
    },
    {
        "id": "SCF-A4-01",
        "variant": "A small alto",
        "midi": 69,
        "bore": 0.591,
        "wall": 0.125,
        "body": "Cone 6 stoneware",
        "profile": "cylindrical baseline",
    },
    {
        "id": "SCF-C5-01",
        "variant": "C soprano",
        "midi": 72,
        "bore": 0.512,
        "wall": 0.115,
        "body": "Cone 6 stoneware",
        "profile": "cylindrical baseline",
    },
]


def note_name(midi: int) -> str:
    return f"{NOTE_NAMES[midi % 12]}{midi // 12 - 1}"


def freq(midi: int) -> float:
    return A4_HZ * 2 ** ((midi - 69) / 12)


def r(value: float, digits: int = 3) -> float:
    return round(value, digits)


def calc_family() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in FAMILY:
        midi = int(item["midi"])
        f0 = freq(midi)
        bore = float(item["bore"])
        wall = float(item["wall"])
        od = bore + 2 * wall
        acoustic = SPEED_SOUND_IN_S / (2 * f0)
        end_corr = 0.6 * bore
        sounding = acoustic - end_corr
        head_margin = 1.5 * bore
        foot_trim = 0.50
        pretrim = sounding + head_margin + foot_trim
        emb_x = 0.63 * bore
        emb_y = 0.52 * bore
        rows.append(
            {
                **item,
                "key": note_name(midi),
                "frequency": f0,
                "od": od,
                "acoustic": acoustic,
                "end_corr": end_corr,
                "sounding": sounding,
                "head_margin": head_margin,
                "foot_trim": foot_trim,
                "pretrim": pretrim,
                "emb_x": emb_x,
                "emb_y": emb_y,
            }
        )
    return rows


def calc_holes(family_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for inst in family_rows:
        midi0 = int(inst["midi"])
        f0 = float(inst["frequency"])
        acoustic = float(inst["acoustic"])
        sounding = float(inst["sounding"])
        head_margin = float(inst["head_margin"])
        bore = float(inst["bore"])
        for idx, interval in enumerate(MAJOR_INTERVALS, start=1):
            hmidi = midi0 + interval
            hf = freq(hmidi)
            dist_foot = acoustic * f0 / hf
            dist_head = head_margin + max(0, sounding - dist_foot)
            fired_dia = bore * HOLE_RATIOS[idx - 1]
            leather_cut = fired_dia / (1 - SHRINK_Y) * 0.85
            rows.append(
                {
                    "instrument_id": inst["id"],
                    "key": inst["key"],
                    "hole": idx,
                    "interval": interval,
                    "note": note_name(hmidi),
                    "frequency": hf,
                    "fired_distance_from_foot": dist_foot,
                    "fired_distance_from_head": dist_head,
                    "fired_diameter": fired_dia,
                    "leather_hard_pilot_diameter": leather_cut,
                    "ratio": HOLE_RATIOS[idx - 1],
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]], headers: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in headers})


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def master(value: float, shrink: float) -> float:
    return value / (1 - shrink)


def family_markdown(rows: list[dict[str, object]]) -> str:
    lines = [
        "| ID | Key | Bore ID | OD | Sounding length | Pre-trim fired length | Master X length @12% |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {id} | {key} | {bore:.3f} in | {od:.3f} in | {sounding:.3f} in | {pretrim:.3f} in | {master:.3f} in |".format(
                id=row["id"],
                key=row["key"],
                bore=float(row["bore"]),
                od=float(row["od"]),
                sounding=float(row["sounding"]),
                pretrim=float(row["pretrim"]),
                master=master(float(row["pretrim"]), SHRINK_X),
            )
        )
    return "\n".join(lines)


def design_table_rows(family_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output = []
    for row in family_rows:
        output.append(
            {
                "instrument_id": row["id"],
                "variant": row["variant"],
                "key": row["key"],
                "midi": row["midi"],
                "fundamental_hz": r(float(row["frequency"]), 3),
                "bore_id_fired_in": r(float(row["bore"]), 3),
                "wall_thickness_fired_in": r(float(row["wall"]), 3),
                "od_fired_in": r(float(row["od"]), 3),
                "acoustic_length_in": r(float(row["acoustic"]), 3),
                "end_correction_total_in": r(float(row["end_corr"]), 3),
                "sounding_length_embouchure_to_foot_fired_in": r(float(row["sounding"]), 3),
                "head_margin_fired_in": r(float(row["head_margin"]), 3),
                "foot_trim_band_fired_in": r(float(row["foot_trim"]), 3),
                "pretrim_overall_length_fired_in": r(float(row["pretrim"]), 3),
                "embouchure_center_from_head_fired_in": r(float(row["head_margin"]), 3),
                "embouchure_x_length_fired_in": r(float(row["emb_x"]), 3),
                "embouchure_y_width_fired_in": r(float(row["emb_y"]), 3),
                "master_overall_length_x_in_initial": r(master(float(row["pretrim"]), SHRINK_X), 3),
                "master_bore_y_in_initial": r(master(float(row["bore"]), SHRINK_Y), 3),
                "master_od_y_in_initial": r(master(float(row["od"]), SHRINK_Y), 3),
                "master_od_z_in_initial": r(master(float(row["od"]), SHRINK_Z), 3),
                "bore_profile": row["profile"],
                "clay_body_round_1": row["body"],
                "status": "Round 1 target fired dimensions",
            }
        )
    return output


def hole_csv_rows(hole_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out = []
    for row in hole_rows:
        out.append(
            {
                "instrument_id": row["instrument_id"],
                "key": row["key"],
                "hole_no": row["hole"],
                "scale_degree_interval_semitones": row["interval"],
                "target_note": row["note"],
                "target_frequency_hz": r(float(row["frequency"]), 3),
                "fired_center_from_foot_in": r(float(row["fired_distance_from_foot"]), 3),
                "fired_center_from_head_in": r(float(row["fired_distance_from_head"]), 3),
                "fired_hole_diameter_in": r(float(row["fired_diameter"]), 3),
                "leather_hard_pilot_cut_dia_in_85pct": r(float(row["leather_hard_pilot_diameter"]), 3),
                "hole_to_bore_ratio": row["ratio"],
                "round_1_note": "Cut pilot undersize; tune after bisque by opening the hole. Position is first-pass open-open model.",
            }
        )
    return out


def doe_rows() -> list[dict[str, object]]:
    keys = ["SCF-D4-01", "SCF-G4-01", "SCF-C5-01"]
    clays = ["Cone 6 stoneware", "Cone 6 porcelain"]
    walls = ["thin drain", "nominal drain", "thick drain"]
    profiles = ["cylindrical", "mild taper"]
    emb = ["round/standard oval", "long oval"]
    orientations = ["horizontal drain", "vertical drain"]
    rows: list[dict[str, object]] = []
    run = 1
    for key_i, inst in enumerate(keys):
        for clay_i, clay in enumerate(clays):
            for wall_i, wall in enumerate(walls):
                profile = profiles[(key_i + clay_i + wall_i) % 2]
                embouchure = emb[(key_i + wall_i) % 2]
                orientation = orientations[(clay_i + wall_i) % 2]
                rows.append(
                    {
                        "run_id": f"SCF-R1-{run:02d}",
                        "phase": "Round 1 screening",
                        "instrument_id": inst,
                        "clay_body": clay,
                        "wall_target": wall,
                        "bore_profile": profile,
                        "embouchure_geometry": embouchure,
                        "mold_orientation": orientation,
                        "replicate": "screening",
                        "primary_response": "X/Y/Z shrink, playable response, cents error",
                        "decision_rule": "Keep if no cracks, first octave speaks, median cents abs <= 35 after bisque tune.",
                    }
                )
                run += 1
    rows.extend(
        [
            {
                "run_id": "SCF-R1-FAM-F4",
                "phase": "Round 1 family check",
                "instrument_id": "SCF-F4-01",
                "clay_body": "Best available from early screening",
                "wall_target": "nominal drain",
                "bore_profile": "winner or cylindrical fallback",
                "embouchure_geometry": "winner or standard oval fallback",
                "mold_orientation": "winner or horizontal drain fallback",
                "replicate": "family fill-in",
                "primary_response": "Interpolation across family range",
                "decision_rule": "Use to test whether shrink model interpolates between D4/G4/C5.",
            },
            {
                "run_id": "SCF-R1-FAM-A4",
                "phase": "Round 1 family check",
                "instrument_id": "SCF-A4-01",
                "clay_body": "Best available from early screening",
                "wall_target": "nominal drain",
                "bore_profile": "winner or cylindrical fallback",
                "embouchure_geometry": "winner or standard oval fallback",
                "mold_orientation": "winner or horizontal drain fallback",
                "replicate": "family fill-in",
                "primary_response": "Interpolation across family range",
                "decision_rule": "Use to test whether shrink model interpolates between G4/C5.",
            },
        ]
    )
    return rows


def bom_rows() -> list[dict[str, object]]:
    return [
        {
            "item_id": "SCF-BOM-001",
            "subsystem": "CAD/master",
            "item": "Parametric flute body master set",
            "qty": "5",
            "unit": "masters",
            "material_spec": "Sealed 3D print or machined master, scaled by X/Y/Z shrink factors",
            "make_buy": "Make",
            "drawing_ref": "drawings/SCF-*-body.svg; cad/slip_cast_transverse_flute_body.scad",
            "notes": "Use as mold masters or CAD reference. Add mold split before production tooling.",
        },
        {
            "item_id": "SCF-BOM-002",
            "subsystem": "Mold",
            "item": "Two-piece or three-piece plaster molds",
            "qty": "5+",
            "unit": "molds",
            "material_spec": "Pottery plaster, registration keys, pour/drain reservoir",
            "make_buy": "Make",
            "drawing_ref": "drawings/mold-stack.svg",
            "notes": "D4 may need sectional mold or reinforced cradle due to length.",
        },
        {
            "item_id": "SCF-BOM-003",
            "subsystem": "Material",
            "item": "Cone 6 stoneware casting slip",
            "qty": "TBD",
            "unit": "gallons",
            "material_spec": "Casting slip with known fired shrinkage and absorption",
            "make_buy": "Buy/mix",
            "drawing_ref": "data/doe-build-matrix.csv",
            "notes": "Date-check supplier and record batch number.",
        },
        {
            "item_id": "SCF-BOM-004",
            "subsystem": "Material",
            "item": "Cone 6 porcelain casting slip",
            "qty": "TBD",
            "unit": "gallons",
            "material_spec": "Porcelain slip for comparison runs",
            "make_buy": "Buy/mix",
            "drawing_ref": "data/doe-build-matrix.csv",
            "notes": "Higher shrink/warpage risk, better density and surface.",
        },
        {
            "item_id": "SCF-BOM-005",
            "subsystem": "Tuning",
            "item": "Diamond needle files and small diamond burrs",
            "qty": "1",
            "unit": "set",
            "material_spec": "Fine files for bisque and fired ceramic hole tuning",
            "make_buy": "Buy",
            "drawing_ref": "assembly-manual.md",
            "notes": "Avoid glazing acoustic edges after tuning.",
        },
        {
            "item_id": "SCF-BOM-006",
            "subsystem": "Validation",
            "item": "Measurement kit",
            "qty": "1",
            "unit": "kit",
            "material_spec": "Calipers, bore gauges/pin gauges, tuner, mic, thermometer/hygrometer, scale",
            "make_buy": "Use/buy",
            "drawing_ref": "validation.csv",
            "notes": "Use the same tuner/mic distance for all response tests.",
        },
        {
            "item_id": "SCF-BOM-007",
            "subsystem": "Voicing",
            "item": "Cork/stopper test kit",
            "qty": "5",
            "unit": "sets",
            "material_spec": "Cork, silicone, or printed plug for head-end tuning experiments",
            "make_buy": "Make/buy",
            "drawing_ref": "drawing-brief.md",
            "notes": "Treat head-stopper position as an adjustable variable before ceramic-integral solutions.",
        },
        {
            "item_id": "SCF-BOM-008",
            "subsystem": "Finish",
            "item": "Wax resist and glaze test set",
            "qty": "1",
            "unit": "set",
            "material_spec": "Food-safe/contact-safe glaze where mouth contact occurs; acoustic edges waxed clear",
            "make_buy": "Buy",
            "drawing_ref": "mold-workflow.md",
            "notes": "Keep glaze out of embouchure, bore, tone holes, and stopper fit surfaces.",
        },
    ]


def sourcing_rows() -> list[dict[str, object]]:
    return [
        {
            "source_id": "SRC-SLIP-STONEWARE",
            "category": "Ceramic slip",
            "spec": "Cone 6 stoneware casting slip, published shrinkage and absorption data",
            "supplier_or_search_terms": "local ceramic supplier cone 6 stoneware casting slip shrinkage data sheet",
            "qty": "TBD",
            "date_checked": "",
            "unit_price": "",
            "lead_time": "",
            "substitution_rule": "Must have measured or published shrinkage; color can vary.",
            "risk_notes": "Live price and availability intentionally blank until purchase planning.",
        },
        {
            "source_id": "SRC-SLIP-PORCELAIN",
            "category": "Ceramic slip",
            "spec": "Cone 6 porcelain casting slip, low warpage preferred",
            "supplier_or_search_terms": "cone 6 porcelain casting slip shrinkage casting data sheet",
            "qty": "TBD",
            "date_checked": "",
            "unit_price": "",
            "lead_time": "",
            "substitution_rule": "Substitute only with data-backed shrink and firing schedule.",
            "risk_notes": "Porcelain may move more; use bars and rings before long D4 molds.",
        },
        {
            "source_id": "SRC-PLASTER",
            "category": "Mold material",
            "spec": "Pottery plaster or high-strength mold plaster",
            "supplier_or_search_terms": "USG pottery plaster No. 1 local ceramic supplier",
            "qty": "TBD",
            "date_checked": "",
            "unit_price": "",
            "lead_time": "",
            "substitution_rule": "Must be absorbent mold plaster, not general patching plaster.",
            "risk_notes": "Mold drying time affects casting wall thickness and repeatability.",
        },
        {
            "source_id": "SRC-PRINT",
            "category": "Master fabrication",
            "spec": "High-resolution sealed print or machined master; smooth bore core strategy",
            "supplier_or_search_terms": "SLA print service large format resin smooth finish or in-house FDM sealed master",
            "qty": "5 masters plus coupons",
            "date_checked": "",
            "unit_price": "",
            "lead_time": "",
            "substitution_rule": "Any method is acceptable if master dimensions are measured and sealed.",
            "risk_notes": "Layer lines transfer to plaster and may disturb mold release.",
        },
        {
            "source_id": "SRC-TUNING",
            "category": "Tuning tools",
            "spec": "Diamond needle files, small diamond burrs, tuner/mic",
            "supplier_or_search_terms": "diamond needle file set ceramic tuning burr chromatic tuner measurement microphone",
            "qty": "1 kit",
            "date_checked": "",
            "unit_price": "",
            "lead_time": "",
            "substitution_rule": "Prefer fine controlled abrasion over aggressive rotary cutting.",
            "risk_notes": "Over-opening holes is not reversible.",
        },
    ]


def cut_list_rows(family_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in family_rows:
        rows.append(
            {
                "cut_id": f"CUT-{row['id']}",
                "part": "Scaled master body blank/envelope",
                "qty": "1",
                "rough_dimensions": f"{r(master(float(row['pretrim']), SHRINK_X)+1.0, 2)} x {r(master(float(row['od']), SHRINK_Y)+0.5, 2)} x {r(master(float(row['od']), SHRINK_Z)+0.5, 2)} in",
                "final_dimensions": f"{r(master(float(row['pretrim']), SHRINK_X), 3)} x {r(master(float(row['od']), SHRINK_Y), 3)} x {r(master(float(row['od']), SHRINK_Z), 3)} in",
                "material": "Sealed printed/machined master",
                "orientation": "X along bore axis; mark top/embouchure datum",
                "operation": "Print/machine, sand, seal, measure, then mold",
                "yield_or_notes": "Add handles/sprues outside acoustic envelope only.",
            }
        )
    rows.extend(
        [
            {
                "cut_id": "CUT-SHRINK-BAR-X",
                "part": "Shrinkage bar set",
                "qty": "12",
                "rough_dimensions": "6.5 x 0.5 x 0.25 in master or cast bars",
                "final_dimensions": "Measure fired length, width, thickness",
                "material": "Each slip body",
                "orientation": "Label X, Y, Z and casting direction",
                "operation": "Cast alongside every flute run",
                "yield_or_notes": "Primary anisotropic shrink data.",
            },
            {
                "cut_id": "CUT-BORE-RING",
                "part": "Bore/roundness ring coupons",
                "qty": "12",
                "rough_dimensions": "OD/ID matching each bore family",
                "final_dimensions": "Measure fired ID/OD in Y and Z",
                "material": "Each slip body",
                "orientation": "Same drain orientation as flute",
                "operation": "Cast with flute body",
                "yield_or_notes": "Detect ovalization and wall-thickness drift.",
            },
        ]
    )
    return rows


def validation_rows(family_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in family_rows:
        rows.append(
            {
                "build_id": "",
                "instrument_id": row["id"],
                "stage": "final fired",
                "measurement": "fundamental",
                "target_value": r(float(row["frequency"]), 3),
                "unit": "Hz",
                "tolerance": "+/-10 cents after tuning; Round 1 accepts +/-35 cents before correction",
                "measured_value": "",
                "environment": "Record temp F / humidity / tuner distance",
                "result": "",
                "action": "Move stopper, file embouchure/tone holes, or update Round 2 CAD factor.",
            }
        )
        rows.append(
            {
                "build_id": "",
                "instrument_id": row["id"],
                "stage": "final fired",
                "measurement": "overall length X",
                "target_value": r(float(row["pretrim"]), 3),
                "unit": "in",
                "tolerance": "+/-0.030 in before trim",
                "measured_value": "",
                "environment": "Room temp; calipers/tape ID",
                "result": "",
                "action": "Use target/measured as Round 2 X scale correction.",
            }
        )
        rows.append(
            {
                "build_id": "",
                "instrument_id": row["id"],
                "stage": "final fired",
                "measurement": "bore ID Y/Z",
                "target_value": r(float(row["bore"]), 3),
                "unit": "in",
                "tolerance": "+/-0.010 in; record Y and Z separately",
                "measured_value": "",
                "environment": "Pin gauge or bore gauge",
                "result": "",
                "action": "Use Y/Z shrink correction and check ovalization.",
            }
        )
    return rows


def measurement_template_rows() -> list[dict[str, object]]:
    return [
        {
            "build_id": "SCF-R1-01-A",
            "instrument_id": "SCF-D4-01",
            "material_batch": "",
            "mold_id": "",
            "axis": "X",
            "feature": "overall_length",
            "master_target_in": "",
            "master_measured_in": "",
            "wet_green_measured_in": "",
            "bone_dry_measured_in": "",
            "bisque_measured_in": "",
            "glaze_measured_in": "",
            "observed_total_shrink": "=IF(OR(H2=\"\",L2=\"\"),\"\",1-L2/H2)",
            "round2_scale_multiplier": "=IF(OR(G2=\"\",L2=\"\"),\"\",G2/L2)",
            "target_frequency_hz": "",
            "measured_frequency_hz": "",
            "cents_error": "=IF(OR(O2=\"\",P2=\"\"),\"\",1200*LOG(P2/O2,2))",
            "notes": "Duplicate rows for each feature/axis/note.",
        }
    ]


def shrink_fit_rows() -> list[dict[str, object]]:
    return [
        {
            "axis": "X length",
            "initial_assumed_shrink": SHRINK_X,
            "measured_mean_shrink": "",
            "measured_std_dev": "",
            "recommended_round2_shrink": "=IF(C2=\"\",B2,C2)",
            "apply_to_features": "overall length, hole station X, embouchure station X",
            "notes": "Separate D4/G4/C5 if shrink depends on length or mold orientation.",
        },
        {
            "axis": "Y width",
            "initial_assumed_shrink": SHRINK_Y,
            "measured_mean_shrink": "",
            "measured_std_dev": "",
            "recommended_round2_shrink": "=IF(C3=\"\",B3,C3)",
            "apply_to_features": "bore ID Y, OD Y, horizontal hole/embouchure dimensions",
            "notes": "Use bore rings to separate shrink from wall buildup.",
        },
        {
            "axis": "Z height",
            "initial_assumed_shrink": SHRINK_Z,
            "measured_mean_shrink": "",
            "measured_std_dev": "",
            "recommended_round2_shrink": "=IF(C4=\"\",B4,C4)",
            "apply_to_features": "OD Z, wall thickness, vertical hole/embouchure dimensions",
            "notes": "Watch sag/ovalization separately from true shrink.",
        },
    ]


def draw_body_svg(row: dict[str, object], holes: list[dict[str, object]]) -> str:
    length = float(row["pretrim"])
    od = float(row["od"])
    scale = min(42.0, 1040.0 / length)
    margin = 70
    body_x = margin
    body_y = 120
    body_w = length * scale
    body_h = max(24, od * scale)
    height = 330
    width = int(body_w + 2 * margin)
    def x_from_head(value: float) -> float:
        return body_x + value * scale
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,sans-serif;font-size:12px;fill:#102030}.small{font-size:10px}.line{stroke:#102030;stroke-width:1.2;fill:none}.dim{stroke:#446;stroke-width:1;marker-start:url(#a);marker-end:url(#a)}.body{fill:#f7f4ee;stroke:#102030;stroke-width:1.5}.hole{fill:#ffffff;stroke:#102030;stroke-width:1.2}</style>",
        '<defs><marker id="a" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto"><path d="M0,3 L6,0 L6,6 Z" fill="#446"/></marker></defs>',
        f'<text x="{margin}" y="34" style="font-size:18px;font-weight:bold">{escape(str(row["id"]))} Slip-Cast Transverse Flute - Fired Target Drawing</text>',
        f'<text x="{margin}" y="54">Key {escape(str(row["key"]))}; bore ID {float(row["bore"]):.3f} in; OD {od:.3f} in; pre-trim fired length {length:.3f} in; initial master X {master(length, SHRINK_X):.3f} in at 12% shrink</text>',
        f'<rect class="body" x="{body_x:.1f}" y="{body_y:.1f}" width="{body_w:.1f}" height="{body_h:.1f}" rx="{body_h/2:.1f}"/>',
        f'<line class="line" x1="{body_x:.1f}" y1="{body_y+body_h/2:.1f}" x2="{body_x+body_w:.1f}" y2="{body_y+body_h/2:.1f}" stroke-dasharray="5 5"/>',
    ]
    emb_x = x_from_head(float(row["head_margin"]))
    emb_w = float(row["emb_x"]) * scale
    emb_h = max(8, float(row["emb_y"]) * scale)
    lines.append(f'<ellipse class="hole" cx="{emb_x:.1f}" cy="{body_y+body_h/2:.1f}" rx="{emb_w/2:.1f}" ry="{emb_h/2:.1f}"/>')
    lines.append(f'<text class="small" x="{emb_x-30:.1f}" y="{body_y-12:.1f}">Emb</text>')
    for h in holes:
        hx = x_from_head(float(h["fired_distance_from_head"]))
        dia = max(7, float(h["fired_diameter"]) * scale)
        lines.append(f'<circle class="hole" cx="{hx:.1f}" cy="{body_y+body_h/2:.1f}" r="{dia/2:.1f}"/>')
        lines.append(f'<text class="small" x="{hx-10:.1f}" y="{body_y+body_h+28:.1f}">H{h["hole"]}</text>')
        lines.append(f'<text class="small" x="{hx-16:.1f}" y="{body_y+body_h+42:.1f}">{escape(str(h["note"]))}</text>')
    dim_y = body_y + body_h + 75
    lines.extend(
        [
            f'<line class="dim" x1="{body_x:.1f}" y1="{dim_y:.1f}" x2="{body_x+body_w:.1f}" y2="{dim_y:.1f}"/>',
            f'<line class="line" x1="{body_x:.1f}" y1="{body_y+body_h:.1f}" x2="{body_x:.1f}" y2="{dim_y+8:.1f}"/>',
            f'<line class="line" x1="{body_x+body_w:.1f}" y1="{body_y+body_h:.1f}" x2="{body_x+body_w:.1f}" y2="{dim_y+8:.1f}"/>',
            f'<text x="{body_x+body_w/2-70:.1f}" y="{dim_y+22:.1f}">Pre-trim fired length {length:.3f} in</text>',
            f'<text class="small" x="{margin}" y="{height-46}">Datums: X0=head end, X+ toward foot; centerline through bore. Tone-hole stations are first-pass acoustic targets and should be cut undersize, then tuned after bisque.</text>',
            f'<text class="small" x="{margin}" y="{height-28}">Shrink model: master_x=fired_x/(1-sx), master_y=fired_y/(1-sy), master_z=fired_z/(1-sz). Initial sx=sy=sz=12%; replace with measured Round 1 data.</text>',
            "</svg>",
        ]
    )
    return "\n".join(lines)


def draw_family_svg(family_rows: list[dict[str, object]], holes: list[dict[str, object]]) -> str:
    width = 1250
    row_h = 92
    height = 110 + row_h * len(family_rows)
    max_len = max(float(row["pretrim"]) for row in family_rows)
    scale = 980 / max_len
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        "<style>text{font-family:Arial,sans-serif;font-size:12px;fill:#102030}.title{font-size:22px;font-weight:bold}.body{fill:#f7f4ee;stroke:#102030;stroke-width:1.4}.hole{fill:#fff;stroke:#102030;stroke-width:1}.axis{stroke:#607080;stroke-width:1;stroke-dasharray:5 5}</style>",
        f'<text class="title" x="40" y="40">Slip-Cast Transverse Flute Family - Fired Target Lengths</text>',
        f'<text x="40" y="63">Generated {DATE}. Dimensions are final fired targets; master dimensions use X/Y/Z shrink factors and are listed in the workbook/data tables.</text>',
    ]
    y = 100
    for row in family_rows:
        x = 180
        length = float(row["pretrim"])
        od = float(row["od"])
        body_w = length * scale
        body_h = max(18, od * scale)
        center_y = y + row_h / 2
        lines.append(f'<text x="40" y="{center_y-4:.1f}" style="font-weight:bold">{escape(str(row["id"]))}</text>')
        lines.append(f'<text x="40" y="{center_y+13:.1f}">{escape(str(row["key"]))}, {length:.2f} in fired</text>')
        lines.append(f'<rect class="body" x="{x:.1f}" y="{center_y-body_h/2:.1f}" width="{body_w:.1f}" height="{body_h:.1f}" rx="{body_h/2:.1f}"/>')
        lines.append(f'<line class="axis" x1="{x:.1f}" y1="{center_y:.1f}" x2="{x+body_w:.1f}" y2="{center_y:.1f}"/>')
        inst_holes = [h for h in holes if h["instrument_id"] == row["id"]]
        emb_x = x + float(row["head_margin"]) * scale
        lines.append(f'<ellipse class="hole" cx="{emb_x:.1f}" cy="{center_y:.1f}" rx="{max(5,float(row["emb_x"])*scale/2):.1f}" ry="{max(4,float(row["emb_y"])*scale/2):.1f}"/>')
        for h in inst_holes:
            hx = x + float(h["fired_distance_from_head"]) * scale
            dia = max(4, float(h["fired_diameter"]) * scale)
            lines.append(f'<circle class="hole" cx="{hx:.1f}" cy="{center_y:.1f}" r="{dia/2:.1f}"/>')
        lines.append(f'<text x="{x+body_w+18:.1f}" y="{center_y-4:.1f}">bore {float(row["bore"]):.3f} in</text>')
        lines.append(f'<text x="{x+body_w+18:.1f}" y="{center_y+13:.1f}">master X {master(length, SHRINK_X):.2f} in @12%</text>')
        y += row_h
    lines.append("</svg>")
    return "\n".join(lines)


def draw_mold_svg() -> str:
    return """<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="520" viewBox="0 0 1100 520">
<style>text{font-family:Arial,sans-serif;font-size:14px;fill:#102030}.title{font-size:22px;font-weight:bold}.part{fill:#f7f4ee;stroke:#102030;stroke-width:1.5}.mold{fill:#d9e2e7;stroke:#102030;stroke-width:1.4}.line{stroke:#102030;stroke-width:1.2;fill:none}.dim{stroke:#445;stroke-width:1;stroke-dasharray:4 4}.call{font-size:12px}</style>
<text class="title" x="40" y="42">Slip-Cast Transverse Flute Mold Stack - Concept Drawing</text>
<text x="40" y="68">Use as a manufacturing brief, not a finished mold drawing. Final split lines depend on CAD draft, release tests, and clay body.</text>
<rect class="mold" x="120" y="150" width="820" height="92" rx="18"/>
<rect class="mold" x="120" y="278" width="820" height="92" rx="18"/>
<rect class="part" x="185" y="236" width="690" height="56" rx="28"/>
<line class="dim" x1="120" y1="260" x2="940" y2="260"/>
<circle class="part" cx="250" cy="264" r="15"/>
<circle class="part" cx="380" cy="264" r="10"/>
<circle class="part" cx="455" cy="264" r="10"/>
<circle class="part" cx="525" cy="264" r="10"/>
<circle class="part" cx="590" cy="264" r="10"/>
<circle class="part" cx="655" cy="264" r="10"/>
<circle class="part" cx="720" cy="264" r="10"/>
<path class="line" d="M165 150 L165 370"/>
<path class="line" d="M895 150 L895 370"/>
<circle cx="210" cy="196" r="13" fill="#fff" stroke="#102030"/>
<circle cx="830" cy="196" r="13" fill="#fff" stroke="#102030"/>
<circle cx="210" cy="324" r="13" fill="#fff" stroke="#102030"/>
<circle cx="830" cy="324" r="13" fill="#fff" stroke="#102030"/>
<text class="call" x="150" y="126">Pour/drain reservoir at head or foot; keep it outside final fired trim band.</text>
<line class="line" x1="180" y1="132" x2="190" y2="225"/>
<text class="call" x="430" y="126">Molded center marks are useful; cut tone holes undersize at leather-hard stage for tuning.</text>
<line class="line" x1="575" y1="132" x2="575" y2="248"/>
<text class="call" x="610" y="425">Registration keys clear of bore axis and acoustic edges.</text>
<line class="line" x1="700" y1="405" x2="830" y2="337"/>
<text class="call" x="120" y="425">Optional three-piece mold for D4 length, ovalized forms, or undercut-looking external detail.</text>
<text class="call" x="40" y="482">Critical controls: mold dry weight, pour time, drain time, wall thickness coupon, demold time, seam cleanup, head-stopper fit, and edge glaze exclusion.</text>
</svg>"""


def write_drawings(family_rows: list[dict[str, object]], hole_rows: list[dict[str, object]]) -> None:
    write_text(ROOT / "drawings" / "family-overview.svg", draw_family_svg(family_rows, hole_rows))
    write_text(ROOT / "drawings" / "mold-stack.svg", draw_mold_svg())
    for row in family_rows:
        holes = [h for h in hole_rows if h["instrument_id"] == row["id"]]
        write_text(ROOT / "drawings" / f"{row['id']}-body.svg", draw_body_svg(row, holes))


def col_name(index: int) -> str:
    name = ""
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name


def xlsx_cell(ref: str, value: object) -> str:
    if value is None:
        return f'<c r="{ref}"/>'
    if isinstance(value, str) and value.startswith("="):
        return f'<c r="{ref}"><f>{escape(value[1:])}</f></c>'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{ref}"><v>{value}</v></c>'
    text = escape(str(value))
    return f'<c r="{ref}" t="inlineStr"><is><t>{text}</t></is></c>'


def sheet_xml(rows: list[list[object]]) -> str:
    out = [
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">',
        "<sheetData>",
    ]
    for r_idx, row in enumerate(rows, start=1):
        out.append(f'<row r="{r_idx}">')
        for c_idx, value in enumerate(row, start=1):
            if value == "":
                continue
            out.append(xlsx_cell(f"{col_name(c_idx)}{r_idx}", value))
        out.append("</row>")
    out.extend(["</sheetData>", "</worksheet>"])
    return "\n".join(out)


def write_xlsx(path: Path, sheets: list[tuple[str, list[list[object]]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook_sheets = []
    workbook_rels = []
    content_overrides = [
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    for idx, (name, _) in enumerate(sheets, start=1):
        workbook_sheets.append(f'<sheet name="{escape(name)}" sheetId="{idx}" r:id="rId{idx}"/>')
        workbook_rels.append(
            f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>'
        )
        content_overrides.append(
            f'<Override PartName="/xl/worksheets/sheet{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        )
    workbook_rels.append(
        f'<Relationship Id="rId{len(sheets)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(
            "[Content_Types].xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
            + "".join(content_overrides)
            + "</Types>",
        )
        zf.writestr(
            "_rels/.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>',
        )
        zf.writestr(
            "xl/workbook.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
            + "".join(workbook_sheets)
            + '</sheets><calcPr calcMode="auto"/></workbook>',
        )
        zf.writestr(
            "xl/_rels/workbook.xml.rels",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            + "".join(workbook_rels)
            + "</Relationships>",
        )
        zf.writestr(
            "xl/styles.xml",
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts><fills count="1"><fill><patternFill patternType="none"/></fill></fills><borders count="1"><border/></borders><cellStyleXfs count="1"><xf/></cellStyleXfs><cellXfs count="1"><xf xfId="0"/></cellXfs></styleSheet>',
        )
        for idx, (_, rows) in enumerate(sheets, start=1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", sheet_xml(rows))


def workbook_rows(family_rows: list[dict[str, object]], hole_rows: list[dict[str, object]], doe: list[dict[str, object]]) -> list[tuple[str, list[list[object]]]]:
    inputs = [
        ["Slip-Cast Transverse Flute Family Inputs"],
        ["Generated", DATE],
        ["Source basis", "Open-open flute model adapted from Tony's Flutes-AI.xlsx Irish Flute sheet"],
        [],
        ["A4_Hz", A4_HZ],
        ["speed_of_sound_in_per_s_68F", SPEED_SOUND_IN_S],
        ["shrink_x_initial", SHRINK_X, "X axis = bore length and hole stations"],
        ["shrink_y_initial", SHRINK_Y, "Y axis = side-to-side bore/OD and hole width"],
        ["shrink_z_initial", SHRINK_Z, "Z axis = vertical OD/wall/ovalization"],
        ["round2_rule", "new_master_axis = old_master_axis * target_fired_axis / measured_fired_axis"],
    ]
    fired = [
        [
            "instrument_id",
            "variant",
            "key",
            "midi",
            "fundamental_hz",
            "bore_id_fired_in",
            "wall_fired_in",
            "od_fired_in",
            "acoustic_length_in",
            "end_correction_total_in",
            "sounding_length_in",
            "head_margin_in",
            "foot_trim_band_in",
            "pretrim_overall_fired_in",
            "embouchure_x_len_fired_in",
            "embouchure_y_width_fired_in",
        ]
    ]
    for excel_row, row in enumerate(family_rows, start=2):
        fired.append(
            [
                row["id"],
                row["variant"],
                row["key"],
                row["midi"],
                f"=Inputs!$B$5*2^((D{excel_row}-69)/12)",
                row["bore"],
                row["wall"],
                f"=F{excel_row}+2*G{excel_row}",
                f"=Inputs!$B$6/(2*E{excel_row})",
                f"=0.6*F{excel_row}",
                f"=I{excel_row}-J{excel_row}",
                f"=1.5*F{excel_row}",
                0.5,
                f"=K{excel_row}+L{excel_row}+M{excel_row}",
                f"=0.63*F{excel_row}",
                f"=0.52*F{excel_row}",
            ]
        )
    master_rows = [
        [
            "instrument_id",
            "master_overall_x_in",
            "master_bore_y_in",
            "master_od_y_in",
            "master_od_z_in",
            "master_emb_x_in",
            "master_emb_y_in",
            "formula_note",
        ]
    ]
    for idx, row in enumerate(family_rows, start=2):
        master_rows.append(
            [
                row["id"],
                f"='Fired Targets'!N{idx}/(1-Inputs!$B$7)",
                f"='Fired Targets'!F{idx}/(1-Inputs!$B$8)",
                f"='Fired Targets'!H{idx}/(1-Inputs!$B$8)",
                f"='Fired Targets'!H{idx}/(1-Inputs!$B$9)",
                f"='Fired Targets'!O{idx}/(1-Inputs!$B$7)",
                f"='Fired Targets'!P{idx}/(1-Inputs!$B$8)",
                "Update Inputs B7:B9 after Round 1 measurement.",
            ]
        )
    hole_sheet = [
        [
            "instrument_id",
            "key",
            "hole_no",
            "interval",
            "target_note",
            "target_frequency_hz",
            "fired_center_from_foot_in",
            "fired_center_from_head_in",
            "fired_hole_diameter_in",
            "leather_hard_pilot_dia_in_85pct",
            "notes",
        ]
    ]
    for row in hole_rows:
        hole_sheet.append(
            [
                row["instrument_id"],
                row["key"],
                row["hole"],
                row["interval"],
                row["note"],
                r(float(row["frequency"]), 3),
                r(float(row["fired_distance_from_foot"]), 3),
                r(float(row["fired_distance_from_head"]), 3),
                r(float(row["fired_diameter"]), 3),
                r(float(row["leather_hard_pilot_diameter"]), 3),
                "First-pass station; cut undersize and tune after bisque.",
            ]
        )
    doe_sheet = [list(doe[0].keys())] + [list(row.values()) for row in doe]
    measurements = [list(measurement_template_rows()[0].keys()), list(measurement_template_rows()[0].values())]
    shrink_fit = [list(shrink_fit_rows()[0].keys())] + [list(row.values()) for row in shrink_fit_rows()]
    return [
        ("Inputs", inputs),
        ("Fired Targets", fired),
        ("Master Scale", master_rows),
        ("Hole Schedule", hole_sheet),
        ("DoE Matrix", doe_sheet),
        ("Measurements", measurements),
        ("Shrink Fit", shrink_fit),
    ]


def write_markdown_docs(family_rows: list[dict[str, object]], doe: list[dict[str, object]]) -> None:
    family_table = family_markdown(family_rows)
    write_text(
        ROOT / "README.md",
        f"""
# Slip-Cast Transverse Flute Family

This folder is a build packet for a first-round family of slip-cast ceramic transverse flutes. It is set up for the workflow you described: target final fired dimensions first, build from shrink-scaled masters, measure the fired results, fit X/Y/Z shrinkage and acoustic correction factors, then run a second corrected round.

Start with:

- `Slip-Cast-Transverse-Flute-Family.xlsx` for the parametric workbook.
- `data/fired-dimension-targets.csv` for target fired dimensions.
- `data/hole-schedule.csv` for first-pass tone-hole stations.
- `data/doe-build-matrix.csv` for the Round 1 screening plan.
- `drawings/family-overview.svg` and individual `drawings/SCF-*-body.svg` files for shop review.
- `assembly-manual.md`, `mold-workflow.md`, and `validation.csv` for the actual build/measure loop.

All shrink factors are deliberately provisional: X=12%, Y=12%, Z=12%. Replace them with measured values after Round 1.
""",
    )
    write_text(
        ROOT / "design.md",
        f"""
# Slip-Cast Transverse Flute Family Build Packet

## Source And Scope

- Date: `{DATE}`
- Source workbook inspected: `/mnt/c/Users/Tony/Documents/Claude/Projects/Career/flutes-staging/Flutes-AI.xlsx`
- Relevant sheet: `Irish Flute`, which uses open-open flute math, D4 sanity dimensions, end correction, and 6-hole diatonic placement.
- Ceramic workflow references inspected: `Ocarina`, `Udu Drum Family`, and `vessel-flute-lab` build packets.

This packet is for unkeyed transverse ceramic flute prototypes made by slip casting. The acoustic dimensions below are final fired targets. Master and mold dimensions are scaled from those targets using provisional X/Y/Z shrink factors.

## Design Intent

Build a family across D4, F4, G4, A4, and C5 so the study sees both long-body casting behavior and smaller higher-key behavior. Round 1 is not trying to prove a finished product. It is meant to produce a clean data set:

- actual X/Y/Z fired shrink by material, wall, and mold orientation,
- actual bore roundness and wall buildup,
- pitch and response error against the open-open first-pass model,
- embouchure and bore-profile preferences before Round 2.

## Governing Model

First-pass open-open transverse flute model:

```text
f = c / (2 * L_eff)
L_acoustic = c / (2 * f)
end_correction_total ~= 0.6 * bore_ID
sounding_length ~= L_acoustic - end_correction_total
hole_distance_from_foot ~= L_acoustic * (fundamental_frequency / hole_frequency)
```

The hole positions are first-pass acoustic stations. Ceramic wall thickness, hole chimney height, undercutting, bore ovalization, embouchure geometry, and stopper position will move real pitch. The packet therefore makes hole cuts undersize and expects bisque-stage tuning.

## Initial Family Targets

{family_table}

## Shrinkage Model

Coordinate convention:

- X = flute length/bore axis/hole stations.
- Y = side-to-side bore and outside width.
- Z = vertical height, wall buildup, and ovalization direction.

```text
master_x = fired_target_x / (1 - shrink_x)
master_y = fired_target_y / (1 - shrink_y)
master_z = fired_target_z / (1 - shrink_z)
observed_shrink_axis = 1 - fired_measured_axis / master_measured_axis
round2_master_axis = round1_master_axis * fired_target_axis / fired_measured_axis
```

Initial assumption is `shrink_x = shrink_y = shrink_z = 0.12`. This is a placeholder, not a material claim.

## Round 1 Success Criteria

- No full-length cracking through drying, bisque, or glaze fire.
- Bore remains measurable and cleanable.
- Embouchure speaks a stable fundamental and octave on at least the G4 or C5 prototypes.
- Hole tuning can be brought within +/-35 cents after bisque without grotesque hole enlargement.
- X/Y/Z shrink measurements have enough consistency to choose Round 2 scale factors.

## Round 2 Decision Path

1. Fit shrink_x, shrink_y, and shrink_z from bars, bore rings, and flute features.
2. Choose the best material/profile/embouchure combination from the DoE.
3. Update the workbook inputs and regenerate master dimensions.
4. Rebuild the full five-key family using corrected X/Y/Z scale factors.
5. Tighten acceptance to +/-10 cents for tuned notes and +/-0.010 to +/-0.030 in on critical fired dimensions.

## Open Assumptions

- Bore diameters are adapted from the existing Irish/simple-system flute design range, then made ceramic-friendly with thinner walls than wood.
- A removable head stopper or cork test plug is assumed for Round 1 because it gives a reversible tuning variable.
- All prices, supplier availability, and exact clay data must be date-checked before buying.
- CAD mold release and split lines need confirmation in the actual CAD model before cutting production molds.
""",
    )
    write_text(
        ROOT / "mold-workflow.md",
        """
# Slip-Cast Mold Workflow

## Master Strategy

1. Generate the master from the workbook/CAD dimensions using X/Y/Z scale factors.
2. Add external handling tabs, pour/drain reservoir geometry, and mold keys outside the final fired acoustic envelope.
3. Seal and polish the master. Measure master X/Y/Z dimensions before making plaster.
4. Mark datums permanently: head end, foot end, top/embouchure side, X/Y/Z axes, split line, and build ID.

## Mold Strategy

- Use a two-piece mold for G4/A4/C5 if release is clean.
- Consider a three-piece or sectional mold for D4 because length, sag, and demold stress are the main risks.
- Mold center marks or shallow dimples for holes are useful; avoid fully molded tone holes in Round 1 unless release testing proves they are clean.
- Keep registration keys away from the bore axis, embouchure edge, hole centers, and seam-cleanup surfaces.
- Include a pour/drain reservoir that can be removed without touching the fired trim target.

## Casting Controls

Record these for every run:

- slip body and batch,
- mold dry weight and mold age,
- pour time, drain time, and drain orientation,
- room temperature and humidity,
- leather-hard demold time,
- wall thickness at sacrificial rim/coupon,
- dry, bisque, and glaze firing schedules,
- fired mass, length, bore Y/Z, OD Y/Z, and note frequencies.

## Tuning-Friendly Hole Strategy

1. Cast the body with molded center marks only.
2. Cut pilot holes at leather hard, about 85% of the shrink-compensated target diameter.
3. Dry and bisque.
4. Tune by opening holes with diamond tools. Stop before final glaze.
5. Wax resist all acoustic edges before glaze.

## Failure Modes To Watch

- Long D4 body sags or twists while drying.
- Bore ovalizes differently in Y and Z.
- Mold seam intrudes into the embouchure or tone-hole region.
- Wall thickness drifts with drain time enough to change hole chimney height.
- Glaze softens, rounds, or chokes the embouchure and tone-hole edges.
""",
    )
    write_text(
        ROOT / "doe-plan.md",
        f"""
# Round 1 DoE Plan

## Purpose

Round 1 is a screening study for a slip-cast transverse flute family. It should answer:

- What are the actual X/Y/Z shrink factors for each clay/process condition?
- Which clay body and wall target survive long flute geometry?
- Does a cylindrical bore or mild taper give better response after ceramic firing?
- Which embouchure geometry speaks cleanly before excessive hand correction?
- Do shrink and acoustic errors interpolate across D4, G4, and C5 well enough to build F4 and A4 in Round 2?

## Factors

| Factor | Levels |
| --- | --- |
| Key/scale | D4, G4, C5 screening; F4 and A4 family fill-ins |
| Clay body | Cone 6 stoneware, Cone 6 porcelain |
| Wall target | thin drain, nominal drain, thick drain |
| Bore profile | cylindrical, mild taper |
| Embouchure | standard oval, longer oval |
| Mold orientation | horizontal drain, vertical drain |

## Responses

- X/Y/Z shrink from bars, bore rings, and flute features.
- Bore roundness: fired ID Y vs ID Z.
- Wall thickness at head, middle, foot.
- Fundamental and six-finger scale cents error.
- Octave response, breath threshold, tone stability, and subjective playability.
- Crack/warp/sag/seam cleanup outcomes.

## Round 1 Matrix

See `data/doe-build-matrix.csv`. It contains {len(doe)} planned runs including screening and family fill-in builds.

## Round 2 Fit

Use `data/prototype-measurements.csv` and `data/shrinkage-fit.csv` to compute:

```text
shrink_axis = 1 - fired_axis / master_axis
round2_axis_scale_multiplier = target_fired_axis / measured_fired_axis
cents_error = 1200 * log2(measured_frequency / target_frequency)
```

If material or orientation creates a strong interaction, keep separate shrink factors by material/orientation rather than forcing a single global X/Y/Z value.
""",
    )
    write_text(
        ROOT / "assembly-manual.md",
        """
# Slip-Cast Transverse Flute Assembly Manual

## Tools

- CAD or OpenSCAD/SolidWorks for master geometry.
- 3D printer or machining route for sealed masters.
- Plaster mold supplies, cottle boards, scale, mixing bucket, release, clamps.
- Casting slip, deflocculant tools if mixing, and slip hydrometer if available.
- Needle tools, hole cutters, small round cutters, ribs, sponges, fettling knife.
- Calipers, bore gauges or pin gauges, scale, tuner, microphone, thermometer/hygrometer.
- Diamond needle files and fine diamond burrs.
- Wax resist, glaze, kiln access, and kiln-safe supports.

## Build Sequence

1. Pick a build row from `data/doe-build-matrix.csv`.
2. Confirm workbook shrink inputs and export the master dimensions for that run.
3. Print or machine the master, then sand, seal, and measure it.
4. Build the plaster mold with marked datums and registration keys.
5. Dry the mold completely enough for repeatable casting.
6. Pour slip, hold for the planned drain time, drain in the assigned orientation, and log the run.
7. Demold at leather hard and clean seams while preserving datums.
8. Cut embouchure and pilot tone holes undersize.
9. Dry slowly with support under the long body.
10. Bisque fire.
11. Measure X/Y/Z features, bore, mass, and first tuning.
12. Tune holes and embouchure in small steps using diamond tools.
13. Wax resist acoustic edges and glaze only after tuning is understood.
14. Final fire, then remeasure dimensions and tuning.
15. Enter data into `data/prototype-measurements.csv` and update `data/shrinkage-fit.csv`.

## Tuning Notes

- Enlarge an open tone hole to raise that note.
- Undercutting can raise pitch and improve response, but it changes the correction model.
- A head stopper gives a reversible global tuning lever; use it in Round 1 before committing to an integral ceramic head solution.
- Do not glaze the embouchure edge, tone-hole chimneys, bore interior, or stopper seating surface during the data rounds.

## Safety And Handling

- Fired ceramic edges and dust need care; use wet sanding or dust control.
- Long greenware bodies need full support while drying and moving.
- Label every prototype before it enters the kiln so the DoE data survives the shop day.
""",
    )
    write_text(
        ROOT / "drawing-brief.md",
        """
# Drawing Brief

## Required Views

- Family overview showing D4, F4, G4, A4, and C5 fired target lengths.
- Individual body plan view for each key with X-axis datum, embouchure, tone holes, bore ID, OD, and fired/master length notes.
- Section view at embouchure showing wall thickness, bore, hole edge, undercut zone, and stopper relationship.
- Section view through a tone hole showing chimney height and allowed tuning/undercut area.
- Mold stack view showing split line, registration keys, pour/drain direction, seam cleanup zone, and optional three-piece D4 strategy.
- Shrink coupon drawing with X/Y/Z labels and measurement flats.

## Critical Dimensions

| Dimension | Source | Tolerance Intent |
| --- | --- | --- |
| Fired sounding length | `data/fired-dimension-targets.csv` and workbook | Tuning critical |
| Embouchure center from head | workbook, initial 1.5 x bore ID | Response and tuning |
| Bore ID Y/Z | workbook and bore ring measurement | Tuning, response, shrink fit |
| Tone-hole stations X | `data/hole-schedule.csv` | Tuning critical; first-pass only |
| Tone-hole diameters | `data/hole-schedule.csv` | Cut undersize; tune after bisque |
| Wall thickness | DoE wall target and measured coupons | Durability, weight, hole chimney |
| Master X/Y/Z scale | shrink model | Process critical |

## Existing Drawings

- `drawings/family-overview.svg`
- `drawings/mold-stack.svg`
- `drawings/SCF-D4-01-body.svg`
- `drawings/SCF-F4-01-body.svg`
- `drawings/SCF-G4-01-body.svg`
- `drawings/SCF-A4-01-body.svg`
- `drawings/SCF-C5-01-body.svg`

These are SVG shop-review drawings. They are not a substitute for final CAD mold drawings with draft and release analysis.
""",
    )
    write_text(
        ROOT / "visual-bom-brief.md",
        """
# Visual BOM Brief

Create an image-forward BOM plate in Tony's Ashiko BOM style:

- Header: Slip-Cast Transverse Flute Family, quote date, material status, and Round 1 / Round 2 label.
- Hero image: family fan of the five fired target flutes or a clean CAD render.
- Table rows grouped by CAD/master, mold, ceramic material, tuning tools, validation tools, and finishing.
- Include thumbnails for: master, plaster mold halves, casting slip, shrink bars, bore rings, diamond files, tuner/mic, cork/stopper kit.
- Add callouts showing X/Y/Z shrink axes and where measurements are taken.
- Mark generated/CAD imagery as placeholders until replaced with shop photos or supplier images.

Important: the visual BOM should communicate process and parts, not invent unverified dimensions. Pull all numbers from the workbook and CSVs.
""",
    )
    write_text(
        ROOT / "supplier-rfq.md",
        """
# Supplier RFQ Starter

Subject: RFQ - slip-cast ceramic flute prototype materials and master/mold support

Hello,

I am prototyping a family of slip-cast ceramic transverse flutes and need materials or fabrication support with measured shrinkage and repeatability data.

Please quote the following where available:

- Cone 6 stoneware casting slip with shrinkage, absorption, and firing schedule data.
- Cone 6 porcelain casting slip with shrinkage, absorption, and firing schedule data.
- Pottery plaster suitable for slip-casting molds.
- Optional high-resolution master printing or machining for long cylindrical flute masters up to about 29 in master length.

Please include:

- unit price and minimum order,
- current availability and lead time,
- shipping or local pickup options,
- technical data sheets,
- recommended mold/drying/firing notes,
- any substitutions you recommend for thin-walled musical instrument bodies.

The prototypes will be measured for X/Y/Z shrinkage, bore roundness, wall thickness, and acoustic tuning after firing.

Thank you,

Tony
""",
    )
    write_text(
        ROOT / "wolfram-starter.wl",
        """
(* Slip-Cast Transverse Flute Family - Wolfram starter *)

a4 = 440;
cIn = 13552;
freq[midi_] := a4*2^((midi - 69)/12);
acousticLength[f_] := cIn/(2*f);
endCorrection[bore_] := 0.6*bore;
soundingLength[midi_, bore_] := acousticLength[freq[midi]] - endCorrection[bore];
holeDistanceFromFoot[midiFund_, interval_, bore_] :=
  acousticLength[freq[midiFund]] * freq[midiFund]/freq[midiFund + interval];
centsError[measured_, target_] := 1200*Log2[measured/target];
masterDim[fired_, shrink_] := fired/(1 - shrink);
observedShrink[master_, fired_] := 1 - fired/master;

family = {
  <|"ID" -> "SCF-D4-01", "MIDI" -> 62, "Bore" -> .748|>,
  <|"ID" -> "SCF-F4-01", "MIDI" -> 65, "Bore" -> .669|>,
  <|"ID" -> "SCF-G4-01", "MIDI" -> 67, "Bore" -> .669|>,
  <|"ID" -> "SCF-A4-01", "MIDI" -> 69, "Bore" -> .591|>,
  <|"ID" -> "SCF-C5-01", "MIDI" -> 72, "Bore" -> .512|>
};

Dataset[
  family /. inst_Association :> Join[
    inst,
    <|
      "FreqHz" -> freq[inst["MIDI"]],
      "SoundingLengthIn" -> soundingLength[inst["MIDI"], inst["Bore"]],
      "MasterXAt12PctIn" -> masterDim[soundingLength[inst["MIDI"], inst["Bore"]], .12]
    |>
  ]
]

Manipulate[
 Plot[
  Evaluate@Table[Sin[n*Pi*x/soundingLength[midi, bore]], {n, 1, 3}],
  {x, 0, soundingLength[midi, bore]},
  PlotRange -> {-1, 1},
  PlotLabel -> Row[{"Standing wave sketch, MIDI ", midi, ", bore ", bore, " in"}]
 ],
 {{midi, 62}, 62, 72, 1},
 {{bore, .748}, .45, .85, .001}
]
""",
    )
    write_text(
        ROOT / "cad" / "slip_cast_transverse_flute_body.scad",
        """
// Slip-cast transverse flute body concept model.
// Units: inches. Convert to mm in slicer/CAD if needed.
// This is a geometry starter, not a final mold with draft analysis.

instrument_id = "SCF-G4-01";
fired_length = 17.786;
fired_bore = 0.669;
fired_wall = 0.130;
shrink_x = 0.12;
shrink_y = 0.12;
shrink_z = 0.12;

master_length = fired_length / (1 - shrink_x);
master_bore_y = fired_bore / (1 - shrink_y);
master_bore_z = fired_bore / (1 - shrink_z);
master_od_y = (fired_bore + 2*fired_wall) / (1 - shrink_y);
master_od_z = (fired_bore + 2*fired_wall) / (1 - shrink_z);

inch = 25.4;

module flute_outer() {
  scale([1, master_od_y/master_od_z, 1])
    rotate([0,90,0])
      cylinder(h=master_length*inch, d=master_od_z*inch, $fn=96);
}

module flute_bore() {
  scale([1, master_bore_y/master_bore_z, 1])
    translate([-0.01*inch,0,0])
      rotate([0,90,0])
        cylinder(h=(master_length+0.02)*inch, d=master_bore_z*inch, $fn=96);
}

difference() {
  flute_outer();
  flute_bore();
}
""",
    )
    write_text(
        ROOT / "cnc" / "master-fabrication-plan.md",
        """
# Master Fabrication Plan

The first practical route is sealed 3D printed masters rather than CNC-cut plaster molds. The CAD model should still keep named parameters so SolidWorks/OpenSCAD can drive later configurations.

## Master Requirements

- Dimensioned from `Slip-Cast-Transverse-Flute-Family.xlsx`.
- X/Y/Z scale factors applied before export.
- Surface sealed enough that plaster will not bond or pick up layer texture.
- Bore/core strategy documented: solid master for external mold only, removable core, or split master.
- Datums engraved or marked: head, foot, top, X/Y/Z, build ID.

## Pre-Mold Checklist

- Measure master overall X, OD Y, OD Z, embouchure station, and any pilot dimples.
- Confirm no undercuts for selected mold pull direction.
- Confirm pour/drain reservoir can be cut away outside acoustic final target.
- Photograph master with scale before mold making.
""",
    )


def main() -> None:
    family_rows = calc_family()
    hole_rows = calc_holes(family_rows)
    doe = doe_rows()

    write_csv(
        ROOT / "data" / "fired-dimension-targets.csv",
        design_table_rows(family_rows),
        [
            "instrument_id",
            "variant",
            "key",
            "midi",
            "fundamental_hz",
            "bore_id_fired_in",
            "wall_thickness_fired_in",
            "od_fired_in",
            "acoustic_length_in",
            "end_correction_total_in",
            "sounding_length_embouchure_to_foot_fired_in",
            "head_margin_fired_in",
            "foot_trim_band_fired_in",
            "pretrim_overall_length_fired_in",
            "embouchure_center_from_head_fired_in",
            "embouchure_x_length_fired_in",
            "embouchure_y_width_fired_in",
            "master_overall_length_x_in_initial",
            "master_bore_y_in_initial",
            "master_od_y_in_initial",
            "master_od_z_in_initial",
            "bore_profile",
            "clay_body_round_1",
            "status",
        ],
    )
    write_csv(
        ROOT / "data" / "hole-schedule.csv",
        hole_csv_rows(hole_rows),
        [
            "instrument_id",
            "key",
            "hole_no",
            "scale_degree_interval_semitones",
            "target_note",
            "target_frequency_hz",
            "fired_center_from_foot_in",
            "fired_center_from_head_in",
            "fired_hole_diameter_in",
            "leather_hard_pilot_cut_dia_in_85pct",
            "hole_to_bore_ratio",
            "round_1_note",
        ],
    )
    write_csv(ROOT / "data" / "doe-build-matrix.csv", doe, list(doe[0].keys()))
    write_csv(ROOT / "bom.csv", bom_rows(), list(bom_rows()[0].keys()))
    write_csv(ROOT / "sourcing.csv", sourcing_rows(), list(sourcing_rows()[0].keys()))
    write_csv(ROOT / "cut-list.csv", cut_list_rows(family_rows), list(cut_list_rows(family_rows)[0].keys()))
    write_csv(ROOT / "validation.csv", validation_rows(family_rows), list(validation_rows(family_rows)[0].keys()))
    write_csv(ROOT / "data" / "prototype-measurements.csv", measurement_template_rows(), list(measurement_template_rows()[0].keys()))
    write_csv(ROOT / "data" / "shrinkage-fit.csv", shrink_fit_rows(), list(shrink_fit_rows()[0].keys()))

    write_drawings(family_rows, hole_rows)
    write_markdown_docs(family_rows, doe)
    write_xlsx(ROOT / "Slip-Cast-Transverse-Flute-Family.xlsx", workbook_rows(family_rows, hole_rows, doe))


if __name__ == "__main__":
    main()
