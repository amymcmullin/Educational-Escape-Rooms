# Educational Escape Rooms

Print-and-play escape rooms for career and technical education. Each one runs on
paper, needs no lab and no computers, and is built so a teacher can regenerate it
with different answer codes before putting it in front of a cohort.

Built for [Immokalee Technical College](https://itc.collierschools.com/) Computer
Systems & Information Technology (Florida program Y100200). Open for any CTE
program that wants to use or adapt it.

---

## Rooms

### SYSTEM LOCKDOWN — ransomware incident response

A worm called BLACKOUT has locked a client's server. Students are the incident
response team. The client's only IT tech quit and left four sealed envelopes and
a locked recovery box.

| | |
|---|---|
| **Play time** | 45 minutes, plus ~10 briefing and ~20 debrief |
| **Group size** | Teams of 3–5; runs cleanly from 8 to 30 students |
| **Prep** | ~25 minutes of printing and cutting for six teams |
| **Prerequisites** | None. Every reference card students need is in the envelope. |
| **Cost** | Free (sealed envelopes) up to about $40 (combination locks) |

Four **parallel** stations feed one final meta-puzzle:

| Station | Content | Employability skill on display |
|---|---|---|
| A — Parts Requisition | Hardware component identification; function vs. specification | Reading technical documentation for meaning |
| B — Memory Dump | Binary → decimal → ASCII character encoding | Precision; checking your own work |
| C — Network Map | IPv4 addressing, /24 subnet logic, ports and protocols | Comparing data systematically |
| D — Ransom Note | Caesar cipher, keyspace, why weak crypto fails | Following a procedure exactly |
| Final | Synthesis and documentation | Handoff and verification |

The stations are parallel rather than sequential on purpose: no team gets stuck
behind one puzzle, everyone works at once, and a quiet student can own a station
instead of watching one loud student solve everything.

**Contents**

```
system-lockdown/
  generator/build_pack.py   Builds the print pack. Puzzle codes are configurable.
  print-pack/*.pdf          18-page pack, cut-ready, black-and-white friendly
  facilitator/*.md          Setup, run of show, full answer key, debrief, troubleshooting
```

---

## Change the codes before you run it

**The default answer codes are published in this repository.** If your students
can find your GitHub, assume they can find the answers.

Every station code is derived from a config block at the top of
`generator/build_pack.py`. Change those values, rebuild, and you have a pack with
different answers — the layout, puzzles and reference cards all follow
automatically.

```bash
cd system-lockdown/generator
pip install -r requirements.txt
# edit the PUZZLE CONFIG block, then:
python3 build_pack.py
```

The build prints the answer key to the terminal:

```
built out/SYSTEM_LOCKDOWN_Print_Pack.pdf
  Station A (components) : 7349
  Station B (REBOOT)     : 8284
  Station C (network)    : 8621
  Station D (cipher)     : 3192 | word lock: PATCH
  MASTER CODE            : 4829
```

What you can change without touching layout code:

| Setting | Controls |
|---|---|
| `COMPONENT_IDS`, `REQUISITION_ORDER` | Which digit sits on each component card, and which four parts the requisition asks for |
| `RECOVERY_WORD` | The word hidden in the memory dump. Any length — the dump table and prose resize. |
| `ROGUE_HOST_OCTET`, `ROGUE_THIRD_OCTET` | The undocumented device on the wrong subnet |
| `CONTROL_PORT` | The protocol the traffic log points at |
| `CIPHER_SHIFT_WORD`, `RANSOM_PLAINTEXT` | The Caesar shift and the ransom note. Ciphertext is enciphered at build time. |

The facilitator guide's answer key reflects the **published defaults**. If you
change the config, the terminal output is your key.

---

## Three ways to run it

1. **Physical locks** (~$40) — four 4-digit combination locks and a lockbox. Best
   experience. An optional 5-letter word lock set to the Station D word works too.
2. **Sealed envelopes** (free) — write each code on the *outside* of a sealed
   envelope. A team may open it once they can tell you the code out loud. Costs
   nothing and keeps the whole feel.
3. **Google Form digital locks** — regex response validation blocks a student from
   advancing until the code is right, so it behaves like a lock, and you get
   timestamps for a leaderboard. Build instructions are in §9 of the facilitator
   guide. This is the best fit for a Google Classroom or no-lab environment.

---

## Notes for facilitators

- **It runs cold.** No prerequisite instruction, so it works as a week-one
  diagnostic. §2 of the guide lists what to watch for while teams play — who reads
  the reference card versus who guesses, who writes things down unprompted, who
  checks a teammate's arithmetic. That is better cohort data than any icebreaker.
- **Say less than feels comfortable.** The instinct to rescue a struggling team is
  the main threat to the activity.
- **The debrief is the lesson.** The escape room is the hook. §10 is 20 minutes and
  should not be skipped.
- **It laminates.** Reference cards, component cards, role cards, hint cards and
  cipher wheels last for years. Only six consumable sheets per team need
  reprinting between sections.

---

## Authorship

The scenario design, content alignment, classroom testing and facilitation
decisions are mine. The print pack generator and the facilitator guide were
produced with AI assistance against my specification.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — use it, change it,
run it with your students. Attribution appreciated.
