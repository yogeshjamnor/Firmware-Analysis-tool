import subprocess
from pathlib import Path

def mount_image(img_path, mount_dir):
    img_path = str(Path(img_path).resolve())
    mount_dir = str(Path(mount_dir).resolve())

    Path(mount_dir).mkdir(parents=True, exist_ok=True)

    subprocess.run(
        ["sudo", "mount", "-o", "loop,ro", img_path, mount_dir],
        check=True
    )


def create_zip(mount_dir, output_zip):
    subprocess.run(
        ["sudo", "zip", "-r", output_zip, "."],
        cwd=mount_dir,
        check=True
    )


def unmount(mount_dir):
    subprocess.run(
        ["sudo", "umount", mount_dir],
        check=True
    )