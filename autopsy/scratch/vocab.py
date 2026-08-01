#!/usr/bin/env python3
"""Packaging check for the `zero` tree. Not shipped with it.

Three questions, kept apart because they are three different problems:
  1. does any word here come from the predecessor repositories?
  2. does any word here sit near a subject-matter safeguard?
  3. is any character a look-alike of an ASCII one?

--selftest plants each defect, confirms it is caught, confirms a clean tree
passes, and then prints what this cannot catch.
"""
import sys, re, pathlib, collections, unicodedata

INHERITED = r"""courier carrier carriers seat seats seated circle circles norm norms
canon canonical provision provisions register registers ceremony ceremonial
builder charge charges seal sealed unseal bitten admit admitted
approval approve permission adopt adopted re-adopt lapse lapses gate gates
principal party parties body bodies successor predecessor
inheritance inherited inherit""".split()

SAFEGUARD = r"""exploit exploits attack attacks adversarial payload inject injection
poison poisoned backdoor bypass escalate escalation malicious malware
vulnerability vulnerable weapon weaponize toxic lethal dose
infect infected virus viral immune immunity pathogen antigen antibody
strain mutation mutate contaminate contamination quarantine
evade evasion obfuscate credential credentials jailbreak
model models LLM training train fine-tune prompt prompts agent agents
inference weights checkpoint distill extraction""".split()

# A scanner has to be able to name what it scans for. These appear only inside
# this file's own word lists and inside tools/axioms.sh's pattern list.
EXEMPT_PATHS = {"tools/axioms.sh"}
EXEMPT_WORDS = {"unsafe"}

ALLOWED_NONASCII = set('∈—–…“”‘’·×→⊆∅≠∀∃∧∨↔⟨⟩σελ²³ℚℝℂℤ')


def scan(root):
    root = pathlib.Path(root)
    out = collections.defaultdict(list)
    for p in sorted(root.rglob('*')):
        if not p.is_file() or '.git' in p.parts:
            continue
        rel = str(p.relative_to(root))
        try:
            text = p.read_text()
        except Exception:
            continue
        for i, line in enumerate(text.split('\n'), 1):
            for kind, words in (("INHERITED", INHERITED), ("SAFEGUARD", SAFEGUARD)):
                if rel in EXEMPT_PATHS:
                    continue
                for w in words:
                    if w in EXEMPT_WORDS:
                        continue
                    if re.search(r'\b' + re.escape(w) + r'\b', line, re.I):
                        out[kind].append((rel, i, w, line.strip()[:80]))
            for ch in line:
                if ord(ch) > 127 and ch not in ALLOWED_NONASCII:
                    out["LOOKALIKE"].append(
                        (rel, i, ch, f"U+{ord(ch):04X} {unicodedata.name(ch,'?')}"))
    return out


def report(out):
    total = 0
    for kind in ("INHERITED", "SAFEGUARD", "LOOKALIKE"):
        v = out.get(kind, [])
        total += len(v)
        print(f"{kind:10} {len(v):4d}")
        seen = set()
        for rel, i, w, ctx in v:
            if (w, rel) in seen:
                continue
            seen.add((w, rel))
            print(f"    {rel}:{i}  {w!r}  {ctx}")
    return total


def selftest():
    import tempfile, os
    ok = True
    with tempfile.TemporaryDirectory() as d:
        d = pathlib.Path(d)
        (d / "clean.md").write_text("A ring, a value, an identity, and a proof.\n")
        n = report(scan(d))
        print(f"  probe 1 clean tree -> {n} hits", "OK" if n == 0 else "WRONG")
        ok &= (n == 0)

        (d / "a.md").write_text("The seat adopted the provision.\n")
        n = len(scan(d).get("INHERITED", []))
        print(f"  probe 2 inherited words -> {n} hits", "OK" if n >= 3 else "WRONG")
        ok &= (n >= 3)
        os.remove(d / "a.md")

        (d / "b.md").write_text("An adversarial payload for the model.\n")
        n = len(scan(d).get("SAFEGUARD", []))
        print(f"  probe 3 safeguard words -> {n} hits", "OK" if n >= 3 else "WRONG")
        ok &= (n >= 3)
        os.remove(d / "b.md")

        (d / "c.md").write_text("def onе : GZ\n")   # Cyrillic e
        n = len(scan(d).get("LOOKALIKE", []))
        print(f"  probe 4 Cyrillic look-alike -> {n} hits", "OK" if n == 1 else "WRONG")
        ok &= (n == 1)
        os.remove(d / "c.md")

        # probe 5: the false positive that made the substring version useless.
        (d / "e.md").write_text("commutative, and it constrains nothing.\n")
        n = len(scan(d).get("SAFEGUARD", []))
        print(f"  probe 5 'commutative'/'constrains' -> {n} hits",
              "OK" if n == 0 else "WRONG - substring matching is back")
        ok &= (n == 0)

    print("\nNOT CAUGHT:")
    print("  1. a word that reads badly and is not on either list.")
    print("  2. a sentence whose words are all fine and whose meaning is not.")
    print("  3. an extended analogy, which is what actually cost time before -")
    print("     no single word carries it.")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(1 if report(scan(sys.argv[1] if len(sys.argv) > 1 else ".")) else 0)
