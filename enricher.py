import pandas as pd

def score_company(revenue_str, employees_str):
    revenue = float(revenue_str.strip("$B")) if "B" in revenue_str else 0
    employees = int(employees_str.replace(",", ""))
    score = 0
    if revenue >= 1.0:
        score += 50
    if employees >= 1000:
        score += 30
    return score

def enrich_company(company_name):
    # Placeholder enrichment logic (fake data)
    revenue = "$1.2B"
    employees = "5,000"
    score = score_company("1.2B", "5000")
    return {
        "company": company_name,
        "industry_fit": "Signage & Graphics",
        "revenue": revenue,
        "employees": employees,
        "priority_score": score,
        "rationale": f"{company_name} specializes in signage and has >$1B revenue.",
    }

def enrich_company_list(company_list):
    enriched = []
    for entry in company_list:
        enriched_data = enrich_company(entry["company"])
        enriched.append({**entry, **enriched_data})
    return enriched

def save_enriched_data(data, path="data/enriched_companies.csv"):
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)

if __name__ == "__main__":
    companies = [
        {"company": "Avery Dennison", "url": "https://averydennison.com"},
        {"company": "3M", "url": "https://3m.com"}
    ]
    enriched = enrich_company_list(companies)
    from pprint import pprint
    pprint(enriched)
