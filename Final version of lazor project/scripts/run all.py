import sys, subprocess, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOLVER = ROOT / "lazor_solver.py"
OUTDIR = ROOT / "out"
OUTDIR.mkdir(exist_ok=True)

def run_one(bff: pathlib.Path) -> int:
    out = OUTDIR / (bff.stem + ".sol")
    cmd = [sys.executable, str(SOLVER), "-i", str(bff), "-o", str(out), "--diagnose"]
    return subprocess.run(cmd, check=False).returncode

if __name__ == "__main__":
    # focus on official set for grading reproducibility
    bff_dir = ROOT / "examples" / "official"
    cases = sorted(bff_dir.glob("*.bff"))
    ok = 0
    for bff in cases:
        print(f"==> {bff}")
        code = run_one(bff)
        print("exit=", code)
        ok += (code == 0)
    print(f"passed {ok}/{len(cases)}")
