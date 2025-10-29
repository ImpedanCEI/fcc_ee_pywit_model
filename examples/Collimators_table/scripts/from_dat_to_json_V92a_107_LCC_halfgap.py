import json
import os

# === Input and output file paths ===
input_file_path = "/home/dogibellieri/fcc_ee_pywit_model/examples/Collimators_table/dat_files/FCCee_z_V92a_107_LCC_collimator_table_halfgap.dat"
output_file_path = input_file_path.replace("dat_files", "json_files").replace(".dat", ".json")

# === Read the input file ===
with open(input_file_path, "r") as file:
    lines = file.readlines()

collimator_data = {}

for line in lines[1:]:  # Skip header
    parts = line.strip().split()
    if len(parts) < 8:
        continue

    try:
        name = parts[1]
        plane = parts[3]
        s = float(parts[4])
        material_raw = parts[5].lower()
        length = float(parts[6])
        n_sigma = float(parts[7])
    except (ValueError, IndexError) as e:
        print(f"Skipping line due to error: {e}")
        continue

    # Extract half-gaps (positions 8 and 9 in the file)
    try:
        halfgap_x = float(parts[8])
        halfgap_y = float(parts[9])
    except (ValueError, IndexError):
        halfgap_x = None
        halfgap_y = None

    # Normalize material names
    material_map = {
        'mogr': 'moc',
        'mo': 'Mo',
        'w': 'W',
        'inermet180': 'inermet180'
    }
    material = material_map.get(material_raw, material_raw)

    is_horizontal = plane.upper() == 'H'
    angle = 0.0 if is_horizontal else 1.57079633
    halfgap = halfgap_x if is_horizontal else halfgap_y

    collimator_data[name] = {
        "s": s,
        "angle": angle,
        "layers": [{"material": material, "thickness": 10}],
        "length": length,
        "tilt_1": 0.0,
        "tilt_2": 0.0,
        "halfgap_dependent_hom_files": [],
        "halfgap": halfgap*1e-3  
    }

# === Save the JSON file ===
with open(output_file_path, "w") as json_file:
    json.dump(collimator_data, json_file, indent=2)

output_file_path  # Display path to the saved file
