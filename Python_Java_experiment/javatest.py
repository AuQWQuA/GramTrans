import concurrent.futures
from tqdm import tqdm
import tempfile
import subprocess
import sys
import os
import json
import argparse

def test_java_program(program):
    testcode = program['solution']

    with tempfile.TemporaryDirectory() as tmp_dir:
        java_file_path = os.path.join(tmp_dir, "Main.java")
        
        with open(java_file_path, 'w', encoding="utf-8") as tmp_file:
            tmp_file.write(testcode)

        try:
            compile_result = subprocess.run(['javac', java_file_path], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return False, program['task_id']

            run_result = subprocess.run(['java', '-cp', tmp_dir, "Main"], capture_output=True, text=True, timeout=10)
            return run_result.returncode == 0, program['task_id']
        except Exception:
            return False, program['task_id']



if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--filename", type=str, default="testjava.json")
    args = argparser.parse_args()
    filename = args.filename
    with open(filename, "r") as f:
        programs = [json.loads(line) for line in f]

    results = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(test_java_program, prog) for prog in programs]
        for f in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Testing"):
            results.append(f.result())

    indices = [int(id[5:]) for result, id in results if result]
    sorted_indices = sorted(indices)


    total = len(programs)
    success = len(sorted_indices)
    success_rate = success / total * 100
    print(round(success_rate, 2))