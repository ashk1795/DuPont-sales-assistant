from enricher import enrich_company_list
from stakeholder import find_stakeholders, find_stakeholders_for_companies

# 1. Find stakeholders for a single company
print("\n--- Stakeholders for a single company ---")
single_contacts = find_stakeholders("Avery Dennison")
for contact in single_contacts:
    print(contact)

# 2. Find stakeholders for a list of companies
print("\n--- Stakeholders for a list of companies ---")
company_list = [
    {"company": "Avery Dennison", "url": "https://averydennison.com"},
    {"company": "3M", "url": "https://3m.com"}
]
list_contacts = find_stakeholders_for_companies(company_list)
for contact in list_contacts:
    print(contact)

# 3. Integrate with enrichment pipeline
print("\n--- Enriched companies with stakeholders ---")
enriched = enrich_company_list(company_list)
for enriched_entry in enriched:
    stakeholders = find_stakeholders(enriched_entry["company"])
    print({**enriched_entry, "stakeholders": stakeholders})
