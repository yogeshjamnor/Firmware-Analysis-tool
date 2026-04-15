import subprocess
from pathlib import Path
from core.utils import get_base_path


def extract(file_path, output_dir, log_callback=None):
    base = get_base_path()

    file_path = Path(file_path).resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if file_path.name == "payload.bin":
        tool = base / "bin" / "payload-dumper-go"
        cmd = [str(tool), str(file_path), "-o", str(output_dir)]

    elif file_path.name == "super.img":
        tool = base / "bin" / "lpunpack"
        cmd = [str(tool), str(file_path), str(output_dir)]

    else:
        raise Exception("Unsupported file type")

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=0,
        cwd=str(output_dir)
    )

    # Read in chunks and normalize carriage-return progress
    while True:
        chunk = process.stdout.read(1024)
        if not chunk:
            break

        text = chunk.replace('\r', '\n')

        for line in text.split('\n'):
            clean = line.strip()
            if clean and log_callback:
                log_callback(clean)

    process.wait()

    if process.returncode != 0:
        raise Exception("Extraction failed")