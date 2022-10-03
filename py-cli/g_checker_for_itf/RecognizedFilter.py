import re
from typing import List, Tuple, TypedDict

from .Color import FEATURE_COLOR_STR, Color


class KamokuClass(object):
    def __init__(self, all: List[str], expect: bool = False) -> None:
        self.course_number = all[2]
        self.course_name = all[3]
        self.credit = float(all[4])
        self.grade = all[7]
        self.can_use = self.grade in ("P", "C", "A+", "A", "B", "C", "認") or (
            self.grade == "履修中" and expect
        )
        self.used = False
        self.isCount = "C0" != all[8]

    def print(self) -> None:
        data = f"{self.course_number}:{self.course_name}{Color.RESET}"
        if self.can_use:
            if self.used:
                print(f"{Color.BLUE}{data}")
            else:
                print(f"{Color.GREEN}{data}")
        else:
            print(f"{Color.RED}{data}")


class RecognizedFilterResDict(TypedDict):
    regexp_number: str
    regexp_name: str


class RecognizedFilter(object):
    name: str
    regexp_number: str
    regexp_name: str

    def __init__(self, name: str, num: str, regname: str) -> None:
        self.name = name
        self.regexp_number = num
        self.regexp_name = regname

    def genDict(self) -> RecognizedFilterResDict:
        res: RecognizedFilterResDict = {
            "regexp_number": self.regexp_number,
            "regexp_name": self.regexp_name,
        }
        return res

    def checkCourse(
        self, ls: List[KamokuClass], drop: bool = True
    ) -> Tuple[float, List[str], float]:
        res_credit = 0.0
        feature_credit = 0.0
        res_course_name: List[str] = []
        for kamoku in ls:
            flag = False
            if not self.regexp_number == r"" and re.compile(self.regexp_number).match(
                kamoku.course_number
            ):
                flag = True
            if not self.regexp_name == r"" and re.compile(self.regexp_name).match(
                kamoku.course_name
            ):
                flag = True
            data = f"{kamoku.course_name}{Color.RESET}"
            if flag:
                if not kamoku.used:
                    if kamoku.can_use:
                        kamoku.used = True
                        res_credit += kamoku.credit
                        res_course_name.append(f"{Color.GREEN}{data}")
                    elif kamoku.grade == "履修中":
                        kamoku.used = True
                        feature_credit += kamoku.credit
                        res_course_name.append(f"{FEATURE_COLOR_STR}{data}")

                    else:
                        if drop:
                            res_course_name.append(f"{Color.RED}{data}")

        return res_credit, res_course_name, feature_credit

    def print_son(self, depth: int) -> None:
        print("   " * (depth - 1) + self.name)
