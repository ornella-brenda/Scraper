from flask import Flask, render_template, request
import re
import requests

app = Flask(__name__)

# Expression régulière pour trouver les numéros de téléphone français
phone_regex = r"(?<!\d)(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}(?!\d)"

# Expression régulière pour trouver les adresses e-mail
email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def get_results():
    urls = request.form.get('urls')
    url_list = urls.split(',')

    all_phone_numbers = []
    all_emails = []

    for url in url_list:
        # Obtenir le contenu HTML du site web
        response = requests.get(url)
        html_content = response.text

        # Rechercher les numéros de téléphone dans le contenu HTML
        phone_numbers = set(re.findall(phone_regex, html_content))
        all_phone_numbers.extend(phone_numbers)

        # Rechercher les adresses e-mail dans le contenu HTML
        emails = set(re.findall(email_regex, html_content))
        all_emails.extend(emails)

    return render_template('results.html', phone_numbers=all_phone_numbers, emails=all_emails)

if __name__ == '__main__':
    app.run()
