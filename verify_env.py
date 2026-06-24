import importlib, shutil, sys

def verify_env() -> dict[str, bool]:
    """Verify that the required tools are available in the environment."""
    out = {}
    for m in ["numpy", "scipy", "matplotlib", "skrf", "serdespy", "cocotb"]:
        try:
            importlib.import_module(m); out[m] = True
            
        except Exception:
            out[m] = False
    for exe in ["verilator", "iverilog", "make", "git"]:
        out[exe] = shutil.which(exe) is not None
    
    return out

if __name__ == "__main__":
    r = verify_env()
    for k, v in r.items():
        print(f"{'OK ' if v else 'XX '}")
    sys.exit(0 if all(r.values()) else 1)