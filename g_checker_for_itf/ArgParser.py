import argparse
import shutil

from g_checker_for_itf import __version__


class GchkHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def parse_arg() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="gchk",
        description="A checker that your credit can meet the graduation requirements.",
        formatter_class=(
            lambda prog: GchkHelpFormatter(
                prog,
                **{
                    "width": shutil.get_terminal_size(fallback=(120, 50)).columns,
                    "max_help_position": 30,
                },
            )
        ),
    )
    parser.add_argument(
        "-i",
        "--input",
        help="target file from twins (UTF-8, CSV)",
        default="sample.csv",
    )
    parser.add_argument(
        "-r", "--requirements", help="requirements file", default="coins20.json"
    )
    parser.add_argument("-g", "--gpa", help="print GPA", action="store_true")
    parser.add_argument("-d", "--drop", help="print drop credit", action="store_false")
    parser.add_argument("-n", "--name", help="print name and id", action="store_true")
    parser.add_argument("-s", "--save", help="save as JSON", action="store_true")
    parser.add_argument("-e", "--expect", help="count 履修中", action="store_true")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser.parse_args()
