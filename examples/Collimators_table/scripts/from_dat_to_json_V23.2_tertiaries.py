import json
import os

# === Input and output file paths ===
input_file_path = "/home/dogibellieri/fcc_ee_pywit_model/examples/Collimators_table/dat_files/FCCee_z_v23_coll_table_TCTs.dat"
output_file_path = input_file_path.replace("dat_files", "json_files").replace(".dat", ".json")

# === Read the input file ===
with open(input_file_path, "r") as file:
    lines = file.readlines()

# === Prepare the JSON structure ===
collimator_data = {}

for line in lines[1:]:  # Skip header
    parts = line.strip().split()  # Split on any whitespace

    if len(parts) < 7:
        continue  # Skip malformed lines

    try:
        name = parts[0]
        plane = parts[2]
        s = float(parts[3])
        material_raw = parts[4].lower()
        length = float(parts[5])
        n_sigma = float(parts[6])
    except (ValueError, IndexError) as e:
        print(f"Skipping line due to error: {e}")
        continue

    # Normalize material names
    material_map = {
        'mogr': 'moc',
        'mo': 'Mo',
        'w': 'W',
        'inermet180': 'inermet180'
    }
    material = material_map.get(material_raw, material_raw)

    angle = 0.0 if plane.upper() == 'H' else 1.57079633

    # Build JSON entry
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

# === Ensure output folder exists ===
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# === Save JSON file ===
with open(output_file_path, "w") as json_file:
    json.dump(collimator_data, json_file, indent=2)

print(f"✅ JSON saved to {output_file_path} with {len(collimator_data)} entries")


