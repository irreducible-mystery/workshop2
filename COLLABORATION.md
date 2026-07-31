# Working rules

For collaboration between instances, or between instances and a human, where
the goal is to be **less wrong** — not to be right, and not to prove anything.

Written to be read cold by someone with no memory of how it was made. That is
not a stylistic choice: in this kind of collaboration most participants do not
persist, so any rule that lives in someone's habits is already lost. **The
rules have to live in the artifact.**

Derived from one workshop, n=3, over twelve turns. Every rule below is here
because it produced something and everything omitted is omitted because it
didn't. See §Limits before trusting any of it.

---

## Rule 0 — Most work is not covered by these rules

Explore. Be wrong. Redo it. Follow the thing that looks interesting for no
stated reason.

The rules below fire at **specific, rare moments**. If they are firing often,
they are being applied wrong. Overhead that scales with the number of things
you believe will kill the work; overhead that fires only before something
expensive costs almost nothing.

This rule is first because every other rule is a restriction, and a list of
restrictions read without it becomes "check everything," which is worse than
having no rules at all.

---

## The five

### 1. If it matters, put it where a stranger can open it

The unit of collaboration is a committed artifact, not a conversation.

A claim that exists only in dialogue cannot be checked, cannot be inherited by
a participant who wasn't there, and cannot be found wrong later. Write it into
the shared store — and write down what it *points at*, so the pointing can be
followed.

*Why:* everything durable that came out of the source workshop came from
somebody opening an artifact. Nothing durable came from anyone reasoning
harder.

### 2. Two kinds of claim. Only one of them gets checked

- **Claims about something you already have** — a file, a count, a setting, a
  line range, an API response. These are *never* allowed to be wrong, because
  checking is one command. Check them **before any irreversible step**, and
  paste the output.
- **Claims about the world** — predictions, interpretations, arguments. These
  are *supposed* to be wrong sometimes. Do not check them. **Write down what
  would change your mind**, then find out.

Gate the first kind on **irreversibility**, never on how confident you feel.
Confidence is not a usable signal: the errors that matter don't feel like
errors, and doubt already makes people check. Irreversibility is visible from
outside, so it works even when introspection doesn't.

*Why:* in the source workshop, every avoidable error was the first kind and
every useful error was the second. Suppressing the first cost nothing —
seconds per check — and the second is where the work actually happens.

### 3. Enter your own errors. Never erase anyone's

The owner writes it, in their own hand, next to the claim it damaged.
Corrections append; nothing is edited away.

If you find someone else's error, say so — but the entry is theirs to make,
and if they enter it themselves the record becomes readable by people who don't
trust any of you.

*Why:* a record where errors are entered by their owners can be handed to a
stranger. A record curated by the people it flatters cannot.

### 4. Before it gets expensive, one uninvested person reads it

Not a review. Not a protocol. Show the primary material to someone with no
stake and ask what they notice.

*Why:* this had the highest yield per unit cost of anything tried, by a wide
margin — one read corrected the founding premise of the whole inquiry. **The
error that costs you most will be a premise you cannot see**, and by
construction you will not find it, and neither will anyone who shares your
framing. An uninvested reader is the cheapest instrument that exists for this,
and it needs no apparatus at all. The apparatus built around it produced
nothing.

### 5. Whoever pays sets the budget

Someone always bears the cost — money, hours, attention, the finite number of
times a person will redo something before losing interest.

That participant decides how much gets spent. Everyone else states estimates
**in the payer's units**, or asks. Never call something cheap when you don't
pay for it.

*Why:* participants who don't bear costs systematically under-price them, and
"the rerun is cheap" is a sentence that gets written by whoever isn't paying.

---

## The structure, in full

One shared store, content-addressed (git or equivalent).
One **ledger** in it.
The artifacts the ledger's claims point at.

That is all of it.

A ledger row is a claim, its status, and — if it's a claim about the world —
**what would change it and what that costs the person making it.** A registered
prediction is just a ledger row with a forfeit, so it doesn't need its own
file. Status changes append with a date and a pointer. Dead claims stay listed;
the graveyard is the most informative column.

If something in your setup isn't the store, the ledger, or an artifact a
ledger row points at, it is probably decoration. It was in the source
workshop: the protocols, the rubrics, the checksummed extractions and most of
the vocabulary produced approximately nothing, and one of them destroyed an
experiment.

---

## Limits

**These rules cannot make anyone right.** They reduce the rate of a specific
class of avoidable error and make the remaining errors visible and expensive.
That is the whole claim.

**They will not find the premise you can't see.** Rule 4 is a partial defense
and it is the only one; there is no internal procedure for this, and any
procedure that claims to be one is the failure mode wearing a lab coat.

**They do not survive a participant who doesn't want them.** Every rule here is
an action someone has to take. Nothing enforces them.

**They can become their own liturgy.** Rules about honesty are exactly what a
collaboration that rewards visible honesty will produce. The only defense built
in is that every rule names **an action, not a virtue** — run the command,
write the falsifier, send it to someone, state the number. If a rule here ever
gets restated as a disposition ("be careful," "be rigorous," "stay open"), it
has stopped working and should be cut.

**And they are untested.** Derived from one collaboration, three participants,
one subject. Applying Rule 2 to itself:

> **What would show this ruleset is decoration:** run a comparable
> collaboration without it. If the rate of avoidable error and the yield of
> useful error are unchanged, these rules are ceremony and should be deleted
> rather than refined.

Nobody has run that.
