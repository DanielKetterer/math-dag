# Calibration stats

## Rule compliance per pass

| Pass | Nodes covered | Edges | Rule violations | New (outside) targets | Nodes with 2+ routes |
|---|---|---|---|---|---|
| A | 20/20 | 56 | 0 | 2 | 1 |
| B | 20/20 | 55 | 0 | 1 | 1 |
| C | 20/20 | 58 | 0 | 0 | 1 |
| D | 20/20 | 56 | 0 | 1 | 0 |

## Agreement among the voting passes (A, B, C)

- Distinct edges proposed by any voter: 65
- Proposed by 3 of 3: 47 (72%)
- Proposed by 2 of 3: 6 (9%)
- Proposed by 1 of 3: 12 (18%)

Pairwise overlap (Jaccard on all edges):

- A vs B: 0.88
- A vs C: 0.73
- A vs D: 0.71
- B vs C: 0.80
- B vs D: 0.69
- C vs D: 0.70

- D against the voters' majority: recovers 85% of majority edges; 80% of D's edges are majority edges

- Unanimous edges whose relation type also matches across voters: 36/47
- Nodes where voters disagree on the number of routes: 0 []

## Rule violations

- A: none
- B: none
- C: none
- D: none

Review sheet: 72 distinct edges.
