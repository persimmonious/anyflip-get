import click
import urllib
from urllib import request
import os


def download(source, pages, output, verbose):
    dirname = output
    if not dirname:
        dirname = os.getcwd()
    dirname = os.path.abspath(dirname)
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    downloaded = 0
    for i in range(1, pages + 1):
        url = f'{source}/files/mobile/{i}.jpg'
        filename = os.path.join(dirname, f'{i}.jpg')
        try:
            request.urlretrieve(url, filename)
        except urllib.error.URLError as e:
            raise e
        except urllib.error.ContentTooShortError as e:
            raise e
        else:
            downloaded += 1
        if verbose:
            click.echo(f'Dowloaded page {i}', err=True)
    if verbose:
        click.echo(f'{downloaded} pages saved to {dirname}', err=True)


@click.command()
@click.argument('source')
@click.option('--pages',
              type=click.INT,
              prompt='How many pages to download',
              help='Number of pages to download.')
@click.option('--output',
              type=click.Path(writable=True),
              help='Where to save the downloaded files')
@click.option('--verbose',
              is_flag=True,
              help='Verbose output')
def cli(source, pages, output, verbose):
    """SOURCE example: https://online.anyflip.com/xxxx/yyyy"""
    download(source, pages, output, verbose)


def main():
    cli()
