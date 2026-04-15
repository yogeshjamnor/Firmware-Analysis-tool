import subprocess

def run_cmd(cmd):
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    return result.stdout + result.stderr

def file_info(path):
    return run_cmd(["file", path])

def strings_dump(path):
    return run_cmd(["strings", path])

def readelf_header(path):
    return run_cmd(["readelf", "-d", path])