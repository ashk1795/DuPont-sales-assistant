from flask import Flask, request, render_template_string, send_file, redirect, url_for, flash
import csv
import io
import os
from enricher import enrich_company
from outreach import generate_outreach_note

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Company Enrichment & Outreach Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #333; }
        form { margin-bottom: 30px; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background: #f4f4f4; }
        .error { color: red; }
        .success { color: green; }
        .spinner { color: #555; font-style: italic; }
    </style>
</head>
<body>
    <h1>Company Enrichment & Outreach Dashboard</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
      {% if messages %}
        {% for category, message in messages %}
          <div class="{{ category }}">{{ message }}</div>
        {% endfor %}
      {% endif %}
    {% endwith %}
    <h2>Single Company/Contact</h2>
    <form method="post" enctype="multipart/form-data" action="/enrich">
        <input type="text" name="company_name" placeholder="Company name" required>
        <input type="text" name="contact_name" placeholder="Contact name" required>
        <input type="text" name="title" placeholder="Title" required>
        <input type="text" name="linkedin_url" placeholder="LinkedIn URL (optional)">
        <input type="text" name="event" placeholder="Event" required>
        <input type="text" name="rationale" placeholder="Rationale (why a fit)" required>
        <button type="submit">Enrich & Generate Outreach</button>
    </form>
    {% if single_result %}
        <h3>Result</h3>
        <table>
            <tr>
                <th>Company</th><th>Contact Name</th><th>Title</th><th>LinkedIn URL</th><th>Event</th><th>Rationale</th><th>Outreach Message</th>
            </tr>
            <tr>
                <td>{{ single_result['company'] }}</td>
                <td>{{ single_result['contact_name'] }}</td>
                <td>{{ single_result['title'] }}</td>
                <td>{{ single_result['linkedin_url'] }}</td>
                <td>{{ single_result['event'] }}</td>
                <td>{{ single_result['rationale'] }}</td>
                <td><pre style="white-space: pre-wrap;">{{ single_result['outreach_message'] }}</pre></td>
            </tr>
        </table>
    {% endif %}
    <hr>
    <h2>Batch Enrichment & Outreach (CSV Upload)</h2>
    <form method="post" enctype="multipart/form-data" action="/batch_enrich">
        <input type="file" name="csv_file" accept=".csv" required>
        <button type="submit">Upload & Process</button>
    </form>
    {% if batch_processing %}
        <div class="spinner">Processing batch... This may take up to a minute for large files.</div>
    {% endif %}
    {% if batch_results %}
        <h3>Batch Results</h3>
        <table>
            <tr>
                <th>Company</th><th>Contact Name</th><th>Title</th><th>LinkedIn URL</th><th>Event</th><th>Rationale</th><th>Outreach Message</th>
            </tr>
            {% for row in batch_results %}
            <tr>
                <td>{{ row['company'] }}</td>
                <td>{{ row['contact_name'] }}</td>
                <td>{{ row['title'] }}</td>
                <td>{{ row['linkedin_url'] }}</td>
                <td>{{ row['event'] }}</td>
                <td>{{ row['rationale'] }}</td>
                <td><pre style="white-space: pre-wrap;">{{ row['outreach_message'] }}</pre></td>
            </tr>
            {% endfor %}
        </table>
        <form method="post" action="/download_csv">
            <input type="hidden" name="csv_data" value="{{ csv_data }}">
            <button type="submit">Download Results as CSV</button>
        </form>
    {% endif %}
</body>
</html>
'''

def build_result_row(form_or_row):
    # Helper to ensure all fields are present
    return {
        'company': form_or_row.get('company') or form_or_row.get('company_name', ''),
        'contact_name': form_or_row.get('contact_name', ''),
        'title': form_or_row.get('title', ''),
        'linkedin_url': form_or_row.get('linkedin_url', ''),
        'event': form_or_row.get('event', ''),
        'rationale': form_or_row.get('rationale', ''),
    }

@app.route('/', methods=['GET'])
def home():
    return render_template_string(TEMPLATE, single_result=None, batch_results=None, csv_data=None, batch_processing=False)

@app.route('/enrich', methods=['POST'])
def enrich():
    # Single company/contact enrichment + outreach
    form = request.form
    row = build_result_row(form)
    try:
        enriched = enrich_company(row['company']) or {}
        # Merge enrichment fields if not already present
        for k, v in enriched.items():
            if not row.get(k):
                row[k] = v
        # Generate outreach
        outreach = generate_outreach_note(row)
        row['outreach_message'] = outreach
        return render_template_string(TEMPLATE, single_result=row, batch_results=None, csv_data=None, batch_processing=False)
    except Exception as e:
        flash(f'Error: {e}', 'error')
        return redirect(url_for('home'))

@app.route('/batch_enrich', methods=['POST'])
def batch_enrich():
    file = request.files.get('csv_file')
    if not file or not file.filename.endswith('.csv'):
        flash('Please upload a valid CSV file.', 'error')
        return redirect(url_for('home'))
    try:
        stream = io.StringIO(file.stream.read().decode('utf-8'))
        reader = csv.DictReader(stream)
        rows = [build_result_row(row) for row in reader]
        # Warn if large batch
        batch_processing = len(rows) > 10
        # Enrich and generate outreach for each row
        for row in rows:
            try:
                enriched = enrich_company(row['company']) or {}
                for k, v in enriched.items():
                    if not row.get(k):
                        row[k] = v
                outreach = generate_outreach_note(row)
                row['outreach_message'] = outreach
            except Exception as e:
                row['outreach_message'] = f"[Error: {e}]"
        # Prepare CSV for download
        output = io.StringIO()
        fieldnames = ['company', 'contact_name', 'title', 'linkedin_url', 'event', 'rationale', 'outreach_message']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
        csv_data = output.getvalue()
        return render_template_string(TEMPLATE, single_result=None, batch_results=rows, csv_data=csv_data, batch_processing=batch_processing)
    except Exception as e:
        flash(f'Error processing CSV: {e}', 'error')
        return redirect(url_for('home'))

@app.route('/download_csv', methods=['POST'])
def download_csv():
    csv_data = request.form.get('csv_data')
    if not csv_data:
        flash('No CSV data to download.', 'error')
        return redirect(url_for('home'))
    return send_file(
        io.BytesIO(csv_data.encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='enriched_outreach_results.csv'
    )

if __name__ == '__main__':
    app.run(port=5000, debug=True) 