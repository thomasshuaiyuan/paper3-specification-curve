# Assessment of the proposed Q1 upgrade plan — specification-curve paper

*8 October 2026. The plan was supplied as "Plan only," ten weeks solo full-time, four analysis
workstreams. This assesses feasibility, and then the things that are not feasibility problems.*

*Revised the same day. **§1's central finding was wrong and is retracted**: Gallien et al. is a real
paper, verified against PubMed, and the plan's use of it was correct. The retraction and how the
error was made are in §1. Everything else was verified independently and stands.*

---

## Verdict in one line

**Roughly 80% of the analysis is possible and most of it is cheaper than the plan assumes. The one
thing the plan does not know about is a competing paper published in the target journal three
months ago. Its reference list still needs verifying, but the specific citation this assessment
first flagged as fabricated is sound.**

---

## 1. The citation problem, which comes first

The plan carries about twenty bracketed references to
`background_research_spec_curve_influenza.md`. **That file is not in the project store.** A search
on its distinctive content returns nothing. So every numbered citation in the plan is unverifiable
from here, in a project whose hardest standing rule is that an unverified reference does not enter
a document.

### Retracted: the Gallien finding was wrong, and the error was this assessment's

**An earlier version of this section asserted that "Gallien et al. [58] does not appear to exist,"
that the plan had confused it with Garrido-Garcia et al., and that "the plan has invented a name
and a finding." All three claims are withdrawn. The paper is real and the plan was right.**

Verified 8 October 2026 against PubMed, record PMID 39086096: **Gallien Y, Paireau J, Paty A-C,
Villegas-Ramirez B, Hamidouche M, Modenesi G, Zhu-Soubise A, Bonaldi C, Fouillet A, Vaux S,
Bernard-Stoecklin S, Tarantola A, *Using the near real-time effective reproduction number Rt as an
early-warning tool for seasonal bronchiolitis and influenza-like illness epidemics*, Am J Epidemiol
2025;194(5):1332–1340, doi:10.1093/aje/kwae195.** Twelve authors, Santé publique France and
Institut Pasteur. Île-de-France emergency-department syndromic data, 2010–2022. Rt alarms arrived a
median of 6 days earlier than the incumbent MASS alarm for influenza-like illness (IQR 4–8) and 64
days earlier for bronchiolitis (IQR 52–80).

So the plan's journal was right, its description of the content was right, and it is a genuine foil
alongside Garrido-Garcia and Otero — arguably the closest of the three, because it is a single
specification of exactly the R(t)-versus-threshold comparison this paper runs across thousands.
**One correction to the plan's own citation**: the issue year is 2025, not 2024. The 2024 date is
online-first; the reference list takes 2025 with volume 194, issue 5, pages 1332–1340.

**How the error was made, because the mechanism matters more than the correction.** The PubMed
author search returned 81 PMIDs and the metadata for none of them was fetched. The judgement
"none matches" was made from a list of bare identifiers. Two targeted searches run afterwards each
returned exactly one record, PMID 39086096, and its abstract matches the plan's description
precisely. The reference slot had a prior history of mis-attribution (the project instructions
record Garrido-Garcia as "previously mis-attributed to Pei S."), and that history was used as
circumstantial support for a conclusion the evidence did not carry.

**This is the exact failure mode two of the project's own standing rules exist to prevent.**
"Verify before you worry" — alarm is not evidence. And "verify the verifier" — an audit's finding
carries the same burden as the claim it assesses. A false negative costs work rather than a
retraction, which is the cheaper direction, but it is the same defect. **The operative rule: a
PubMed or Crossref search result is not a verification until the metadata record has been fetched
and its fields compared. A count of hits, or a list of identifiers, is not a check.**

Everything else in this assessment was verified independently of the Gallien section and stands:
the Otero/AEDSEO finding in §2, the missing background reference file, the Delphi revision-history
result, the statistical corrections and the governance issues.

**Action before any of the plan runs:** every reference in
`background_research_spec_curve_influenza.md` goes through `verify_citations.py` from a container
that reaches Crossref, and the file goes into the project store. Until then Workstream D cannot
start, because its entire content is that reference list.

## 2. What the plan does not know, and it is bigger than anything in the plan

**Otero SM, Emborg H-D, Telkamp KS, Moustsen-Helms IR, Søborg B, Christiansen LE, *Evaluation of
the Automated and Early Detection of Seasonal Epidemic Onset and Burden Levels (AEDSEO) method for
respiratory surveillance using data from 21 European countries*, Euro Surveill 2026;31(30),
doi:10.2807/1560-7917.ES.2026.31.30.2500896.** Retrieved from PubMed, 8 October 2026.

Published in **the target journal**, in July 2026, three months ago. It compares AEDSEO against MEM
across **63 surveillance series from 21 European countries**, covering influenza, RSV, ARI and ILI.
AEDSEO signalled onset in 60 of 63 series against MEM's 55, and **signalled earlier in 45 of the 55
where both fired**. Median lead times reported: 6.5 weeks influenza, 4.5 RSV, 22.0 ARI, 5.5 ILI.

The plan lists this as "AEDSEO [34]," one of ten to fifteen studies to extract into an audit table.
That badly understates what it is. Four consequences:

**It is the best available foil, better than Schanzer or White.** Sixty-three point-estimate lead
times, each from a single specification, in the journal this manuscript is aimed at. The audit
figure gains its strongest row from it.

**It engages the manuscript's MEM finding directly, and the manuscript does not engage back.** The
draft's surviving family claim is that MEM is the only estimator whose direction never reverses.
Otero et al. report that a competing method beats MEM on earliness in 45 of 55 series. These are
not contradictory — different estimands — but a Eurosurveillance reviewer who handled that paper
will expect the connection drawn.

**It moves the novelty bar in the target journal.** `roadmap_v3_source.md` says "the ground is
empty — no specification-curve, multiverse or vibration-of-effects analysis of infectious-disease
surveillance." That is still true as written, because Otero et al. is not a specification curve.
But "Eurosurveillance has not recently published a large multi-country onset-detection method
comparison" is no longer true, and the framing has to account for it.

**It is a scale argument against the current draft.** Two systems and 23 channels, beside 21
countries and 63 series. The paper's defence is that it varies the analysis rather than the data,
which is the right defence and must be made explicitly.

## 3. Workstream-by-workstream feasibility

### A1 — null test. Possible. Compute is fine; the statistics are not as specified.

**Compute.** The plan's estimate of 180k detections per replicate is right, and its "≤10⁵ per run"
claim elsewhere contradicts it. Measured against the US run in this repo (3,024 specs × 10 channels
in about six minutes), a full-space HK replicate is three to five minutes, so 1,000 replicates is
**50 to 80 hours single-threaded**. The pilot-throughput rule is the right instinct.

**A speedup the plan misses, worth roughly 5–10×.** Under season-alignment permutation the baseline
thresholds do not change: they are computed from pooled non-season weeks of the whole series, and
permuting within-season alignment leaves that pool intact. So thresholds can be computed **once per
specification** and reused across all 1,000 replicates, leaving only the crossing search in the
inner loop. That brings the full space within an overnight run and makes the 500-specification
fallback unnecessary.

**The statistical problem, and it is the project's own known defect at 75× scale.** A1 proposes
22,464 per-specification p-values and then reports "the share of specifications with p < 0.05."
The project instructions already flag this: *"a project whose thesis is that specification variants
are not independent observations cannot report 296 of them as 296 independent observations. Decide
the unit of analysis once, in writing, for both strands."* That decision is still open, and A1 as
written makes it implicitly and in the anti-conservative direction.

The Simonsohn-style pooled test is the right object and is one number per channel. It should be the
headline; the per-specification share should either go, or be reported as a descriptive quantity
with no p attached.

**A second problem, smaller.** Leads are multiples of seven days and the statistic is a median of
eight seasons, so the null distribution is heavily discrete and p-values will be chunky. Report
the achievable resolution rather than quoting p to three decimals.

### A2 — variance-component regression. Possible in minutes, and largely redundant as specified.

The specification space is a **balanced full factorial**. In a balanced factorial with no
interactions, the OLS main-effect coefficients are an exact linear recoding of the swing table
already in Table 2. The plan's acceptance criterion — "coefficient ranking compared against the
swing ranking; any disagreement reported" — will find no disagreement, by construction. That is not
a finding, it is arithmetic.

**The interactions are the only new content**, and they are worth having, because they operationalise
the "choices compound" claim the swing decomposition cannot express.

**HC3 is the wrong standard error.** Errors are correlated within specification across the 13
channels and within channel across specifications. HC3 addresses neither. Two-way clustered SEs, or
a mixed model with crossed random effects for specification and channel.

### B — simulation with known truth. Possible, cheap, and the most valuable item in the plan.

Compute is trivial: twelve synthetic seasons across the full threshold space and R(t) space is on
the order of twenty minutes. The value is high because it closes the draft's self-declared
limitation and converts instability into a bias map.

**One design flaw that would undermine it.** The plan defines known truth as "first week true
intensity exceeds 1% of that season's peak amplitude, sustained 2 weeks." That is itself a
specification choice of exactly the kind the paper studies, and it fires at different relative
points on channels with different shapes and scales, so the measured bias is contaminated by the
thing being measured. **The imposed shift L is the truth.** Report estimate − L and drop the
threshold-based truth definition, or report both and show they differ, which is itself a finding.

**Expect the mechanism test to be equivocal.** The real-data version already splits: zero fraction
predicts relative threshold drop (ρ = 0.570, p = 0.042) but not the shift in days (ρ = −0.470,
p = 0.105). The plan is right to pre-register and report either way.

### C — real-time vantage. Possible, and substantially easier than the plan says.

**Checked directly today.** The Delphi V4 API is alive, and historical issues are queryable:
a single epiweek returns **24 distinct issues** spanning lag 5 to lag 51. So the whole revision
history is retrievable retrospectively.

That removes the plan's premise. There is no need to "pull a second pinned issue +8 weeks after the
original pin" and wait — an as-of vintage can be reconstructed for every week of every season now,
which is a stronger design than a single +8-week comparison. The vintage dimension becomes a
genuine ninth dimension rather than a two-level sensitivity check.

**The deprecation deadline in the project instructions is live.** V4 is tentatively deprecated from
October 2026, which is now. The API responded today. Pull and pin the full revision history this
week rather than scheduling it for week 6.

**A pre-specification note.** In confirming the API behaviour I saw one epiweek's revision
magnitude. That is a peek at an outcome of Workstream C and is recorded here so the pre-registration
can declare it.

**The Hong Kong arm is the weak half.** Archived Flu Express vintages may not exist, and the
fallback — right-truncation plus chain-ladder — *simulates* revision rather than measuring it, so it
answers a different question and must be labelled as such. Before spending a week: establish whether
CHP materially revises these series at all. If it does not, vantage is a United States question and
should be presented as one.

### D — published-estimate audit figure. Possible and cheap, gated entirely on §1.

Extraction of ten to fifteen studies is days of work, and the figure is a good one: specification
ranges with published point estimates overlaid, coloured by how many of the eight dimensions each
study reports. That is the paper's thesis in one panel, and it is the strongest single addition
after the simulation.

It cannot start until the reference list is verified, because the reference list *is* the
workstream.

## 4. The problems that are not feasibility

**Nothing here has been put to Vijay.** Standing instruction 2: no analysis direction advances
toward a standalone submission without his input. The plan proposes a ten-week programme, a
restructure, a journal decision and an escalation branch, none of it raised with him. It should go
to him as one short message — the current state, the four proposed additions, and the journal
question — before week one.

**The plan contradicts the roadmap on what this paper is.** `roadmap_v3_source.md` has Strand B as
Eurosurveillance or EID, **short communication**, eight sections with six ready. The plan adds
roughly 1,600 words and three Results sections. Those are different papers. Someone has to choose,
and it is his call under the standing division of writing labour.

**"Solo, full-time, ten weeks" does not match the project.** The current instructions have the
specification curve as chapter 3 of the conversion argument, with the sampling-exponent line as the
main thread, coursework running, lab integration in its first weeks, and four items carrying October
deadlines. Ten weeks of full-time single-paper work is not available, and committing to it would
displace the thing the conversion argument rests on.

**The Nature Communications branch is not realistic and should be dropped.** The project
instructions are explicit that NC is his aspiration for the papers *after* this one, and that the
honest ceiling for this line is BMC Public Health, *Epidemics*, *Influenza and Other Respiratory
Viruses*, or Eurosurveillance/EID. AJE as first choice is defensible — White et al. is in AJE
Advances — but a specification-curve methods paper does not reach NC, and holding four weeks for it
costs more than it can return.

**One assumption in the plan is wrong in the optimistic direction, which is worth saying because
it is the only one.** The plan budgets about a week to regenerate specification-level output if it
was not saved per estimate. For Hong Kong it was not — `paper3_anchor_speccurve.csv` carries
`median_lead` collapsed across seasons, with no season column. But `runall.sh --fresh` regenerates
everything in about nine minutes, so this is an afternoon of editing the writer to emit season-level
rows, not a week.

## 5. What to do, in order

1. **Verify the background reference list.** Put the file in the project store and run
   `verify_citations.py` from a container that reaches Crossref. Nothing else starts first. Half a
   day. Gallien et al. is now verified (PMID 39086096, Am J Epidemiol 2025;194(5):1332–1340) and
   needs only its year corrected from 2024 to 2025; the other nineteen-odd slots are untouched.
2. **Read Otero et al. 2026 and decide what it does to the framing.** It is in the target journal,
   it is three months old, and it is both the best foil and the strongest competitive fact. Half a
   day.
3. **Pull and pin the full Delphi revision history this week**, because the API carries a live
   deprecation date and the data is the input to Workstream C.
4. **Put the four additions and the journal question to Vijay in one short message**, per "shorter
   emails, more papers."
5. **Then, if he agrees: Workstream B first** — it is the highest value, the cheapest compute, and
   the one that converts the paper's claim from instability to validity. A1 second, with the unit of
   analysis decided in writing beforehand. D third. C alongside, since its data pull is already
   done.

A2 is an afternoon and can ride along with A1. The simulation is the paper; the rest is support.
