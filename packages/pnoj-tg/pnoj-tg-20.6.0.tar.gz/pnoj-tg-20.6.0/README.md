# pnoj-tg

This is a testcase generator for the PNOJ Online Judge.

It is recommended to install pnoj-tg using the PIP package available on PYPI.

# Installation

```bash
pip install pnoj-tg
```

# Usage

First create a file named `config.yaml`. Change the content to suit your needs.

`config.yaml`:
```yaml
version: v1
generator:
  input: ["python3", "generator.py"] # command to execute the input generator
  output: ["python3", "solution.py"] # command to execute the solution
testcase:
  batch:
  - name: batch1 # batch name
    points: 100 # points
    testcase:
      name: t-{0} # testcase name, "{0}" is replaced with the testcase number
      num: 10 # number of testcases
  - name: example
    points: 0
    testcase:
      name: sample
      num: 1
```

Then create two programs `generator.py` and `solution.py`.
`generator.py` should generate a random case.
`solution.py` should be the reference solution to the problem you are creating testdata for.

Then run:
```bash
pnoj-tg config.yaml
```

## Build Instructions
```bash
git clone https://github.com/pnoj/pnoj-tg.git # clones the repository
cd scrapec
pip install . # install pnoj-tg
```
