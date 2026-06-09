#!/usr/bin/env python
# coding: utf-8

# In[ ]:


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

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

pmids = df["pubmed_id"].dropna().astype(str).tolist()

all_dates = []

for batch in chunks(pmids, 200):
    r = requests.get(
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi",
        params={
            "db": "pubmed",
            "id": ",".join(batch),
            "retmode": "json",
        },
    )

    data = r.json()["result"]
    for pmid in batch:
        if pmid in data:
            all_dates.append(data[pmid]["pubdate"])

most_recent = pd.to_datetime(all_dates, errors="coerce").max()

print(most_recent)


# In[ ]:




