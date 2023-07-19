import click
import logging
from permifrost_concatinator.Spesification import Spesification


@click.command()
@click.option("--input", help="Input file or directory", required=True)
@click.option("--output", help="Output path and filename", required=True)
@click.option(
    "--verification", help="Verify the spesification", required=False, default=False
)
def main(input, output, verification):
    logformat = logging.Formatter(fmt="%(levelname)s - %(message)s")
    consolHandler = logging.StreamHandler()
    consolHandler.setLevel(logging.INFO)
    consolHandler.setFormatter(logformat)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(consolHandler)
    spesification = Spesification(verification=verification)
    spesification.load(input)
    spesification.identify_modules()
    spesification.identify_entities()
    spesification.generate()
    spesification.export(output)


if __name__ == "__main__":
    main()
