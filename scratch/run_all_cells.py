import json
import io
import sys
import contextlib
import traceback

sys.stdout.reconfigure(encoding='utf-8')

nb_path = 'hypothesis_testing_and_visualization.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells to process: {len(nb['cells'])}")

g_vars = {}
exec_count = 1

for idx, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    
    code = ''.join(cell['source'])
    f_out = io.StringIO()
    f_err = io.StringIO()
    
    print(f"Executing Code Cell {idx} (count={exec_count})...", end=' ')
    try:
        with contextlib.redirect_stdout(f_out), contextlib.redirect_stderr(f_err):
            exec(code, g_vars)
        out_text = f_out.getvalue()
        err_text = f_err.getvalue()
        
        outputs = []
        if out_text:
            outputs.append({
                'name': 'stdout',
                'output_type': 'stream',
                'text': out_text.splitlines(keepends=True)
            })
        if err_text:
            outputs.append({
                'name': 'stderr',
                'output_type': 'stream',
                'text': err_text.splitlines(keepends=True)
            })
            
        cell['outputs'] = outputs
        cell['execution_count'] = exec_count
        exec_count += 1
        print(f"SUCCESS! (stdout lines: {len(out_text.splitlines())})")
    except Exception as e:
        print(f"FAILED with error: {e}")
        traceback.print_exc()
        sys.exit(1)

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("\n" + "=" * 60)
print(f"All {exec_count - 1} code cells executed successfully with 0 errors!")
print("Notebook saved with updated outputs and execution counts.")
print("=" * 60)
