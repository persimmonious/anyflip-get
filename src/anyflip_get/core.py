import click
from PIL import Image
import tempfile
import urllib
from urllib import request
import os
import sys


def download_jpgs(source, pages, dest, verbose):
    failed = []
    for i in range(1, pages + 1):
        url = f'{source}/files/mobile/{i}.jpg'
        filename = os.path.join(dest, f'{i}.jpg')
        try:
            request.urlretrieve(url, filename)
        except urllib.error.URLError:
            if verbose:
                click.echo(f'Failed to download page {i}!', err=True)
            failed.append(i)
        except urllib.error.ContentTooShortError:
            if verbose:
                click.echo(f'Failed to download page {i}!', err=True)
            failed.append(i)
        else:
            if verbose:
                click.echo(f'Downloaded page {i}.', err=True)

    return failed


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
    failed = len(download_jpgs(source, pages, dest, verbose))
    downloaded = pages - failed
    if verbose:
        click.echo(f'{downloaded} pages saved to {dest}.', err=True)
        if failed > 0:
            click.echo(f'{failed} pages failed to download.', err=True)


def download_to_pdf(source, pages, pdf_dest, verbose):
    pdf_dest = os.path.abspath(pdf_dest)
    with tempfile.TemporaryDirectory() as tmp_dir:
        failed = len(download_jpgs(source, pages, tmp_dir, verbose))
        if failed > 0:
            click.echo(f'Download incomplete! Failed to download \
                       {failed} pages. PDF creation aborted.', err=True)
            sys.exit(1)
        create_pdf(tmp_dir, pages, pdf_dest)
        if verbose:
            click.echo(f'{pdf_dest} created from {pages} pages.', err=True)
