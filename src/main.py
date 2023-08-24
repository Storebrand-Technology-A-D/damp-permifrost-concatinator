import click
import logging
from permifrost_concatinator.Spesification import Spesification
from permifrost_concatinator.Permission_state import Permission_state
from permifrost_concatinator.loader_local_file import Local_file_loader


@click.command()
@click.option("--input", help="Input file or directory", required=True)
@click.option("--output", help="Output path and filename", required=True)
@click.option(
    "--verification", help="Verify the spesification", required=False, default=False
)
@click.option(
    "--role_generation",
    help="Generate AR roles based on functional roles and databases",
    required=False,
    default=False,
)
@click.option(
    "--plan",
    help="output planned changes based on spec comparison",
    required=False,
    default=False,
)
@click.option(
    "--plan_output", help="path to plan output file", required=False, default=""
)
@click.option(
    "--apply",
    help="apply planned changes based on spec comparison",
    required=False,
    default=False,
)
@click.option("--state", help="path to state file", required=False, default="")
def main(input, output, verification, plan, apply, state, role_generation, plan_output):
    logformat = logging.Formatter(fmt="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    consolHandler = logging.StreamHandler()
    consolHandler.setLevel(logging.INFO)
    consolHandler.setFormatter(logformat)

    fileHandler = logging.FileHandler('debug.log')
    fileHandler.setLevel(logging.DEBUG)
    fileHandler.setFormatter(logformat)


    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(consolHandler)
    logger.addHandler(fileHandler)




    spesification = Spesification(
        verification=verification, generate_roles=role_generation
    )
    spesification.load(input)
    spesification.identify_modules()
    spesification.identify_entities()
    spesification.generate()
    if plan == True:
        try:
            current_state = Permission_state()
            current_state.load(Local_file_loader, state)
        except:
            logger.error("Failed to load state")

        new_state = Permission_state(spesification).generate()
        new_state.compare(current_state)
        new_state.plan(plan_output)

    spesification.export(output)

    if apply == True:
        try:
            new_state = Permission_state(spesification).generate()
            new_state.export(state)
        except:
            logger.error("Failed to update state file")


if __name__ == "__main__":
    main()
