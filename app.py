from config import Config
from utils.feed_parser import init_cache, get_all_feeds
from flask import Flask, render_template, request # type: ignore


app = Flask(__name__)
app.config.from_object(Config)
init_cache(app)

@app.route('/')
def index():
    all_articles = get_all_feeds()
    page = int(request.args.get('page', 1))
    per_page = 10
    total = len(all_articles)
    start = (page-1)*per_page
    end = start + per_page
    articles = all_articles[start:end]

    return render_template(
      'index.html',
      articles=articles,
      page=page,
      total=total,
      per_page=per_page
    )

@app.route('/feed/<source>')
def feed(source):
    all_articles = [a for a in get_all_feeds() if a['source'] == source]
    page = int(request.args.get('page', 1))
    per_page = 10
    total = len(all_articles)
    start = (page-1)*per_page
    end = start + per_page
    articles = all_articles[start:end]

    return render_template(
      'feed.html',
      articles=articles,
      source=source,
      page=page,
      total=total,
      per_page=per_page
    )
  
@app.route('/search')
def search():
    q = request.args.get('q', '').lower()
    all_articles = get_all_feeds()
    filtered = [
      a for a in all_articles
      if q in a['title'].lower() or q in a.get('snippet', '').lower()
    ]
    page = int(request.args.get('page', 1))
    per_page = 10
    total = len(filtered)
    start = (page-1)*per_page
    end = start + per_page
    articles = filtered[start:end]

    return render_template('index.html',
                           articles=articles,
                           page=page,
                           total=total,
                           per_page=per_page)

  

if __name__ == '__main__':
    app.run(debug=True)
