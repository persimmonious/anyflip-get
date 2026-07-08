import click
import sys
import core


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
        core.download_to_pdf(source, pages, output, verbose)
    else:
        core.download_as_pages(source, pages, output, verbose)
