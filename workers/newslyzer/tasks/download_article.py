from newslyzer.tasks import Task
from newspaper import Article as NewspaperArticle

class DownloadArticle(Task):
    name = 'Download Article'
    provides = 'download-article'
    depends = []

    def run(self, url):
        article = NewspaperArticle(url)
        article.download()
        article.parse()
        return article.text.replace('\n', ' ')
