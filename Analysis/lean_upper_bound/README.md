# Lean check of Theorem 3.7(a), Paper B

One file per proof step of the upper bound k*(n) <= sqrt(pi e (n-1) log(n^4/4)),
matching the step ids of the "Proof Translation" page. Every file compiles with
Lean 4.35.0 and the Mathlib revision pinned in `lake-manifest.json`, with no
`sorry`, `axiom` or `native_decide`.

    lake exe cache get && lake build

Not formalized: combining S2a and S2b into ||gamma||_1 <= n^4/4, turning S3b-S3e
into the pointwise bound on log|P|, and integrating that bound in S3g.
