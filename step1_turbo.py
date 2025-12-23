import numpy as np
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

class GaussianTaskHandler:
    def __init__(self, output_dir="step1_inputs"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.n_procs = 6    
        self.mem = "4GB"    
        self.functional = "wB97XD"  
        self.basis_water = "def2SVP" 
        self.basis_gold = "LANL2DZ"      
        self.au_lattice_const = 4.078 
        self.plate_gap = 6.0 

    def generate_gold_plate_3x3(self):
        coords = []
        d = self.au_lattice_const
        step = d / np.sqrt(2)
        indices = range(-1, 2)
        z_bottom = -self.plate_gap / 2.0
        for i in indices:
            for j in indices:
                coords.append(["Au", i*step, j*step, z_bottom])
        z_top = self.plate_gap / 2.0
        for i in indices:
            for j in indices:
                coords.append(["Au", i*step, j*step, z_top])
        return coords

    def get_water_coords(self, angle_deg, z_offset):
        coordO = np.array([0.000000, 0.000000, 0.000000])
        coordH1 = np.array([0.000000, 0.759354, -0.595870])
        coordH2 = np.array([0.000000, 0.759354, 0.595870])
        psi = 2 * np.pi * angle_deg / 360
        c = np.cos(psi)
        s = np.sin(psi)
        rotate_matrix = np.array([[1, 0, 0], [0, c, s], [0, -s, c]])
        rotatedH1 = np.dot(rotate_matrix, coordH1)
        rotatedH2 = np.dot(rotate_matrix, coordH2)
        shift = np.array([0.0, 0.0, z_offset])
        final_coords = [coordO + shift, rotatedH1 + shift, rotatedH2 + shift]
        atom_types = ["O", "H", "H"]
        return [[at] + co.tolist() for at, co in zip(atom_types, final_coords)]

    def write_gjf(self, angle, z_idx, z_val, au_coords, water_coords):
        filename = os.path.join(self.output_dir, f"step1_p{angle}_z{z_idx}.gjf")
        with open(filename, 'wb') as f:
            def w(t): f.write(t.encode('utf-8'))
            w(f"%nprocshared={self.n_procs}\n%mem={self.mem}\n%chk=step1_p{angle}_z{z_idx}.chk\n")
            w(f"#p {self.functional}/gen pseudo=read nosym\n\nTitle\n\n0 1\n")
            for a in au_coords: w(f"{a[0]:<2} {a[1]:12.6f} {a[2]:12.6f} {a[3]:12.6f}\n")
            for a in water_coords: w(f"{a[0]:<2} {a[1]:12.6f} {a[2]:12.6f} {a[3]:12.6f}\n")
            w(f"\nH O 0\n{self.basis_water}\n****\nAu 0\n{self.basis_gold}\n****\n\nAu 0\n{self.basis_gold}\n\n")

    def run_generation(self):
        print("--- 正在生成文件 ---")
        au_coords = self.generate_gold_plate_3x3()
        scan_range_angle = range(0, 360, 10)
        scan_range_z = np.linspace(-0.6, 0.6, 7)
        files_to_run = []
        for angle in scan_range_angle:
            for z_idx, z_val in enumerate(scan_range_z):
                w_coords = self.get_water_coords(angle, z_val)
                self.write_gjf(angle, z_idx, z_val, au_coords, w_coords)
                files_to_run.append(f"step1_p{angle}_z{z_idx}.gjf")
        self.create_python_runner(files_to_run)
        print(f"--- 成功! 生成了 {len(files_to_run)} 个任务 ---")

    def create_python_runner(self, files):
        with open("turbo_run.py", 'w') as f:
            f.write(f"import os, subprocess\nfrom concurrent.futures import ThreadPoolExecutor\n")
            f.write(f"def run_g(file):\n  inp=os.path.join('step1_inputs', file)\n  out=inp.replace('.gjf', '.log')\n")
            f.write(f"  if os.path.exists(out): return 'skip'\n")
            f.write(f"  subprocess.run(f'g16 {{inp}} > {{out}} 2>&1', shell=True)\n  return 'done'\n")
            f.write(f"if __name__ == '__main__':\n  with ThreadPoolExecutor(max_workers=4) as e: list(e.map(run_g, {files}))\n")

if __name__ == "__main__":
    GaussianTaskHandler().run_generation()
