# Tedlar LeadGen

Tedlar LeadGen is a tool for scraping, enriching, and generating personalized outreach for event and company leads.

## Features
- Streamlit UI for easy interaction
- Event and company data scraping
- Company and contact enrichment
- Personalized outreach message generation

## Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run main.py
   ```

## Directory Structure
```
tedlar-leadgen/
├── main.py               # Streamlit UI
├── agent.py              # Outreach generator
├── scraper.py            # Event/company scraper
├── enricher.py           # Company/contact enrichment
├── outreach.py           # Personalized message logic
├── utils.py              # Helper functions
├── config.py             # API keys and constants
├── requirements.txt
├── README.md
└── data/                 # Store output files
``` 