import typer
# <XMPP CLIENT>
import metatype
import urllib


app = typer.Typer()

DRIVER = __name__.split('.', 1)[0]


# Data Model.
class Message(metatype.Dict):
    pass


@app.command()
def collect(url: str, name: str = 'default', path: str = ""):

    driver = DRIVER + '-' + urllib.parse.urlparse(url).hostname

    DRIVE = f'{driver}:{name}'

    FEED = [{"_": "<XMPP CLIENT>"}]

    if path:
        try:
            import os
            if not os.path.exists(path):
                os.makedirs(path)
            metatype.config.DATA_DIR = os.path.join(path, 'data')
        except:
            print("Can't create on selected path.")

    for item in FEED['items']:
        item['@'] = DRIVE
        item['-'] = item['link']
        # item['updated_date'] = item.get('published')

        Message(item).save()

    typer.echo("DONE: " + str(Message(item).get_filedir()))

if __name__ == "__main__":
    app()
