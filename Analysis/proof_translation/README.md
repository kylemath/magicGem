# Proof translation page, run locally

The page shows each step of Paper B's Theorem 3.7(a) in Lean, TeX, Python, English and a demo.
Served by `server.py`, its Lean panel is checked by Lean on this computer and its Python runs in python3.

One-time setup (downloads the prebuilt Mathlib cache, a few GB):

    curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain none
    cd ../lean_upper_bound && ~/.elan/bin/lake exe cache get

Then:

    python3 server.py        # open http://127.0.0.1:8765

Opened as a plain file or as the published artifact, the page still works, with Python running in the
browser (Brython) and Lean checks sent to the Lean web editor. `source/` holds the generator
(`python3 source/build.py` after editing `steps.py` or `pyruns.py`; it expects the Lean files in `../lean_upper_bound`).
