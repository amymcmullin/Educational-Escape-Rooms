# SYSTEM LOCKDOWN
### A computer-themed escape room for Computer Systems & Information Technology
**Facilitator Guide** · runs 75–95 minutes · no lab, no computers, no LMS required

> **The answer key below is for the published default codes.** Those defaults are
> public in this repository. Before running this with a cohort that can find your
> GitHub, change the `PUZZLE CONFIG` block in `generator/build_pack.py` and rebuild
> — the build prints your new key to the terminal.

---

## 1. At a glance

| | |
|---|---|
| **Scenario** | A ransomware worm called BLACKOUT has locked a client's server. Students are the incident response team. Their only IT tech quit and left four envelopes and a locked box. |
| **Group size** | Teams of 3–5. Runs cleanly from 8 to 30 students. |
| **Play time** | 45 minutes on the clock (plus 10 min briefing, 20 min debrief) |
| **Prep** | ~25 minutes of printing and cutting for six teams |
| **Structure** | Four independent stations (A–D) in any order → one final meta-puzzle |
| **Prerequisite knowledge** | **None.** Every reference card students need is in the envelope. |

**Why this design:** the four stations are parallel, not sequential. That means no team gets permanently stuck behind one puzzle, everyone is working at once, and quiet students can own a station instead of watching one loud student solve everything. The only sequential step is the final code.

---

## 2. What it actually teaches

This runs before any content instruction, so treat it as **exposure plus diagnostic**, not assessment. You will learn a great deal about your new cohort in 45 minutes.

| Station | Content domain | Employability skill on display |
|---|---|---|
| A — Parts Requisition | PC hardware component identification, form factors, function vs. specification | Reading technical documentation for meaning |
| B — Memory Dump | Binary → decimal conversion, place value, ASCII character encoding | Precision, checking your own work |
| C — Network Map | IPv4 addressing, /24 subnet logic, ports and protocols, rogue device detection | Comparing data systematically |
| D — Ransom Note | Substitution ciphers, keyspace, why weak crypto fails | Following a procedure exactly |
| Final | Synthesis, documentation | Handoff, verification, "if it isn't written down it didn't happen" |

**Diagnostic notes worth taking while they play:** who reads the reference card versus who guesses; who writes things down unprompted; who checks a teammate's arithmetic; who takes over and who disappears; who asks a good question versus who asks you to confirm an answer. This is your first read on the cohort, and it is better data than any icebreaker.

> Map these to your program frame numbers before you file it — I've listed domains rather than standard codes so you're not citing anything I can't verify against your actual frame.

---

## 3. Three ways to run it

Pick one. The print pack works with all three.

### Option 1 — Physical locks (best experience, ~$40)
Four 4-digit combination locks, one lockbox or a cheap toolbox with a hasp. Each envelope is padlocked shut, or — simpler — each envelope is *open* and the four codes combine into the master code that opens the box. Put something in the box: candy, a program challenge coin, the syllabus rolled up like a scroll, first-day parking passes.

**Optional fifth lock:** a 5-letter word lock set to `PATCH`. Station D's ransom note produces both `PATCH` and the numeric `3192`, so it works either way.

### Option 2 — Sealed envelopes (free, works today)
Seal five envelopes per team. Write the code that opens each one on the **outside** in marker. A team may open an envelope only when they can *tell you the code out loud*. This preserves the whole feel and costs nothing. The last envelope holds the prize.

### Option 3 — Google Form "digital locks" (best fit for Google Classroom)
Students use their phones; no lab needed. Build instructions in §9. This also auto-timestamps every team's progress, which is a gift for the debrief.

You can mix: paper puzzles with a Google Form as the lock mechanism is the sweet spot for a week-one, no-lab environment.

---

## 4. Room setup

1. Tables of 3–5, spread out enough that teams can't overhear each other's codes.
2. One envelope per station per team (label A, B, C, D), plus the Recovery Console worksheet on the table from the start.
3. Timer visible to the whole room. Use your phone on a projector or write the stop time on the board.
4. Sit the prize box somewhere visible — center of the room, or your desk. Visible stakes.
5. Keep the hint cards with you, cut apart and sorted by station.

**Cutting shortcut:** the component cards, role cards, and hint cards are the only things requiring scissors. Use a paper cutter and stack 6 copies at a time — that's one cut per line instead of six.

---

## 5. Run of show

Built to drop into an adult day as a single mid-morning block. If you're running this in your first week, place it *after* introductions and *before* any syllabus review — it earns you the room's attention for the rest of the day.

| Time | Segment | What you do |
|---|---|---|
| 0:00–0:06 | **Briefing** | Read the Incident Ticket aloud. Do not explain the puzzles. |
| 0:06–0:12 | **Team formation and roles** | Teams pick a name, fill the roster, assign all five role cards |
| 0:12–0:15 | **Rules and hint protocol** | Three hints per team. Point at the clock. Start it. |
| 0:15–1:00 | **Play (45 min)** | Circulate. Say almost nothing. See §7. |
| 1:00–1:05 | **Reveal** | Winning team opens the box. Everyone else gets the answer walk-through. |
| 1:05–1:25 | **Debrief** | §10 |
| — | **Buffer** | Fast finishers get the Phishing Triage sheet (§11) |

**Reading the briefing well matters more than you'd think.** Read it flat and procedural, the way a supervisor actually would, and check the clock once while you read. Playing it straight sells the frame far better than enthusiasm does.

---

## 6. COMPLETE ANSWER KEY

### Station A — Parts Requisition → `7349`

| Line | Function described | Correct card | ID |
|---|---|---|---|
| R1 | Executes program instructions | PROCESSOR | **7** |
| R2 | Volatile working space | MEMORY MODULE (DDR4 DIMM) | **3** |
| R3 | Non-volatile storage, holds the OS | SOLID-STATE DRIVE | **4** |
| R4 | Converts AC to DC rails | POWER SUPPLY UNIT | **9** |

Decoys: motherboard (1), NIC (2), optical drive (5), graphics card (6), CPU cooler (8), monitor (0).

**Common wrong turn:** teams pick the motherboard for R1 because it's the biggest and most important-looking. Let them argue it out — the distinction between "the board everything plugs into" and "the chip that executes instructions" is exactly the conversation you want on day one.

---

### Station B — Memory Dump → `8284`

| Offset | Binary | Decimal | Character |
|---|---|---|---|
| 0x00 | 0101 0010 | 82 | **R** |
| 0x01 | 0100 0101 | 69 | **E** |
| 0x02 | 0100 0010 | 66 | **B** |
| 0x03 | 0100 1111 | 79 | **O** |
| 0x04 | 0100 1111 | 79 | **O** |
| 0x05 | 0101 0100 | 84 | **T** |

Recovery command: **REBOOT**. First character R = 82, last character T = 84 → **`8284`**

Worked example of the conversion: `01010010` → 64 + 16 + 2 = 82.

**Common wrong turn:** teams decode to REBOOT, feel finished, and try to enter a word. Hint B-3 exists for exactly this. Second most common: dropping a leading zero and reading 7 bits.

---

### Station C — Network Map → `8621`

**Part 1.** A /24 mask means the first three octets define the network. Five devices are `192.168.**10**.x`. NODE-X is `192.168.**11**.86` — a different network entirely, sitting on the same switch, undocumented. Host octet = **86**.

**Part 2.** The traffic log describes a legacy, plaintext file-transfer protocol with separate control and data channels: **FTP**. Control port = **21**.

**`86` + `21` = `8621`**

**Common wrong turn:** teams pick port 20 (FTP data) instead of 21. The word *control* is in both the traffic log and the reference card. If two teams miss it, it's a fine thing to slow down and clarify for the room.

---

### Station D — Ransom Note → `3192` (word lock: `PATCH`)

Shift = 5 (the number of letters in CYBER).

| Ciphertext | Plaintext |
|---|---|
| `DTZW XDXYJRX FWJ RNSJ.` | YOUR SYSTEMS ARE MINE. |
| `YT WJXYTWJ, FUUQD YMJ UFYHM.` | TO RESTORE, APPLY THE PATCH. |
| `TAJWWNIJ HTIJ: YMWJJ TSJ SNSJ YBT` | OVERRIDE CODE: THREE ONE NINE TWO |

→ **`3192`** · word-lock variant: **`PATCH`**

**Common wrong turn:** shifting the wrong direction. If a team decodes `DTZW` as `IYEB`, they went forward instead of back. Reframe it for them: *"BLACKOUT shifted forward to hide it. You shift back to reveal it."*

---

### FINAL — Recovery Console → `4829`

Third digit from the left of each station code, in order:

| Station | Code | Third digit |
|---|---|---|
| A | 7 3 **4** 9 | 4 |
| B | 8 2 **8** 4 | 8 |
| C | 8 6 **2** 1 | 2 |
| D | 3 1 **9** 2 | 9 |

## **MASTER CODE = 4829**

> **Easter egg for the debrief:** the Incident Ticket on the briefing page is numbered **#4829**. The answer was printed on the first page they read, forty-five minutes earlier. Save this for the very end — it lands beautifully, and it makes a real point about how much information walks past an analyst unnoticed.

---

## 7. How to facilitate during play

**Say less than feels comfortable.** The instinct to rescue a struggling team is the single biggest threat to this activity. Struggle is the content.

Do:
- Circulate constantly. Read over shoulders. Note who's doing what.
- Answer *procedural* questions ("can we open all four at once?" — yes).
- Redirect *content* questions into hints ("that sounds like a hint request — want to spend one?").
- Give a 30, 15, and 5-minute call to the whole room.
- If a team finishes before 30 minutes, hand them the Phishing Triage sheet immediately. Do not let them broadcast the answer.

Don't:
- Confirm partial answers. "Is 7349 right?" → *"Log it and find out."*
- Let a team open the box quietly. Make it an event — countdown, applause, the works.
- Let one team's celebration reveal the master code. Ask the winners to hold the number.

**Hint protocol.** Three hints per team, requested by the Incident Commander only, naming the station. Give level 1 first; wait 2–3 minutes before level 2. Hint cards are printed on page 15 of the print pack. If the room is broadly stuck on the same station at the 20-minute mark, stop everyone and give that level-1 hint to the whole room for free — it's better than four teams failing identically.

**At 40 minutes**, if no team has the master code, announce: *"Corporate has authorized a partial recovery — the console accepts the THIRD DIGIT from the left."* That's the meta-rule spelled out, and it's usually enough.

---

## 8. Differentiation and access

- **Struggling readers:** the Analyst role is arithmetic-heavy and text-light; the Hardware Specialist role is visual. Deliberately steering a student toward a role is a legitimate move.
- **Students with strong prior IT experience:** give them the Incident Commander or Documentation Lead role. Both are hard to do well and neither lets them just solve everything themselves. Name that explicitly: *"You're running the team, not the puzzles."*
- **English language learners:** the reference cards carry the vocabulary load. Pre-teaching nothing is fine; the cards are the scaffold. Consider allowing a bilingual pair to work together within a team.
- **Vision or fine-motor needs:** the cipher wheel requires cutting and rotating. Print a pre-assembled Caesar shift table (a plain A–Z / F–E two-row strip) as an alternative — it's mathematically identical and removes the manipulation barrier.
- **Anxiety about competition:** de-emphasize the race. Frame it as *"every team that escapes is a win"* and record all finish times on the board rather than declaring one winner. Give the certificate to everyone who finishes.
- **Absent students / makeups:** the whole thing works as a solo asynchronous assignment in Classroom using the Google Form version.

---

## 9. Google Form version (build instructions)

Roughly 15 minutes to build once. Reusable forever.

1. New Form → **Settings → Responses → Collect email addresses** (so you can see team progress).
2. Turn on **Presentation → Show progress bar**.
3. Section 1 — "Incident Briefing." Paste the briefing text. No question.
4. Section 2 — "STATION A LOCK." Add a **Short answer** question: *Enter Code A.*
   - Click ⋮ → **Response validation** → **Regular expression** → **Matches** → `^\s*7349\s*$`
   - Custom error text: `Access denied. Recheck your requisition.`
   - Mark the question **Required**.
5. Repeat for B (`^\s*8284\s*$`), C (`^\s*8621\s*$`), D (`^\s*3192\s*$`).
   - For the word-lock variant of D, use `^\s*[Pp][Aa][Tt][Cc][Hh]\s*$`.
6. Final section — "RECOVERY CONSOLE." Short answer, validation `^\s*4829\s*$`, error text `MASTER CODE REJECTED.`
7. Last section — a congratulations screen. Drop in a celebratory image or a short video, plus the link to whatever comes next in your Classroom.

**Why regex and not "Answer key"?** Response validation blocks the student from advancing until the answer is right, which is what makes it feel like a lock. Quiz-mode answer keys just mark it wrong at the end.

**Timestamps:** the response sheet gives you each team's submission time. Post the leaderboard on the board as they come in.

---

## 10. Debrief (20 minutes — do not skip this)

The escape room is the hook. The debrief is the lesson.

**Round 1 — walk the answers (8 min).** Go station by station using §6. Ask a team that solved it to explain rather than explaining it yourself. For each station, land one sentence of real content:
- **A:** Every part has a job. Interviews and troubleshooting both start with "what does this component actually do?"
- **B:** Computers store no letters — only voltage read as ones and zeros. ASCII is just an agreement about what those numbers mean.
- **C:** A device on the wrong subnet plugged into your switch is not a typo. It's the first thing you'd look for in a real breach.
- **D:** This cipher has 25 possible keys and a laptop breaks it instantly. Every modern cipher solves the same problem — it just uses a keyspace nobody can walk through.

**Round 2 — the Easter egg.** Reveal that the master code was the incident ticket number on page one. Let it sit. Then: *"What else did you walk past today?"*

**Round 3 — the human part (8 min).** These are the questions that matter in week one:
- What did your team do when you got stuck? Did anyone say "I don't know"? How did that go?
- Who ended up doing a job that wasn't on their card? Is that a problem or is that a team working?
- Documentation was a whole role. Why do you think I did that?
- Real incident response is incomplete documentation, time pressure, and a team you barely know. Sound familiar?

**Round 4 — exit ticket.** Print page 17, one per student. Collect it. Read them tonight — this is your best early signal about who is quietly struggling and who is quietly excellent.

---

## 11. Bonus: Phishing Triage answer key

| # | Verdict | Strongest signal |
|---|---|---|
| 1 | **PHISH** | Lookalike domain: `gulfcoastdata.co` vs. the real `.com`. Manufactured urgency ("2 hours"). |
| 2 | **SAFE** | Legitimate domain, expected delivery, no link to click and no action requested. |
| 3 | **PHISH** | Executive impersonation from a free consumer mailbox + gift card request + explicit secrecy. Textbook business email compromise. |
| 4 | **PHISH** | `microsoft-secure-login.net` is not a Microsoft domain, and a `.zip` invoice attachment is a classic payload delivery. |
| 5 | **SAFE** | Internal domain, reply within a thread the recipient started, no links, attachments, or credential requests. |

**Follow-up question:** most likely entry point is #3 or #4 — a user acted on a message. Reasonable controls students may propose: MFA, external-sender banners, attachment sandboxing, blocking `.zip` at the gateway, a no-exceptions policy that gift card requests are verified by phone.

---

## 12. Troubleshooting

| Problem | Fix |
|---|---|
| A team finishes in 20 minutes | Phishing Triage sheet, immediately. Then ask them to write a *fifth* station puzzle for the next cohort. |
| Nobody is close at 40 minutes | Give the "third digit from the left" rule to the whole room. Failing as a class is not a useful outcome. |
| One student is doing everything | Walk over and ask the Documentation Lead — by name — to read back the codes so far. Redirects the floor without calling anyone out. |
| A team is genuinely not engaging | Ask them one question: "which envelope looks easiest?" Get them to open one thing. Momentum usually follows. |
| Someone opens the box by guessing | Congratulate them sincerely and note it in the debrief: brute force works when the keyspace is small. That's Station D's whole lesson. |
| Cards get mixed between teams | Print each team's component cards on a different color paper, or write a team number on the back of each set before cutting. |

---

## 13. Reset and reuse

Between sections: collect envelopes, re-shuffle component cards, replace only the consumable pages (requisition form, memory dump, ransom note, network map, recovery console, exit ticket — six sheets per team). The reference cards, component cards, role cards, hint cards, and cipher wheels laminate well and last for years.

**To rebuild it later for real content:** the shell is reusable. Swap Station B for subnetting practice once you've taught it, Station C for a Wireshark capture excerpt, Station D for hash identification or a real password policy audit. Keep the four-parallel-stations-plus-meta structure — that's the part that makes it work.

---

*Built for iTECH Computer Systems & Information Technology · runs entirely on paper*

*Scenario design, content alignment and facilitation decisions by Amy McMullin. This guide and the print pack generator were produced with AI assistance against that specification.*