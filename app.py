from flask import Flask, render_template, request
from collections import Counter

import string

app = Flask(__name__)

indexes = []
paragraphs = []
words = []

class DataProcessing:
    # lower casing, removing punctuation and splitting word
    def pre_process(self, document):
        # d = dict()
        document = document.lower()
        document = document.translate(document.maketrans('', '', string.punctuation))
        # processed_document = []
        processed_document = document.split()
        return processed_document
    
    def paragraphs(self, original):
        original = original.splitlines()
        original = list(filter(None, original))
        
        for i in range(0, len(original)):
            original[i] = original[i].lower()
        
        return original


@app.route('/')
def load_app():
    return render_template('index.html')

@app.route('/load_document', methods=['POST'])
def index():
    document = request.values.get('document')
    data = DataProcessing()

    processed_paragraphs = data.paragraphs(document)
    # paragraphs = processed_paragraphs
    for para in processed_paragraphs:
        paragraphs.append(para)

    # occurence_dict = dict()
    docId = 1

    for paragraph in processed_paragraphs:
        processed = data.pre_process(paragraph)
        x = dict(Counter(processed))
        
        for key in x:
            x.update({key: [docId, x[key]]})
        
        docId = docId + 1
        indexes.append(x)

    return document

@app.route('/search', methods=['GET'])
def search():
    word = request.values.get('search')
    ans = []

    for index in indexes:
        if (index.get(word, None)):
            ans.append(paragraphs[index[word][0] - 1])
        else:
            continue

    return render_template('index.html', ans=ans)
    
    # def clear():
        # todo

# main function
if __name__ == '__main__':
    app.run(debug=True)
