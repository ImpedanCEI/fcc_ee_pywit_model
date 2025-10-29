import json
import re

# === Specify your input file path here ===
input_file_path = "/home/dogibellieri/fcc_ee_pywit_model/examples/Collimators_table/dat_files/FCCee_z_collimators_V23_tridodo_572_colloptics_updated.dat"

# === Open and read the input file ===
with open(input_file_path, "r") as file:
    lines = file.readlines()

# === Prepare the JSON structure ===
collimator_data = {}

for line in lines[1:]:  # Skip header
    parts = re.split(r'\s{2,}', line.strip())
    if len(parts) < 13:
        continue  # Not enough fields

    try:
        name = parts[0]
        plane = parts[2]
        s = float(parts[4])
        length = float(parts[5])
        n_sigma = float(parts[6])
        material_raw = parts[10].lower()
    except (ValueError, IndexError):
        continue  # Skip malformed rows

    # Normalize material names
    material_map = {
        'mogr': 'moc',
        'mo': 'Mo',
        'w': 'W',
        'inermet180': 'inermet180'
    }
    material = material_map.get(material_raw, material_raw)

    angle = 0.0 if plane.upper() == 'H' else 1.57079633

    collimator_data[name] = {
        "s": s,
        "angle": angle,
        "layers": [{"material": material, "thickness": 10}],
        "n_sigma": n_sigma,
        "length": length,
        "tilt_1": 0.0,
        "tilt_2": 0.0,
        "halfgap_dependent_hom_files": []
    }

# === Save JSON to a file ===
output_path = "/home/dogibellieri/fcc_ee_pywit_model/examples/Collimators_table/json_files/FCCee_z_collimators_V23_tridodo_572_colloptics_updated.json"
with open(output_path, "w") as json_file:
    json.dump(collimator_data, json_file, indent=2)

print(f"✅ JSON saved to {output_path} with {len(collimator_data)} entries")
