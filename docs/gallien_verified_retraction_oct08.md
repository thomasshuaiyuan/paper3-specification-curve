# Gallien et al. verified — and the retraction of this project's own false-negative finding

*8 October 2026. A verification record, written because the assessment that contained the error is
long and the lesson is short. Superseded by nothing; `claude/speccurve_upgrade_plan_assessment.md`
§1 carries the same correction in context.*

## The record

**VERIFIED.** PubMed PMID 39086096, metadata record fetched and fields compared 8 October 2026.

> Gallien Y, Paireau J, Paty A-C, Villegas-Ramirez B, Hamidouche M, Modenesi G, Zhu-Soubise A,
> Bonaldi C, Fouillet A, Vaux S, Bernard-Stoecklin S, Tarantola A. *Using the near real-time
> effective reproduction number Rt as an early-warning tool for seasonal bronchiolitis and
> influenza-like illness epidemics.* Am J Epidemiol 2025;194(5):1332–1340.
> doi:10.1093/aje/kwae195

Twelve authors. Santé publique France Île-de-France, with Paireau also at the Institut Pasteur
Mathematical Modelling of Infectious Diseases Unit. Journal Article, English. Keywords:
bronchiolitis, early warning, epidemic, influenza, reproduction number.

**Year correction.** The upgrade plan cites it as 2024. The issue year is **2025**; 2024 is
online-first. The reference list takes 2025, volume 194, issue 5, pages 1332–1340.

## What the paper contains, since it is a foil and not only a citation

Île-de-France emergency-department syndromic data, 2010–2022. Rt estimated in near real time and
the first indication of accelerated transmission (Rt > 1) compared against the alarm time points of
MASS, the statistics-based tool Santé publique France uses to declare epidemic phases. Rt alarmed a
median of **6 days earlier for influenza-like illness (IQR 4, 8)** and **64 days earlier for
bronchiolitis (IQR 52, 80)**. The authors conclude Rt is useful in combination with other
indicators.

**Why it is the closest of the three foils.** Garrido-Garcia is machine learning on search trends;
Otero is AEDSEO against MEM across 63 European series. Gallien is a single specification of
precisely the comparison this paper runs across thousands: an R(t)-based crossing against an
incumbent threshold rule, on syndromic surveillance, reported as a median lead with an IQR. It is
the paper whose answer the specification curve predicts is contingent — and its two headline
numbers, 6 days and 64 days, are a within-paper demonstration that the lead depends on which
series is being watched, which is a gift rather than a threat.

## The retraction

`claude/speccurve_upgrade_plan_assessment.md`, first version, asserted:

> **"Gallien et al. [58]" does not appear to exist.** […] A PubMed author search returns 81 Gallien
> papers across biomedicine and none matches. […] The plan has invented a name and a finding and
> proposed building a Discussion paragraph on both.

All of that is withdrawn. The paper exists, the journal attribution was right, and the described
content was right.

## How the error was made

The author search returned 81 PMIDs. **The metadata for none of them was fetched.** The judgement
"none matches" was reached from a list of bare identifiers, where no match could have been visible
either way. Two targeted searches run afterwards each returned exactly one record, PMID 39086096,
whose abstract matches the plan's description precisely.

A second factor made the wrong conclusion feel supported: the reference slot had a documented
history of mis-attribution, since the project instructions record Garrido-Garcia as "previously
mis-attributed to Pei S." A prior pattern was treated as circumstantial evidence for a new
instance of it.

## The rules this breached, both of which are already in the instructions

**"Verify before you worry."** The 19 September audit found an unfamiliar DOI prefix, a suspected
wrong article number and a possibly-fabricated preprint, and all three were fine. This is the
fourth instance of alarm not being evidence.

**"And verify the verifier."** An audit's finding carries the same burden as the claim it assesses.
This finding would have removed a real reference from a reference list and rewritten a Discussion
paragraph around engaging a paper that does not exist. It was not re-checked before it was written
down as a verdict.

**The direction matters and should be said plainly.** A false negative here costs work; a false
positive costs a retraction. This was the cheaper direction. It is the same defect.

## The operative rule that follows

**A search result is not a verification until the metadata record has been fetched and its fields
compared against what is written.** A hit count is not a check. A list of identifiers is not a
check. "No match found" is a claim about records that were read, and reporting it over records that
were not read is the same error as reporting a pass over a reference that was not resolved —
which is the error the 20 September pass made in the opposite direction on the Xie misspecification
companion.

This belongs beside the existing rule that a verification pass reads the project's prior
verification records before it runs. Both are about doing the mechanical step rather than
reasoning about what the mechanical step would probably have returned.

## Status of the rest of the assessment

Unaffected and standing, each verified independently of the Gallien section: the Otero et al. 2026
AEDSEO finding in Eurosurveillance (the competitive fact the plan does not know about); the absence
of `background_research_spec_curve_influenza.md` from the project store, which leaves roughly
twenty bracketed citations unverifiable; the Delphi Epidata revision-history result, which makes
the real-time-vantage workstream far cheaper than the plan assumes; the statistical corrections;
and the governance issues.
