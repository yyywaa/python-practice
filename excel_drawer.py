import pandas as pd
import os

data = {}
final_list = []

input_dir = r'/root/step1_inputs'
if not os.path.exists(input_dir):
    print(f"Error: Directory {input_dir} does not exist.")
else:
    files = os.listdir(input_dir)
    
    for file in files:
        if file.endswith(".log") and file.startswith("step1_"):
            file_path = os.path.join(input_dir, file)

            clean_name = os.path.splitext(file)[0] 
            parts = clean_name.split("_")
            if len(parts) >= 3:
                p_part = parts[1]
                z_part = parts[2]

                file_key = (p_part, z_part) 
                
                try:
                    with open(file_path, 'r') as f:

                        for line in f:
                            if 'SCF Done' in line:
                                segments = line.strip().split()
                                try:
                                    eq_index = segments.index('=')
                                    energy_num = float(segments[eq_index + 1])
                                    data[file_key] = energy_num
                                except (ValueError, IndexError):
                                    continue
                except Exception as e:
                    print(f"Error reading {file}: {e}")
    for psi in range(0, 360, 10):
        target_p = "p" + str(psi)

        energies_at_p = []
        for (p_key, z_key), energy in data.items():
            if p_key == target_p:
                energies_at_p.append(energy)
        
        if energies_at_p:
            min_e = min(energies_at_p)
            final_list.append({'Psi': psi, 'Min_Energy': min_e})
        else:
            print(f"Warning: No data found for {target_p}")

    if final_list:
        df = pd.DataFrame(final_list)
        df = df.sort_values(by='Psi')
        print(df.head())
        df.to_excel('E-psi.xlsx', index=False)
        print("Done.")
    else:
        print("No valid data extracted.")



         
