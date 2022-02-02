import argparse
import csv
import json
import shutil
from typing import List, cast

from g_checker_for_itf import __version__

from .Dir import Dir, Level1, Level2, Level3, Level4, Level5
from .RecognizedFilter import KamokuClass, RecognizedFilter

MAX = 10000


class GchkHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    pass


def parse_arg() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="gchk",
        description="A checker if your credits meet the graduation requirements or not.",
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


def parseJSON(JSONFILENAME: str) -> Level1:
    data = json.load(open(JSONFILENAME, "r"))
    MAX_STR = "max_certificated_credit_num"
    MIN_STR = "min_certificated_credit_num"

    if len(data) == 0:
        raise ValueError("json data is empty")
    else:
        first_key, *_ = data
        init_k1, init_v1 = first_key, data[first_key]
        all = Level1(init_k1, init_v1[MAX_STR], init_v1[MIN_STR])

    for k1, v1 in data.items():
        all = Level1(k1, v1[MAX_STR], v1[MIN_STR])
        for k2, v2 in v1["leaf"].items():
            all.add(Level2(k2, v2[MAX_STR], v2[MIN_STR]))
            for k3, v3 in v2["leaf"].items():
                cf_k2 = cast(Dir, all.course_filter[k2])
                cf_k2.add(Level3(k3, v3[MAX_STR], v3[MIN_STR]))
                for k4, v4 in v3["leaf"].items():
                    cf_k3 = cast(Dir, cf_k2.course_filter[k3])
                    cf_k3.add(Level4(k4, v4[MAX_STR], v4[MIN_STR]))
                    for k5, v5 in v4["leaf"].items():
                        cf_k4 = cast(Dir, cf_k3.course_filter[k4])
                        cf_k4.add(Level5(k5, v5[MAX_STR], v5[MIN_STR]))
                        cf_k5 = cast(Dir, cf_k4.course_filter[k5])
                        cf_k5.add(
                            RecognizedFilter(
                                k5,
                                v5["leaf"]["regexp_number"],
                                v5["leaf"]["regexp_name"],
                            )
                        )

    return all


def gp(ls: List[KamokuClass]) -> None:
    gps = 0.0
    credit_sum = 0.0
    grade_points = {"A+": 4.3, "A": 4, "B": 3, "C": 2, "D": 0}
    target_kams = [kam for kam in ls if kam.can_use and kam.isCount]
    for kam in target_kams:
        for grade, point in grade_points.items():
            if kam.grade == grade:
                gps += point * kam.credit
                credit_sum += kam.credit
    gpa = gps / credit_sum
    print(f"GPA = GPS/CreditSum : {gpa:1.5} = {gps}/{credit_sum}")


def readCSV(CSVFILENAME: str, expect: bool) -> List[KamokuClass]:
    memo = []
    with open(CSVFILENAME) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i != 0:
                memo.append(KamokuClass(row, expect))

    for t in memo:
        if t.course_name == "オートマトンと形式言語" and t.course_number == "GB21601":
            t.course_number = "GB20401"
        if t.course_name == "プログラム理論" and t.course_number == "GB21111":
            t.course_number = "GB20501"
        if t.course_name == "プログラミングチャレンジ" and t.course_number == "GB21802":
            t.course_number = "GB20602"
        if t.course_name == "プログラム言語処理" and t.course_number == "GB31301":
            t.course_number = "GB30504"
        if t.course_name == "ソフトウェア工学" and t.course_number == "GB31501":
            t.course_number = "GB30601"
        if t.course_name == "情報理論" and t.course_number == "GB12501":
            t.course_number = "GB40601"

    return memo


def readNameFromCSV(CSVFILENAME: str) -> str:
    reader = csv.reader(open(CSVFILENAME, "r"))
    for row in reader:
        if reader.line_num == 1:
            return row[1]
    else:
        raise ValueError("CSV is maybe blank.")


def genJSON(v0: Level1, input_csv: str, requirements: str) -> None:
    res = {}
    res[v0.name] = v0.genDict()
    for v1 in v0.course_filter.values():
        if not isinstance(v1, Dir):
            continue
        res[v0.name]["leaf"][v1.name] = v1.genDict()
        for v2 in v1.course_filter.values():
            if not isinstance(v2, Dir):
                continue
            res[v0.name]["leaf"][v1.name]["leaf"][v2.name] = v2.genDict()
            for v3 in v2.course_filter.values():
                if not isinstance(v3, Dir):
                    continue
                res[v0.name]["leaf"][v1.name]["leaf"][v2.name]["leaf"][
                    v3.name
                ] = v3.genDict()
                for v4 in v3.course_filter.values():
                    if not isinstance(v4, Dir):
                        continue
                    res[v0.name]["leaf"][v1.name]["leaf"][v2.name]["leaf"][v3.name][
                        "leaf"
                    ][v4.name] = v4.genDict()
                    for v5 in v4.course_filter.values():
                        if not isinstance(v5, Dir):
                            continue
                        res[v0.name]["leaf"][v1.name]["leaf"][v2.name]["leaf"][v3.name][
                            "leaf"
                        ][v4.name]["leaf"] = v5.genDict()
    basename = input_csv.replace(".csv", "")
    with open(f"{basename}-{requirements}", "w") as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
    # with open("tani/src/grade.json", "w") as f:
    #     json.dump(res, f, ensure_ascii=False, indent=4)


def main() -> None:
    args = parse_arg()
    CSVFILENAME = args.input
    JSONFILENAME = args.requirements

    coins20 = parseJSON(JSONFILENAME)
    if args.name:
        print(CSVFILENAME, readNameFromCSV(CSVFILENAME))
    kamoku = readCSV(CSVFILENAME, args.expect)
    coins20.check(kamoku)
    coins20.print_son()
    if args.gpa:
        gp(kamoku)
    if args.save:
        genJSON(coins20, args.input, args.requirements)


if __name__ == "__main__":
    main()
