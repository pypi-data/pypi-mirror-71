import easydev
import os
import tempfile
import subprocess
import sys
from sequana.pipelines_common import get_pipeline_location as getpath

sharedir = getpath('downsampling')


def test_standalone_subprocess():
    directory = tempfile.TemporaryDirectory()
    cmd = """sequana_pipelines_downsampling --input-directory {}
            --working-directory {} --force""".format(sharedir, directory.name)
    subprocess.call(cmd.split())


def test_standalone_script():
    directory = tempfile.TemporaryDirectory()
    import sequana_pipelines.downsampling.main as m
    sys.argv = ["test", "--input-directory", sharedir, 
            "--working-directory", directory.name, "--force"]
    m.main()


def test_full():

    with tempfile.TemporaryDirectory() as directory:
        wk = directory
        cmd = "sequana_pipelines_downsampling --input-directory {} "
        cmd += "--working-directory {}  --force"
        cmd = cmd.format(sharedir, wk)
        subprocess.call(cmd.split())
        stat = subprocess.call("sh downsampling.sh".split(), cwd=wk)

    with tempfile.TemporaryDirectory() as directory:
        wk = directory
        cmd = "sequana_pipelines_downsampling --input-directory {} "
        cmd += ' --input-pattern "*fasta"'
        cmd += " --working-directory {} --downsampling-method random_pct  "
        cmd += " --downsampling-input-format fasta --force"
        cmd = cmd.format(sharedir, wk)
        subprocess.call(cmd.split())
        stat = subprocess.call("sh downsampling.sh".split(), cwd=wk)


def test_version():
    cmd = "sequana_pipelines_downsampling --version"
    subprocess.call(cmd.split())

