from newslyzer.tasks import Task

class DownloadArticle(Task):
    name = 'Download Task'
    provides = 'download-task'
    depends = []

    def run(self, url):
        print('Download article {}'.format(url))
        return '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sodales erat in bibendum fermentum. Nam laoreet aliquam justo.
        Aenean quis tellus in sapien porta laoreet. Phasellus neque nunc, viverra sed hendrerit quis, posuere et augue.
        Donec ac metus porttitor, commodo diam sit amet, faucibus purus.'''
        # signature('process-sentences', args=(text, )).apply_async()

