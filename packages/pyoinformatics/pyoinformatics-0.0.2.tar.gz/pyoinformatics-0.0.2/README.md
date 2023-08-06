# pyoinformatics 🐍
![CI/CD](https://github.com/Wytamma/pyoinformatics/workflows/CI/CD/badge.svg)
[![codecov](https://codecov.io/gh/Wytamma/pyoinformatics/branch/master/graph/badge.svg)](https://codecov.io/gh/Wytamma/pyoinformatics)
[![image](https://img.shields.io/github/license/wytamma/pyoinformatics.svg)](https://img.shields.io/github/license/wytamma/pyoinformatics)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://img.shields.io/badge/code%20style-black-000000.svg)
[![PyPI](https://img.shields.io/pypi/v/pyoinformatics)](https://pypi.org/project/pyoinformatics/)


## Examples 

### Find the reverse complement of all the sequences in a file:
```python
with open('out.fasta', 'w') as f:
  for seq in Bio.read_fasta('in.fasta'):
    f.writelines(seq.reverse_complement().to_fasta())
```

### Count the number of occurrences of 'ATG' in seq1
```python
seq1.count('ATG')
```

### Count the number of occurrences of 'ATG' in seq1 that differ by <= 1 base.
```python
seq1.count('ATG', 1)
```

### Find the number of occurrences of 'ATG' or 'AAG' in seq1
```python
len(seq1.find('A[AT]G'))
```

### Find the average position of all occurrences of 'ATG' in a fasta file
```python
from statistics import mean
for seq in Bio.read_fasta('in.fasta'):
  print(mean(seq.find('ATG')))
```

### ASCI plot the relative nt counts for all the sequences in a file
```python
for seq in Bio.read_fasta('in.fasta'):
  counts = seq.counts
  print(f">{seq.id}")
  for nt in sorted(counts.keys()):
    bar = int((counts[nt]/len(seq))*100)
    print(f"{nt}: {'◊' * bar}")

>HSBGPG Human gene for bone gla protein (BGP)
A: ◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊
C: ◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊
G: ◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊
T: ◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊
>HSGLTH1 Human theta 1-globin gene
A: ◊◊◊◊◊◊◊◊◊◊◊◊◊◊
C: ◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊
G: ◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊
T: ◊◊◊◊◊◊◊◊◊◊◊◊◊◊◊
```