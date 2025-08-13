from pathlib import Path
from scripts.generate_instructions import main as gen_main
from scripts.validate import main as val_main

def test_validate_and_generate(tmp_path: Path, monkeypatch):
    # Run validator and generator in-place (repo has fixtures)
    assert val_main() == 0
    assert gen_main() == 0
    runtime = Path('.github/copilot/runtime')
    assert (runtime / 'reviewer.md').exists()
    assert (runtime / 'coder.md').exists()
