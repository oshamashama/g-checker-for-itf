import json
from ast import And, arg
from asyncore import read
from cgitb import reset
from mimetypes import init
import sys
import csv
import pprint
import re
from tabnanny import check
from tokenize import String
from unicodedata import name
from turtle import color
from xml.sax.handler import feature_external_ges
from xmlrpc.client import boolean

from numpy import number
MAX = 10000


class Color:
	BLACK          = '\033[30m'#(文字)黒
	RED            = '\033[31m'#(文字)赤
	GREEN          = '\033[32m'#(文字)緑
	YELLOW         = '\033[33m'#(文字)黄
	BLUE           = '\033[34m'#(文字)青
	MAGENTA        = '\033[35m'#(文字)マゼンタ
	CYAN           = '\033[36m'#(文字)シアン
	WHITE          = '\033[37m'#(文字)白
	COLOR_DEFAULT  = '\033[39m'#文字色をデフォルトに戻す
	BOLD           = '\033[1m'#太字
	UNDERLINE      = '\033[4m'#下線
	INVISIBLE      = '\033[08m'#不可視
	REVERCE        = '\033[07m'#文字色と背景色を反転
	BG_BLACK       = '\033[40m'#(背景)黒
	BG_RED         = '\033[41m'#(背景)赤
	BG_GREEN       = '\033[42m'#(背景)緑
	BG_YELLOW      = '\033[43m'#(背景)黄
	BG_BLUE        = '\033[44m'#(背景)青
	BG_MAGENTA     = '\033[45m'#(背景)マゼンタ
	BG_CYAN        = '\033[46m'#(背景)シアン
	BG_WHITE       = '\033[47m'#(背景)白
	BG_DEFAULT     = '\033[49m'#背景色をデフォルトに戻す
	RESET          = '\033[0m'#全てリセット

OK_COLOR_STR = f'{Color.RESET}{Color.GREEN}{Color.BOLD}'
FEATURE_COLOR_STR = f'{Color.RESET}{Color.CYAN}'
FAIL_COLOR_STR = f'{Color.RESET}{Color.RED}{Color.BOLD}'
RESET_COLOR_STR = f'{Color.RESET}'




class Dir():
    name:String
    max_certificated_credit_num:int
    now_certificated_credit_num:int
    feature_certificated_credit_num:int
    min_certificated_credit_num:int
    is_frame:bool   # if is_frame, filter_mode else dir_mode
    course_filter:dict
    dir_depth:int
    now_certificated_credit_name:list

    def __init__(self, name:String, max:int, min:int, is_frame:boolean, parent_depth:int):
        self.name = name
        self.max_certificated_credit_num = max
        self.now_certificated_credit_num = 0
        self.feature_certificated_credit_num = 0
        self.min_certificated_credit_num = min
        self.is_frame = is_frame
        self.course_filter = {}
        self.dir_depth = parent_depth
        self.now_certificated_credit_name = []
        
    def get_indent(self):
        return (self.dir_depth - 1)*1

    def print_son(self):
        if(self.now_certificated_credit_num >= self.min_certificated_credit_num):
            print("{}{}{} {:5.1f}{}({:5.1f}){}/{:5.1f}{}".format(OK_COLOR_STR,"".rjust(self.get_indent(), "　"), self.name.ljust(5, "　").ljust(24 - self.get_indent(), "　"), self.now_certificated_credit_num, FEATURE_COLOR_STR, self.now_certificated_credit_num + self.feature_certificated_credit_num, OK_COLOR_STR, self.min_certificated_credit_num, RESET_COLOR_STR))
        else:
            print("{}{}{} {:5.1f}{}({:5.1f}){}/{:5.1f}{}".format(FAIL_COLOR_STR,"".rjust(self.get_indent(), "　"), self.name.ljust(5, "　").ljust(24 - self.get_indent(), "　"), self.now_certificated_credit_num, FEATURE_COLOR_STR, self.now_certificated_credit_num + self.feature_certificated_credit_num, FAIL_COLOR_STR, self.min_certificated_credit_num, RESET_COLOR_STR))
        for item in self.course_filter.values():
            if item.is_frame:
                item.print_son()
            else:
                item.print_ls()

    def namelist(self):
        return ' '.join(self.now_certificated_credit_name)

    def print_ls(self):
        if(self.now_certificated_credit_num >= self.min_certificated_credit_num):
            print("{}{}{} {:5.1f}{}({:5.1f}){}/{:5.1f}{} {}".format(OK_COLOR_STR,"".rjust(self.get_indent(), "　"), self.name.ljust(5, "　").ljust(24 - self.get_indent(), "　"), self.now_certificated_credit_num, FEATURE_COLOR_STR, self.now_certificated_credit_num + self.feature_certificated_credit_num, OK_COLOR_STR, self.min_certificated_credit_num, RESET_COLOR_STR, self.namelist()))
        else:
            print("{}{}{} {:5.1f}{}({:5.1f}){}/{:5.1f}{} {}".format(FAIL_COLOR_STR,"".rjust(self.get_indent(), "　"), self.name.ljust(5, "　").ljust(24 - self.get_indent(), "　"), self.now_certificated_credit_num, FEATURE_COLOR_STR, self.now_certificated_credit_num + self.feature_certificated_credit_num, FAIL_COLOR_STR, self.min_certificated_credit_num, RESET_COLOR_STR, self.namelist()))

    def genDict(self):
        res = {
            "max_certificated_credit_num":self.max_certificated_credit_num,
            "min_certificated_credit_num":self.min_certificated_credit_num,
            "leaf":{}
        }
        return res
        # return {self.name:res}

    def check(self, ls) -> int:
        self.now_certificated_credit_num = 0
        if self.is_frame: # 下を見に行く
            for item in self.course_filter.values():
                res = item.check(ls)
                self.now_certificated_credit_num += res[0]
                self.feature_certificated_credit_num += res[1]
        else: # RecoFil について
            for item in self.course_filter.values():
                res = item.checkCourse(ls)
                self.now_certificated_credit_num += res[0]
                if not res[1] == "":
                    self.now_certificated_credit_name += res[1]
                    self.feature_certificated_credit_num += res[2]
        return self.now_certificated_credit_num, self.feature_certificated_credit_num

    def add(self, item):
        self.course_filter[item.name] = item

class RecognizedFilter():
    name:str
    regexp_number:str
    regexp_name:str
    def __init__(self, name, num, regname) -> None:
        self.name = name
        self.regexp_number = num
        self.regexp_name = regname
    
    def checkCourse(self, ls):
        res_credit = 0
        feature_credit = 0
        res_course_name = []
        for kamoku in ls:
            flag = False
            if not self.regexp_number == r"" and re.compile(self.regexp_number).match(kamoku.course_number):
                flag = True
            if not self.regexp_name == r"" and re.compile(self.regexp_name).match(kamoku.course_name):
                flag = True
            if flag:
                if not kamoku.used:
                    if kamoku.can_use:
                        kamoku.used = True
                        res_credit += kamoku.credit
                        res_course_name.append("{}{}{}".format(Color.GREEN, kamoku.course_name, Color.RESET))
                    elif kamoku.grade == "履修中":
                        kamoku.used = True
                        feature_credit += kamoku.credit
                        res_course_name.append("{}{}{}".format(FEATURE_COLOR_STR, kamoku.course_name, Color.RESET))
                    else:
                        res_course_name.append("{}{}{}".format(Color.RED, kamoku.course_name, Color.RESET))
        return res_credit, res_course_name, feature_credit
    
    def print_son(self, depth):
        print("{}{}".format("   "*(depth - 1),self.name))


class Level5(Dir):
    def __init__(self, name, max, min):
        super().__init__(name, max, min, False, 5)

class Level4(Dir):
    def __init__(self, name, max, min):
        super().__init__(name, max, min, True, 4)

class Level3(Dir):
    def __init__(self, name, max, min):
        super().__init__(name, max, min, True, 3)

class Level2(Dir):
    def __init__(self, name, max, min):
        super().__init__(name, max, min, True, 2)

class Level1(Dir):
    def __init__(self, name, max, min):
        super().__init__(name, max, min, True, 1)

def genCoins20() -> Level1:
    all = Level1("情報科学類", 125, 125)
    all.add(Level2("専門", 52, 52))
    all.course_filter["専門"].add(Level3("", 52, 52))
    all.course_filter["専門"].course_filter[""].add(Level4("必修", 16, 16))
    all.course_filter["専門"].course_filter[""].course_filter["必修"].add(Level5("主専攻実験Ａ／Ｂ", 6, 6))
    all.course_filter["専門"].course_filter[""].course_filter["必修"].course_filter["主専攻実験Ａ／Ｂ"].add(RecognizedFilter(
        "主専攻実験Ａ／Ｂ",
        r"^GB[234]6[45]03$",
        r""
    ))
    all.course_filter["専門"].course_filter[""].course_filter["必修"].add(Level5("卒業研究Ａ／Ｂ", 6, 6))
    all.course_filter["専門"].course_filter[""].course_filter["必修"].course_filter["卒業研究Ａ／Ｂ"].add(RecognizedFilter(
        "卒業研究Ａ／Ｂ",
        r"^GB199[4589]8$",
        r""
    ))
    all.course_filter["専門"].course_filter[""].course_filter["必修"].add(Level5("専門語学Ａ／Ｂ", 4, 4))
    all.course_filter["専門"].course_filter[""].course_filter["必修"].course_filter["専門語学Ａ／Ｂ"].add(RecognizedFilter(
        "専門語学Ａ／Ｂ",
        r"^GB190[4578]1$",
        r""
    ))
    all.course_filter["専門"].course_filter[""].add(Level4("選択", 36, 36))
    all.course_filter["専門"].course_filter[""].course_filter["選択"].add(Level5("ＧＢｘ０～", MAX, 18))
    all.course_filter["専門"].course_filter[""].course_filter["選択"].course_filter["ＧＢｘ０～"].add(RecognizedFilter(
        "ＧＢｘ０～",
        r"^GB[234]0.*$",
        r""
    ))
    all.course_filter["専門"].course_filter[""].course_filter["選択"].add(Level5("ＧＢ２３４／ジョットク", 18, 0))
    all.course_filter["専門"].course_filter[""].course_filter["選択"].course_filter["ＧＢ２３４／ジョットク"].add(RecognizedFilter(
        "ＧＢ２３４／ジョットク",
        r"^GB[234][^0].*$",
        r"^情報.*特別.*演習"
    ))
    all.add(Level2("専門基礎", 50, 50))
    all.course_filter["専門基礎"].add(Level3("", 50, 50))
    all.course_filter["専門基礎"].course_filter[""].add(Level4("必修", 26, 26))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("線形代数Ａ", 2, 2))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["線形代数Ａ"].add(RecognizedFilter(
        "線形代数Ａ",
        r"",
        r"^線形代数A$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("線形代数Ｂ", 2, 2))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["線形代数Ｂ"].add(RecognizedFilter(
        "線形代数Ｂ",
        r"",
        r"^線形代数B$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("微分積分Ａ", 2, 2))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["微分積分Ａ"].add(RecognizedFilter(
        "微分積分Ａ",
        r"",
        r"^微分積分A$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("微分積分Ｂ", 2, 2))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["微分積分Ｂ"].add(RecognizedFilter(
        "微分積分Ｂ",
        r"",
        r"^微分積分B$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("情報数学Ａ", 2, 2))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["情報数学Ａ"].add(RecognizedFilter(
        "情報数学Ａ",
        r"",
        r"^情報数学A$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("専門英語基礎", 1, 1))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["専門英語基礎"].add(RecognizedFilter(
        "専門英語基礎",
        r"",
        r"^専門英語基礎$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("プロ入", 3, 3))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["プロ入"].add(RecognizedFilter(
        "プロ入",
        r"",
        r"^プログラミング入門$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("コンプロ", 3, 3))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["コンプロ"].add(RecognizedFilter(
        "コンプロ",
        r"",
        r"^コンピュータとプログラミング$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("ＤＳＡ", 3, 3))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["ＤＳＡ"].add(RecognizedFilter(
        "ＤＳＡ",
        r"",
        r"^データ構造とアルゴリズム$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("ＤＳＡＬ", 2, 2))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["ＤＳＡＬ"].add(RecognizedFilter(
        "ＤＳＡＬ",
        r"",
        r"^データ構造とアルゴリズム実験$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("論理回路", 2, 2))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["論理回路"].add(RecognizedFilter(
        "論理回路",
        r"",
        r"^論理回路$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].add(Level5("論理回路演習", 2, 2))
    all.course_filter["専門基礎"].course_filter[""].course_filter["必修"].course_filter["論理回路演習"].add(RecognizedFilter(
        "論理回路演習",
        r"",
        r"^(論理回路演習|論理回路実験)$"
    ))
    all.course_filter["専門基礎"].course_filter[""].add(Level4("選択", 24, 24))
    all.course_filter["専門基礎"].course_filter[""].course_filter["選択"].add(Level5("実質必修のやつ", MAX, 10))
    all.course_filter["専門基礎"].course_filter[""].course_filter["選択"].course_filter["実質必修のやつ"].add(RecognizedFilter(
        "実質必修のやつ",
        r"",
        r"^(確率論|統計学|数値計算法|論理と形式化|電磁気学|論理システム|論理システム演習)$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["選択"].add(Level5("ＣＳ　ｉｎ　Ｅｎｇｌｉｓｈ", MAX, 2))
    all.course_filter["専門基礎"].course_filter[""].course_filter["選択"].course_filter["ＣＳ　ｉｎ　Ｅｎｇｌｉｓｈ"].add(RecognizedFilter(
        "ＣＳ　ｉｎ　Ｅｎｇｌｉｓｈ",
        r"",
        r"^Computer.*Science.*in.*English.*[AB]$"
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["選択"].add(Level5("ＧＢ１～", MAX, 0))
    all.course_filter["専門基礎"].course_filter[""].course_filter["選択"].course_filter["ＧＢ１～"].add(RecognizedFilter(
        "ＧＢ１～",
        r"^GB1.*$",
        r""
    ))
    all.course_filter["専門基礎"].course_filter[""].course_filter["選択"].add(Level5("ＧＡ１～", MAX, 8))
    all.course_filter["専門基礎"].course_filter[""].course_filter["選択"].course_filter["ＧＡ１～"].add(RecognizedFilter(
        "ＧＡ１～",
        r"^GA1.*$",
        r""
    ))
    all.add(Level2("基礎", 23, 23))
    all.course_filter["基礎"].add(Level3("共通", 17, 13))
    all.course_filter["基礎"].course_filter["共通"].add(Level4("必修", 12, 12))
    all.course_filter["基礎"].course_filter["共通"].course_filter["必修"].add(Level5("総合科目", 2, 2))
    all.course_filter["基礎"].course_filter["共通"].course_filter["必修"].course_filter["総合科目"].add(RecognizedFilter(
        "総合科目",
        r"",
        r"^(学問への誘い|フレッシュマン・セミナー)$"
    ))
    all.course_filter["基礎"].course_filter["共通"].course_filter["必修"].add(Level5("体育", 2, 2))
    all.course_filter["基礎"].course_filter["共通"].course_filter["必修"].course_filter["体育"].add(RecognizedFilter(
        "体育",
        r"^2[12].*$",
        r""
    ))
    all.course_filter["基礎"].course_filter["共通"].course_filter["必修"].add(Level5("外国語（英語）", 4, 4))
    all.course_filter["基礎"].course_filter["共通"].course_filter["必修"].course_filter["外国語（英語）"].add(RecognizedFilter(
        "外国語（英語）",
        r"^31.*$",
        r"(^English Presentation Skills I+$)"
    ))
    all.course_filter["基礎"].course_filter["共通"].course_filter["必修"].add(Level5("情報", 4, 4))
    all.course_filter["基礎"].course_filter["共通"].course_filter["必修"].course_filter["情報"].add(RecognizedFilter(
        "情報",
        r"^6.*$",
        r""
    ))
    all.course_filter["基礎"].course_filter["共通"].add(Level4("選択", 5, 1))
    all.course_filter["基礎"].course_filter["共通"].course_filter["選択"].add(Level5("総合科目（学士基盤科目）", MAX, 1))
    all.course_filter["基礎"].course_filter["共通"].course_filter["選択"].course_filter["総合科目（学士基盤科目）"].add(RecognizedFilter(
        "総合科目（学士基盤科目）",
        r"^1.*$",
        r""
    ))
    all.course_filter["基礎"].course_filter["共通"].course_filter["選択"].add(Level5("体育／外国語／国語／芸術", MAX, 0))
    all.course_filter["基礎"].course_filter["共通"].course_filter["選択"].course_filter["体育／外国語／国語／芸術"].add(RecognizedFilter(
        "体育／外国語／国語／芸術",
        r"aaa",
        r""
    ))
    all.course_filter["基礎"].add(Level3("関連", 10, 6))
    all.course_filter["基礎"].course_filter["関連"].add(Level4("必修", 0, 0))
    all.course_filter["基礎"].course_filter["関連"].add(Level4("選択", 10, 6))
    all.course_filter["基礎"].course_filter["関連"].course_filter["選択"].add(Level5("Ｅ，Ｆ，Ｇ，Ｈ，ＧＣ，ＧＥ，Ｈ以外始まり", MAX, 6))
    all.course_filter["基礎"].course_filter["関連"].course_filter["選択"].course_filter["Ｅ，Ｆ，Ｇ，Ｈ，ＧＣ，ＧＥ，Ｈ以外始まり"].add(RecognizedFilter(
        "Ｅ，Ｆ，Ｇ，Ｈ，ＧＣ，ＧＥ，Ｈ以外始まり",
        r"^[^EFGH1-9].*$",
        r""
    ))
    all.course_filter["基礎"].course_filter["関連"].course_filter["選択"].add(Level5("Ｅ，Ｆ，Ｇ，Ｈ，ＧＣ，ＧＥ，Ｈ始まり", 4, 0))
    all.course_filter["基礎"].course_filter["関連"].course_filter["選択"].course_filter["Ｅ，Ｆ，Ｇ，Ｈ，ＧＣ，ＧＥ，Ｈ始まり"].add(RecognizedFilter(
        "Ｅ，Ｆ，Ｇ，Ｈ，ＧＣ，ＧＥ，Ｈ始まり",
        r"^([EFH]|GC|GE).*$",
        r""
    ))
    return all


class kamokuClass():
    course_number = ""
    course_name = ""
    credit = 0.0
    grade = ""
    used = False
    can_use = False
    isCount = False

    def __init__(self, all) -> None:
        self.course_number = all[2]
        self.course_name = all[3]
        self.credit = float(all[4])
        self.grade = all[7]
        self.can_use = self.grade == "P" or self.grade == "A+" or self.grade == "A" or self.grade == "B" or self.grade == "C" or self.grade == "認"
        self.used = False
        self.isCount = "C0" != all[8]


    def print(self):
        if self.can_use:
            if self.used:
                print('{}{}:{}{}'.format(Color.BLUE,self.course_number,self.course_name,Color.RESET))
            else:
                print('{}{}:{}{}'.format(Color.GREEN,self.course_number,self.course_name,Color.RESET))
        else:
            print('{}{}:{}{}'.format(Color.RED,self.course_number,self.course_name,Color.RESET))

def gp(ls:[]):
    gps = 0.0
    credit_sum = 0.0
    for kam in ls:
        if kam.can_use and kam.isCount:
            if kam.grade == "A+":
                gps += 4.3*kam.credit
                credit_sum += kam.credit
            if kam.grade == "A":
                gps += 4*kam.credit
                credit_sum += kam.credit
            if kam.grade == "B":
                gps += 3*kam.credit
                credit_sum += kam.credit
            if kam.grade == "C":
                gps += 2*kam.credit
                credit_sum += kam.credit
            if kam.grade == "D":
                credit_sum += kam.credit
    
    print("GPA = GPS/CreditSum : {:1.5} = {}/{}".format(gps/credit_sum, gps, credit_sum))



def readCSV(CSVFILENAME):
    
    memo = []
    with open(CSVFILENAME) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i!=0:
                memo.append(kamokuClass(row))


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


def readNameFromCSV(CSVFILENAME):
    
    memo = []
    with open(CSVFILENAME) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i!=0:
                return row[1]
        # return reader[1][1]

def genJSON(v0):
    v0 = genCoins20()
    res = {}
    res[v0.name] = v0.genDict()
    for v1 in v0.course_filter.values():
        res[v0.name]["leaf"][v1.name] = v1.genDict()
        for v2 in v1.course_filter.values():
            res[v0.name]["leaf"][v1.name]["leaf"][v2.name] = v2.genDict()
            for v3 in v2.course_filter.values():
                res[v0.name]["leaf"][v1.name]["leaf"][v2.name]["leaf"][v3.name] = v3.genDict()
                for v4 in v3.course_filter.values():
                    res[v0.name]["leaf"][v1.name]["leaf"][v2.name]["leaf"][v3.name]["leaf"][v4.name] = v4.genDict()
                    for v5 in v4.course_filter.values():
                        res[v0.name]["leaf"][v1.name]["leaf"][v2.name]["leaf"][v3.name]["leaf"][v4.name]["leaf"]["regexp_number"] = v5.regexp_number
                        res[v0.name]["leaf"][v1.name]["leaf"][v2.name]["leaf"][v3.name]["leaf"][v4.name]["leaf"]["regexp_name"] = v5.regexp_name
    return json.dumps(res, ensure_ascii=False, indent=4)

def main():
    args = sys.argv
    CSVFILENAME = ""

    # coins20.print_son()
    print(genJSON(genCoins20()))
    

if __name__ == '__main__':
    main()
    