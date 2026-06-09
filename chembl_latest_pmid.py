#!/usr/bin/env python
# coding: utf-8

# In[42]:


import requests
import pandas as pd

import chembl_downloader

sql = """
SELECT DISTINCT
        doc_id, pubmed_id, year 
FROM docs
WHERE year > 2024 and pubmed_id is not null
"""

df = chembl_downloader.query(sql, version="37")

pmids = df["pubmed_id"].astype(str).tolist()[:350]


records = []

for i in range(0, len(pmids), 200):
    batch = pmids[i:i+200]

    r = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
        params={
            "db": "pubmed",
            "id": ",".join(batch),
            "retmode": "json",
        },
    )

    r.raise_for_status()
    data = r.json()["result"]

    for pmid in batch:
        if pmid in data:
            records.append(
                {
                    "pmid": pmid,
                    "pubdate": pd.to_datetime(
                        data[pmid]["pubdate"],
                        errors="coerce",
                    ),
                }
            )

result = (
    pd.DataFrame(records)
    .dropna(subset=["pubdate"])
    .sort_values("pubdate", ascending=False)
    .iloc[0]
)

print("PMID:", result["pmid"])
print("Date:", result["pubdate"])


# In[ ]:




