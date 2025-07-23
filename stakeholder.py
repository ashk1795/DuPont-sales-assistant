def find_stakeholders(company_name):
    # Mocked contact data for demo purposes
    return [
        {
            "name": "Laura Noll",
            "title": "VP of Product Development",
            "linkedin": "https://www.linkedin.com/in/laura-noll-6388a55/",
            "company": company_name
        },
        {
            "name": "John Doe",
            "title": "Director of Innovation",
            "linkedin": "https://www.linkedin.com/in/johndoe/",
            "company": company_name
        }
    ]

def find_stakeholders_for_companies(company_list):
    all_contacts = []
    for entry in company_list:
        company_name = entry.get("company") or entry.get("name")
        contacts = find_stakeholders(company_name)
        all_contacts.extend(contacts)
    return all_contacts

if __name__ == "__main__":
    companies = [
        {"company": "Avery Dennison"},
        {"company": "3M"}
    ]
    contacts = find_stakeholders_for_companies(companies)
    from pprint import pprint
    pprint(contacts)

def find_stakeholders_for_company(company_name):
    """
    Given a company name, return a list of dicts with stakeholder info.
    Example return:
    [
        {"name": "Jane Doe", "title": "VP of Product", "linkedin": "https://linkedin.com/in/janedoe"},
        {"name": "John Smith", "title": "Director of Innovation", "linkedin": "https://linkedin.com/in/johnsmith"}
    ]
    """
    # TODO: Replace with your real stakeholder-finding logic
    # For now, return a mock list for testing
    return [
        {"name": "Jane Doe", "title": "VP of Product", "linkedin": "https://linkedin.com/in/janedoe"},
        {"name": "John Smith", "title": "Director of Innovation", "linkedin": "https://linkedin.com/in/johnsmith"}
    ]