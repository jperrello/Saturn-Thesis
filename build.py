import subprocess, sys, os

MIKTEX = os.path.expanduser("~/AppData/Local/Programs/MiKTeX/miktex/bin/x64")
env = {**os.environ, "PATH": MIKTEX + os.pathsep + os.environ.get("PATH", "")}

def build():
    for cmd in [
        ["pdflatex", "-interaction=nonstopmode", "thesis.tex"],
        ["bibtex", "thesis"],
        ["pdflatex", "-interaction=nonstopmode", "thesis.tex"],
        ["pdflatex", "-interaction=nonstopmode", "thesis.tex"],
    ]:
        r = subprocess.run(cmd, env=env)
        if r.returncode != 0 and cmd[0] == "pdflatex":
            sys.exit(1)
    print("Done: thesis.pdf")

if __name__ == "__main__":
    build()
