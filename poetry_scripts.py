import subprocess
import sys

project_init_file = 'pagexml/__init__.py'
citation_file = 'CITATION.cff'


def version(argv=None):
    if not argv:
        argv = sys.argv
    parameter = argv[1]
    result = subprocess.run(["poetry", "version", parameter], capture_output=True)
    stdout = result.stdout.decode().strip()
    print(stdout)
    print(result.stderr.decode().strip(), file=sys.stderr)
    new_version = stdout.split()[-1]

    with open(project_init_file) as f:
        lines = f.readlines()

    with open(project_init_file, 'w') as f:
        init_has_version = False
        for line in lines:
            if line.startswith('__version__'):
                init_has_version = True
                f.write(f"__version__ = '{new_version}'\n")
            else:
                f.write(line)
        if not init_has_version:
            f.write(f"__version__ = '{new_version}'\n")

    with open(citation_file) as f:
        citation = yaml.load(f, Loader=yaml.Loader)
    citation['version'] = new_version
    citation['date-released'] = datetime.datetime.now().strftime("%Y-%m-%d")
    with open(citation_file, 'w') as f:
        yaml.dump(citation)
