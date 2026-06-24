import argparse
import json

from rich.console import Console

from just_log.logger import JsonLogger

logger = JsonLogger.setup_logger()


def log_to_terminal(file):
    """Terminal color schemes and format."""

    latest: list[str] = []
    for line in file.readlines():
        log_line = json.loads(line)
        if log_line["date"].strip().split()[-1] not in latest:
            if log_line["level"] == "WARNING":
                Console().print(
                    f"{log_line['date']} [bold black on yellow]{log_line['level'][:4]}[/]\t[white]{log_line['message']}[/]"
                )
            elif log_line["level"] == "ERROR":
                Console().print(
                    f"{log_line['date']} [bold white on red]{log_line['level'][:4]}[/]\t[white]{log_line['message']}[/]"
                )
            elif log_line["level"] == "CRITICAL":
                Console().print(
                    f"{log_line['date']} [bold red on black]{log_line['level'][:4]}[/]\t[white]{log_line['message']}[/]"
                )
            else:
                Console().print(
                    f"{log_line['date']} [bold white on blue]{log_line['level'][:4]}[/]\t[white]{log_line['message']}[/]"
                )
            latest.append(log_line["date"].strip().split()[-1])


def main(path: str, loop: bool):
    """Reading log file and return created information.

    Args:
        path (str): Path of the log file
        loop (bool): True for keep reading the log file else for only once.
    """
    try:
        with open(path) as file:
            if loop:
                while True:
                    log_to_terminal(file)
            else:
                log_to_terminal(file)
    except Exception:
        logger.log(40, "Failed to read log file.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", metavar="", help="Path of the log life")
    parser.add_argument(
        "-l", "--loop", metavar="", help="Read log file in a loop", default=False
    )
    args = parser.parse_args()

    main(args.path, args.loop)
