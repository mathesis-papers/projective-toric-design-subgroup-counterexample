# Identity-containing counterexamples to Conjecture 4.9

Iosue–Mooney–Ehrenberg–Gorshkov, Section 4.3, p. 15, arXiv:2311.13479v3: certificates and extensions of Abdukhalikov's (2014) construction.

Haobo Ma (ChronoAI Pte Ltd, Singapore) and Wenlin Zhang (National University of Singapore; ChronoAI Pte Ltd, Singapore).

Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0; cc-by-4.0).

## Statement

The note gives a 729-point identity-containing counterexample in dimension 27 to Conjecture 4.9, Section 4.3, p. 15 of Iosue, Mooney, Ehrenberg and Gorshkov, arXiv:2311.13479v3. The MUB overlap condition is Eq. (25), Section 4.2, Theorem 4.4, p. 13. The phases form a uniformly weighted projective toric two-design but are not additively closed, and no translate is a subgroup. The classical nonadditive-spread formulas of Abdukhalikov (2014) already imply such a counterexample; the note proves that implication and gives a separate symmetric-matrix certificate in Kantor's (2012) formulation.

For Conjecture 4.7, the forward implication of Conjecture 4.8, the unnumbered dimension-six nonexistence conjecture immediately after Conjecture 4.8, and the minimal-design group question in Section 5, the translation results have the coverage label "literal statement only; translation-invariant version not covered". The examples in dimensions six and two are subgroup cosets. They do not settle the translation-invariant questions or the dimension-six MUB existence problem.

## Files

- `note.tex`: complete mathematical statement, focused proof, displayed matrix certificate and bibliography.
- `note.pdf`: typeset note.
- `matrices.json`: the 27 symmetric matrices over the field of three elements, in the displayed order.
- `verify.py`: Python 3 standard-library exact finite checker.
- `verification.json`: the expected checker output.
- `verify_siblings.py` and `sibling-verification.json`: exact rational translations, cyclic certificates and a cyclotomic overlap obstruction.
- `verify_classical.py` and `classical-verification.json`: the 27 trace-self-adjoint spread maps in the classical field formulas and their nonclosure witness.
- `metadata.json`: bibliographic metadata and the covered problem identifier.

## Rebuild

From the extracted source directory, use Tectonic 0.17.0:

```sh
tectonic --untrusted note.tex
python3 verify.py > calculated.json
diff -u verification.json calculated.json
python3 verify_siblings.py > calculated-siblings.json
diff -u sibling-verification.json calculated-siblings.json
python3 verify_classical.py > calculated-classical.json
diff -u classical-verification.json calculated-classical.json
```

Alternatively, run `pdflatex -interaction=nonstopmode -halt-on-error note.tex` twice. The bibliography is contained in `note.tex`, so BibTeX is not required. The PDF requires only standard LaTeX packages listed in the source.

## Coverage

The written proof treats the spread construction over every odd prime field. The finite checker establishes the 27-matrix certificate, distinctness, anchoring, identity, nonclosure, all second-moment conditions and all distinct-point overlaps for the explicit dimension-27 design. It uses integer arithmetic, not numerical approximations to complex phases.

The pinned Lean declaration `D5.S3.Quantum.Measurements.ProjectiveToricDesignNonGroup.result` proves the negation of the universal identity-containing subgroup assertion using this matrix set:

https://github.com/the-omega-institute/trureturing/blob/f7ba557ae2a5d2c3a3a519e0713d65ac86af2973/D5/S3/Quantum/Measurements/ProjectiveToricDesignNonGroup.lean

The general spread lemma, no-translate conclusion, classical field-formula implication, translation corollaries, affine-plane construction and Hadamard connection have written proofs. The new finite checkers establish only their specified finite premises. The converse in Conjecture 4.8, dimension-six MUB existence, minimal designs up to translation and the higher-strength minimal-size questions are not settled.
