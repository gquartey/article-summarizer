from flask import Flask, render_template, flash, request
from articleAnalysis import summarize_url
from textExtraction import get_title

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarizer', methods=['POST'])
def summarize():

    # get the article link from the form 
    article_link = request.form['article_url']

    # get article title
    try:
        title = get_title(article_link)
    except:
        # this means there was an error trying to query the page 
        error = "Looks like the link you gave us was invalid, try agian"
        return render_template('index.html',error=error)
    # get the most important articles
    sentences = summarize_url(article_link)

    return render_template('results.html',sentences=sentences,title=title)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
