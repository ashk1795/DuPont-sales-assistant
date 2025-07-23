import streamlit as st
import pandas as pd
import io
from enricher import enrich_company
from outreach import generate_outreach_note
from scraper import scrape_event_companies  # Assumes this function exists
from stakeholder import find_stakeholders_for_company  # Assumes this function exists

st.set_page_config(page_title="Tedlar LeadGen", layout="wide")
st.title("Tedlar LeadGen")
st.write("Welcome to the Tedlar LeadGen Streamlit UI.")

st.header("1. Upload or Scrape Event/Company Data")

input_method = st.radio("How would you like to input company data?", ["Upload CSV", "Scrape Event Website"])

companies_df = None
if input_method == "Upload CSV":
    uploaded_file = st.file_uploader("Upload a CSV file with company/event data", type=["csv"])
    if uploaded_file:
        companies_df = pd.read_csv(uploaded_file)
        st.success(f"Loaded {len(companies_df)} companies from CSV.")
elif input_method == "Scrape Event Website":
    event_url = st.text_input("Enter event website URL to scrape companies:")
    if st.button("Scrape Companies") and event_url:
        with st.spinner("Scraping companies from event website..."):
            try:
                companies = scrape_event_companies(event_url)
                companies_df = pd.DataFrame(companies)
                st.success(f"Scraped {len(companies_df)} companies from event.")
            except Exception as e:
                st.error(f"Error scraping event: {e}")

if companies_df is not None and not companies_df.empty:
    st.header("2. Company Table (Raw Data)")
    st.dataframe(companies_df)

    st.header("3. Enrich Companies & Identify Stakeholders")
    if st.button("Enrich All Companies & Find Stakeholders"):
        enriched_rows = []
        with st.spinner("Enriching companies and finding stakeholders. This may take a minute..."):
            for idx, row in companies_df.iterrows():
                company_name = row.get('company') or row.get('Company') or row.get('name')
                enriched = enrich_company(company_name) or {}
                # Merge original row and enrichment
                enriched_row = {**row.to_dict(), **enriched}
                # Find stakeholders (decision-makers)
                try:
                    stakeholders = find_stakeholders_for_company(company_name)
                except Exception as e:
                    stakeholders = [{"name": "[Error]", "title": str(e), "linkedin": ""}]
                enriched_row['stakeholders'] = stakeholders
                # For each stakeholder, generate outreach
                outreach_messages = []
                for s in stakeholders:
                    lead = {
                        "company": company_name,
                        "contact_name": s.get("name", ""),
                        "title": s.get("title", ""),
                        "linkedin_url": s.get("linkedin", ""),
                        "event": row.get("event", ""),
                        "rationale": enriched_row.get("rationale", "") or enriched_row.get("industry_fit", "")
                    }
                    outreach = generate_outreach_note(lead)
                    outreach_messages.append({**lead, "outreach_message": outreach})
                enriched_row['outreach_messages'] = outreach_messages
                enriched_rows.append(enriched_row)
        # Flatten for display
        display_rows = []
        for r in enriched_rows:
            for o in r['outreach_messages']:
                display_rows.append({
                    "Company": r.get("company") or r.get("Company") or r.get("name"),
                    "Contact Name": o.get("contact_name"),
                    "Title": o.get("title"),
                    "LinkedIn URL": o.get("linkedin_url"),
                    "Event": r.get("event", ""),
                    "Industry Fit": r.get("industry_fit", ""),
                    "Revenue": r.get("revenue", ""),
                    "Employees": r.get("employees", ""),
                    "Rationale": o.get("rationale", ""),
                    "Outreach Message": o.get("outreach_message", "")
                })
        results_df = pd.DataFrame(display_rows)
        st.header("4. Enriched Leads & Outreach Table")
        st.dataframe(results_df)
        # Download
        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="enriched_outreach_leads.csv",
            mime="text/csv"
        )
        st.success("All features complete!")
else:
    st.info("Upload a CSV or scrape an event to get started.") 