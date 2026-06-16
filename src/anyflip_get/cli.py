import click
from urllib import request
import os
import random


@click.command()
@click.argument('source')
@click.option('--pages',
              type=click.INT,
              prompt='How many pages to download',
              help='Number of pages to download.')
def cli(source, pages):
    """SOURCE example: https://online.anyflip.com/xxxx/yyyy"""
    dirname = hex(random.randint(0x100000000000, 0xffffffffffff))[2:]
    os.mkdir(dirname)
    dest = os.path.join(os.curdir, dirname)
    for i in range(1, pages + 1):
        url = f'{source}/files/mobile/{i}.jpg'
        filename = f'{dest}/{i}.jpg'
        request.urlretrieve(url, filename)
        click.echo(f'Dowloaded page {i}', err=True)
    click.echo('Done!', err=True)


def main():
    cli()
