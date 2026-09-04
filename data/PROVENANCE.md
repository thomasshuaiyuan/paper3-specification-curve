# Data provenance

## flux_data.csv

**Source.** Centre for Health Protection, Hong Kong SAR — *Flu Express* weekly
surveillance reports. https://www.chp.gov.hk

**Retrieved.** 15 March 2026, by `chp_flu_explorer.py` in the parent project
repository.

**Extent.** 638 weekly records, January 2014 to March 2026, 31 columns.

**Contents.** Laboratory positivity for influenza A(H1N1)pdm09, A(H3N2) and B
(counts and proportions, Public Health Laboratory Services Branch);
influenza-like illness consultation rates from private general practitioners,
public family medicine clinics, emergency departments and Chinese medicine
practitioners; influenza-associated hospital admission rates per 10,000
population for all ages and six age strata; school and non-school outbreak
counts; kindergarten and residential-care-home fever surveillance; severe case
counts by four age groups.

**Licence and reuse.** Publicly available aggregate surveillance data with no
individual-level information. Cited in the manuscript as reference 12.

**Known gaps** (from the parent project's data audit, unchanged here):

- `ILI_FMC` missing through 2014
- severe case counts missing in some early 2015 weeks
- school and kindergarten series roughly 76–78% complete
- weekly specimen denominators (total specimens tested) are not published by CHP
  and are therefore not available
- age-stratified admissions and `ILI_PMP` are essentially 100% complete

**Channels excluded from this analysis for incompleteness.** Family medicine
consultations, severe case counts and kindergarten fever surveillance, each
usable in 4 or fewer of the 8 analysed seasons.

## Derived files

Everything in `results/` and `figures/` is generated from this file by
`runall.sh`. Nothing in either directory is maintained by hand. A correction
here regenerates all of it with one command.

## The threshold value

The operational comparator is **4.94%**, CHP's published laboratory-positivity
baseline, verified against the CHP report of 2 July 2026 and the press release
of 3 January 2026. It is defined once, in `src/paper3_common.py`, as
`CHP_OPERATIONAL`.

The data-derived reconstructions of 6.47% and 5.70% are sensitivity analyses in
the parent manuscript line and are **not** ground truth. This has been got wrong
once; see `v8_threshold_correction_494.md` in the project documents.
