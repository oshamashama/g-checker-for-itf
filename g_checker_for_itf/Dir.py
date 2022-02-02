from typing import Dict, List, Tuple, TypedDict, Union, cast

from .Color import FAIL_COLOR_STR, FEATURE_COLOR_STR, OK_COLOR_STR, RESET_COLOR_STR
from .RecognizedFilter import KamokuClass, RecognizedFilter


class DirResDict(TypedDict):
    max_certificated_credit_num: int
    now_certificated_credit_num: int
    feature_certificated_credit_num: int
    min_certificated_credit_num: int
    # cyclic definition
    leaf: "DirResDict"  # type: ignore[misc]


class Dir(object):
    def __init__(
        self, name: str, max: int, min: int, is_frame: bool, parent_depth: int
    ) -> None:
        self.name = name
        self.max_certificated_credit_num = max
        self.now_certificated_credit_num = 0.0
        self.feature_certificated_credit_num = 0.0
        self.min_certificated_credit_num = min
        self.is_frame = is_frame  # if is_frame, filter_mode else dir_mode
        self.course_filter: Dict[str, Union["Dir", RecognizedFilter]] = {}
        self.dir_depth = parent_depth
        self.now_certificated_credit_name: List[str] = []

    def get_indent(self) -> int:
        return self.dir_depth - 1

    def print_son(self) -> None:
        r_pad = "".rjust(self.get_indent(), "　")
        l_pad = self.name.ljust(5, "　").ljust(24 - self.get_indent(), "　")
        credit_total = (
            self.now_certificated_credit_num + self.feature_certificated_credit_num
        )
        if self.now_certificated_credit_num >= self.min_certificated_credit_num:
            print(
                f"{OK_COLOR_STR}{r_pad}{l_pad}",
                f"{self.now_certificated_credit_num:5.1f}{FEATURE_COLOR_STR}"
                f"({credit_total:5.1f}){OK_COLOR_STR}/{self.min_certificated_credit_num:5.1f}{RESET_COLOR_STR}",
            )
        else:
            print(
                f"{FAIL_COLOR_STR}{r_pad}{l_pad}",
                f"{self.now_certificated_credit_num:5.1f}{FEATURE_COLOR_STR}"
                f"({credit_total:5.1f}){FAIL_COLOR_STR}/{self.min_certificated_credit_num:5.1f}{RESET_COLOR_STR}",
            )
        for item in self.course_filter.values():
            if not isinstance(item, Dir):
                continue
            if item.is_frame:
                item.print_son()
            else:
                item.print_ls()

    def namelist(self) -> str:
        return " ".join(self.now_certificated_credit_name)

    def print_ls(self) -> None:
        r_pad = "".rjust(self.get_indent(), "　")
        l_pad = self.name.ljust(5, "　").ljust(24 - self.get_indent(), "　")
        credit_total = (
            self.now_certificated_credit_num + self.feature_certificated_credit_num
        )
        if self.now_certificated_credit_num >= self.min_certificated_credit_num:
            print(
                f"{OK_COLOR_STR}{r_pad}{l_pad}",
                f"{self.now_certificated_credit_num:5.1f}"
                f"{FEATURE_COLOR_STR}({credit_total:5.1f})"
                f"{OK_COLOR_STR}/{self.min_certificated_credit_num:5.1f}{RESET_COLOR_STR}",
                self.namelist(),
            )
        else:
            print(
                f"{FAIL_COLOR_STR}{r_pad}{l_pad}",
                f"{self.now_certificated_credit_num:5.1f}"
                f"{FEATURE_COLOR_STR}({credit_total:5.1f})"
                f"{FAIL_COLOR_STR}/{self.min_certificated_credit_num:5.1f}{RESET_COLOR_STR}",
                self.namelist(),
            )

    def genDict(self) -> DirResDict:
        res = {
            "max_certificated_credit_num": self.max_certificated_credit_num,
            "now_certificated_credit_num": self.now_certificated_credit_num,
            "feature_certificated_credit_num": self.feature_certificated_credit_num,
            "min_certificated_credit_num": self.min_certificated_credit_num,
            "leaf": {},
        }
        return cast(DirResDict, res)
        # return {self.name:res}

    def check(self, ls: List[KamokuClass]) -> Tuple[float, float]:
        self.now_certificated_credit_num = 0.0
        if self.is_frame:  # 下を見に行く
            for item in self.course_filter.values():
                if not isinstance(item, Dir):
                    continue
                res_d = item.check(ls)
                self.now_certificated_credit_num += res_d[0]
                self.feature_certificated_credit_num += res_d[1]
        else:  # RecoFil について
            for item in self.course_filter.values():
                if not isinstance(item, RecognizedFilter):
                    continue
                res_f = item.checkCourse(ls)
                self.now_certificated_credit_num += res_f[0]
                if res_f[1] != []:
                    self.now_certificated_credit_name += res_f[1]
                    self.feature_certificated_credit_num += res_f[2]
        return self.now_certificated_credit_num, self.feature_certificated_credit_num

    def add(self, item: Union["Dir", RecognizedFilter]) -> None:
        self.course_filter[item.name] = item


class Level1(Dir):
    def __init__(self, name: str, max: int, min: int) -> None:
        super().__init__(name, max, min, True, 1)


class Level2(Dir):
    def __init__(self, name: str, max: int, min: int) -> None:
        super().__init__(name, max, min, True, 2)


class Level3(Dir):
    def __init__(self, name: str, max: int, min: int) -> None:
        super().__init__(name, max, min, True, 3)


class Level4(Dir):
    def __init__(self, name: str, max: int, min: int) -> None:
        super().__init__(name, max, min, True, 4)


class Level5(Dir):
    def __init__(self, name: str, max: int, min: int) -> None:
        super().__init__(name, max, min, False, 5)
