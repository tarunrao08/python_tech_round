import re
import requests
from bs4 import BeautifulSoup
from collections import Counter
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_word_frequency(url):
    # Fetch the webpage content
    response = requests.get(url)
    content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Extract text from the webpage
    text = soup.get_text()

    # Tokenize the text into words
    words = re.findall(r'\b[A-Za-z]+\b', text)

    # Count the frequency of each word
    word_frequency = Counter(words)

    return word_frequency

@app.route('/analyze-website', methods=['POST'])
def analyze_website():
    url = request.json.get('url')

    if not url:
        return jsonify({'error': 'URL is required.'}), 400

    try:
        word_frequency = get_word_frequency(url)
        return jsonify(word_frequency), 200
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
