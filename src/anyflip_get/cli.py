import click
import urllib
from urllib import request
import os
import sys
from PIL import Image
import tempfile


def download_jpgs(source, pages, dest, verbose):
    downloaded = 0
    for i in range(1, pages + 1):
        url = f'{source}/files/mobile/{i}.jpg'
        filename = os.path.join(dest, f'{i}.jpg')
        try:
            request.urlretrieve(url, filename)
        except urllib.error.URLError as e:
            raise e
        except urllib.error.ContentTooShortError as e:
            raise e
        else:
            downloaded += 1
            if verbose:
                click.echo(f'Dowloaded page {i}.', err=True)

    return downloaded


def create_pdf(tmp_dir, pages, pdf_dest):
    paths = (os.path.join(tmp_dir, f'{i}.jpg') for i in range(1, pages + 1))
    jpegs = [Image.open(p).convert("RGB") for p in paths]
    jpegs[0].save(pdf_dest, "PDF", save_all=True, append_images=jpegs[1:])


def download_as_pages(source, pages, output, verbose):
    dest = output
    if not dest:
        dest = os.getcwd()
    dest = os.path.abspath(dest)
    if not os.path.exists(dest):
        os.mkdir(dest)
    downloaded = download_jpgs(source, pages, dest, verbose)
    failed = pages - downloaded
    if verbose:
        click.echo(f'{downloaded} pages saved to {dest}.', err=True)
        if failed > 0:
            click.echo(f'{failed} pages failed to download.', err=True)


def download_to_pdf(source, pages, pdf_dest, verbose):
    pdf_dest = os.path.abspath(pdf_dest)
    with tempfile.TemporaryDirectory() as tmp_dir:
        downloaded = download_jpgs(source, pages, tmp_dir, verbose)
        failed = pages - downloaded
        if failed > 0:
            click.echo('Download incomplete! PDF creation aborted.', err=True)
            sys.exit(1)
        create_pdf(tmp_dir, pages, pdf_dest)
        if verbose:
            click.echo(f'{pdf_dest} created from {pages} pages.', err=True)


@click.command()
@click.argument('source')
@click.option('--pages', '-p',
              type=click.INT,
              prompt='How many pages to download',
              help='Number of pages to download.')
@click.option('--output', '-o',
              type=click.Path(writable=True),
              help='Where to save the downloaded files')
@click.option('--verbose', '-v',
              is_flag=True,
              help='Verbose output')
@click.option('--pdf', '-P',
              is_flag=True,
              help='Combine the downloaded pages into a PDF')
@click.version_option()
def cli(source, pages, output, verbose, pdf):
    """SOURCE example: https://online.anyflip.com/xxxx/yyyy"""
    if pdf and not output:
        click.echo(
            "Error! File name must be specified when using --pdf flag.",
            err=True)
        sys.exit(1)
    if pdf:
        download_to_pdf(source, pages, output, verbose)
    else:
        download_as_pages(source, pages, output, verbose)


def main():
    cli()
