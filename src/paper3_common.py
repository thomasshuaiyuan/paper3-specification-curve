"""
Shared definitions for the Paper 3 specification-curve analysis.

Extracted from seir_pinn_multisignal.py so that this analysis runs without the
PINN codebase or PyTorch. The season boundaries and the loader are byte-for-byte
the same definitions used in the manuscript line.
"""

import os

import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "data", "flux_data.csv")

# CHP Flu Express influenza seasons. Comments record wave structure as
# classified in the v8 manuscript; they are not used by this analysis.
SEASONS = [
    ("2014/15 winter", "2014-10-01", "2015-06-01"),
    ("2015/16 winter", "2015-10-01", "2016-06-01"),
    ("2016/17 winter", "2016-09-15", "2017-06-01"),   # multi-wave
    ("2017/18 summer", "2017-04-01", "2018-04-01"),   # multi-wave
    ("2018/19 winter", "2018-09-15", "2019-06-01"),
    ("2023 summer",    "2023-01-15", "2023-10-01"),
    ("2023/24 winter", "2023-07-15", "2024-04-01"),   # multi-wave (post-COVID)
    ("2024/25 winter", "2024-08-01", "2025-04-01"),   # lowest amplitude
]

SINGLE_WAVE = ["2014/15 winter", "2015/16 winter", "2018/19 winter",
               "2023 summer", "2024/25 winter"]

CHANNELS = ["ILI_PMP", "ILI_AED", "ILI_CMP", "ILI_School", "ILI_NonSchool",
            "Fever_RCHE", "Adm_All", "Adm_0_5", "Adm_6_11", "Adm_12_17",
            "Adm_18_49", "Adm_50_64", "Adm_65_higher"]

LABEL = {
    "ILI_PMP": "Outpatient (private GP)", "ILI_AED": "Emergency attendance",
    "ILI_CMP": "Traditional medicine", "ILI_School": "School outbreaks",
    "ILI_NonSchool": "Non-school outbreaks", "Fever_RCHE": "Care-home fever",
    "Adm_All": "Admissions, all ages", "Adm_0_5": "Admissions 0-5y",
    "Adm_6_11": "Admissions 6-11y", "Adm_12_17": "Admissions 12-17y",
    "Adm_18_49": "Admissions 18-49y", "Adm_50_64": "Admissions 50-64y",
    "Adm_65_higher": "Admissions 65+y",
}

FAMILY = {
    "ILI_PMP": "Outpatient", "ILI_AED": "Emergency",
    "ILI_CMP": "Traditional medicine",
    "ILI_School": "Institutional outbreak",
    "ILI_NonSchool": "Institutional outbreak",
    "Fever_RCHE": "Care-home fever",
    **{c: "Hospital admissions" for c in
       ["Adm_All", "Adm_0_5", "Adm_6_11", "Adm_12_17", "Adm_18_49",
        "Adm_50_64", "Adm_65_higher"]},
}

# CHP's published operational laboratory-positivity threshold.
CHP_OPERATIONAL = 0.0494


def load_flux(path=DATA):
    df = pd.read_csv(path)
    df["From"] = pd.to_datetime(df["From"], format="%d/%m/%Y")
    df["To"] = pd.to_datetime(df["To"], format="%d/%m/%Y")
    df["MidDate"] = df["From"] + (df["To"] - df["From"]) / 2
    return df
