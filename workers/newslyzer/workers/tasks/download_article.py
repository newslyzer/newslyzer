from . import Task
from newspaper import Article

class DownloadArticle(Task):
    name = 'Download Article'
    provides = 'download-article'
    depends = []

    def run(self, url):
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()

        return {
            'image': article.top_image,
            'title': article.title,
            'language': article.meta_lang,
            'description': article.meta_description,
            'summary': article.summary,
            'url': url,
            'sourceName': article.meta_data.get('og', {}).get('site_name', None),
            'sourceUrl': article.source_url,
            'text': article.text.replace('\n', ' ')
        }
