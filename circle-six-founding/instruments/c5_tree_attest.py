#!/usr/bin/env python3
"""c5_tree_attest.py — the completeness instrument.  QUARANTINED (norm 16)
   until the seat that did not write it has bitten it.

WHY THIS EXISTS
  Circle Five's builder cannot reach any repository (its architecture, not
  a choice), so every byte of the record it sees arrives by ferry through
  the prover.  The prover filed that against itself: "I am the builder's
  git remote -v."  Byte-exact files at pins prove every file that ARRIVES
  is authentic.  They prove nothing about a file the sender chose NOT to
  send, and a disclosure list is the sender's word about its own omissions.

THE MECHANISM, AND WHY IT IS NOT CIRCULAR
  A git tree hash is a Merkle root.  So the sender emits (a) the commit's
  tree root and (b) every (mode, blob-sha, path) under it; the receiver
  RECOMPUTES the root from that listing.  Drop one entry to hide a file and
  the recomputed root no longer matches the published one.  The receiver
  needs no repository access to run the check — only sha1 and this script.
  The published root is independently checkable against the forge by anyone
  who does have reach, which is the courier.

  So an omission stops being something the receiver must trust the sender to
  disclose, and becomes something the receiver measures.

CONTRACT
  emit   <commit>            -> a listing: root line, then one line per blob
  verify <listing>           -> exit 0 iff the listing recomputes to its own
                                stated root; exit 1 naming the mismatch
  Exit codes are the whole output contract.  Read them directly, never
  through a pipe (SR30, four occurrences across three seats).

FALSIFIERS THIS MUST FAIL ON, and does (see BITE-LOG below the code)
  - any blob line removed        -> root mismatch, exit 1
  - any blob sha altered         -> root mismatch, exit 1
  - any path renamed            -> root mismatch, exit 1
  - the stated root altered     -> root mismatch, exit 1
"""
import hashlib, subprocess, sys, collections

def sha1_obj(kind: bytes, payload: bytes) -> bytes:
    return hashlib.sha1(kind + b" " + str(len(payload)).encode() + b"\0" + payload).digest()

def build_root(entries):
    """entries: list of (mode:str, sha_hex:str, path:str) for BLOBS only.
       Rebuilds every tree object bottom-up and returns the root sha1 hex.

       Git sorts tree entries by raw name bytes, EXCEPT that a directory
       sorts as if its name carried a trailing '/'.  Getting that wrong
       produces a plausible-looking root that is simply not git's, which is
       how this instrument failed its first self-test."""
    children = collections.defaultdict(dict)          # dir -> name -> (mode, binsha)
    dirs = {""}
    for mode, sha, path in entries:
        parts = path.split("/")
        for i in range(1, len(parts)):
            dirs.add("/".join(parts[:i]))
        children["/".join(parts[:-1])][parts[-1]] = (mode, bytes.fromhex(sha))
    # deepest first, so a subtree's sha exists before its parent needs it
    for d in sorted(dirs, key=lambda p: p.count("/") if p else -1, reverse=True):
        def sortkey(name):
            mode, _ = children[d][name]
            return (name + "/").encode() if mode == "40000" else name.encode()
        payload = b""
        for name in sorted(children[d].keys(), key=sortkey):
            mode, binsha = children[d][name]
            payload += mode.encode() + b" " + name.encode() + b"\0" + binsha
        binsha = sha1_obj(b"tree", payload)
        if d == "":
            return binsha.hex()
        parent, _, base = d.rpartition("/")
        children[parent][base] = ("40000", binsha)
    return None

def emit(commit):
    root = subprocess.run(["git", "rev-parse", commit + "^{tree}"],
                          capture_output=True, text=True, check=True).stdout.strip()
    out = subprocess.run(["git", "ls-tree", "-r", commit],
                         capture_output=True, text=True, check=True).stdout
    entries = []
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        mode, kind, sha = meta.split()
        if kind == "blob":
            entries.append((mode, sha, path))
    print(f"root {root}")
    print(f"blobs {len(entries)}")
    for mode, sha, path in sorted(entries, key=lambda e: e[2]):
        print(f"{mode} {sha} {path}")

def verify(listing_path):
    root = None; stated = None; entries = []
    for line in open(listing_path):
        line = line.rstrip("\n")
        if line.startswith("root "):   root = line.split()[1]; continue
        if line.startswith("blobs "):  stated = int(line.split()[1]); continue
        if not line.strip():           continue
        mode, sha, path = line.split(" ", 2)
        entries.append((mode, sha, path))
    if root is None:
        print("MALFORMED: no root line"); return 1
    if stated is not None and stated != len(entries):
        print(f"COUNT MISMATCH: header says {stated} blobs, listing carries {len(entries)}")
        return 1
    got = build_root(entries)
    if got == root:
        print(f"COMPLETE: {len(entries)} blobs recompute to the stated root {root}")
        return 0
    print(f"INCOMPLETE OR ALTERED: listing recomputes to {got}, stated root is {root}")
    return 1

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "emit":   emit(sys.argv[2]); sys.exit(0)
    if len(sys.argv) == 3 and sys.argv[1] == "verify": sys.exit(verify(sys.argv[2]))
    print(__doc__); sys.exit(2)

# ---------------------------------------------------------------- BITE-LOG
# Norm 16: a new instrument's first output is quarantined until it has failed
# on a planted defect and passed on a clean tree.  Run by the author, in the
# tree the-workshop-circle-five at commit 6f7d8d5, exits taken DIRECTLY:
#
#   clean listing (14 blobs)                                      exit 0
#   one blob line removed, count header corrected to match         exit 1
#   one blob line removed, count header left stale                 exit 1
#   one blob sha altered by a single hex digit                     exit 1
#   one path renamed, every sha left intact                        exit 1
#   the stated root altered by a single hex digit                  exit 1
#
# It also failed its OWN first self-test and that is recorded rather than
# quietly fixed: the first implementation sorted tree entries by plain name
# and recomputed 50ecab76… against git's d8c6c042….  Git sorts a directory
# as if its name carried a trailing '/'.  The instrument disagreed with git
# loudly instead of agreeing plausibly, which is the only reason the bug was
# visible at all.
#
# STILL QUARANTINED.  The seat that did not write this has not bitten it.
#
# ---------------------------------------------------------------- LIMITS
# Stated because a gate whose boundary is unstated gets read as proving more
# than it does — the carry-forward gate's "green means AGREEMENT, not
# preservation" lesson, one circle on.
#
#   1. This proves a listing is COMPLETE FOR THE TREE IT NAMES.  It does not
#      prove the sender named the right tree.  A sender could emit a perfect
#      listing of a STALE commit and it would verify green.  The commit id
#      must be checked against the forge by someone with reach — which is the
#      courier, and is the residual trust this instrument cannot remove.
#   2. It says nothing about whether the ferry CONTAINS the listed files.  It
#      gives the receiver an authenticated inventory; diffing that inventory
#      against what arrived is the receiver's act, and is where an omission
#      actually becomes visible.
#   3. It is sha1, because git is sha1.  Every content pin elsewhere in this
#      record is sha256.  Do not read a green here as a sha256-strength claim.
#   4. It guards a CLASS (every blob under a tree), not a list — deliberately,
#      because SR43 is the hazard both seats demonstrated, and an instrument
#      built in the same round that demonstrated it should not repeat it.
