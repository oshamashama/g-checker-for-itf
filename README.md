<!-- markdownlint-disable MD033 -->
# g-checker-for-itf

ITF の卒業要件を確認したい。(今は coins19/coins20/coins21, mast20 とか)

提供されているプログラム、またそのプログラムによる実行結果に関する保証はできかねます。

## Install

### Clone Repository

```bash
git clone --depth 1 https://github.com/oshamashama/g-checker-for-itf
cd g-checker-for-itf
pip install ./pycli
```

### pip install

```bash
pip install g-checker-for-itf
```

のいずれかで`gchk`コマンドをインストールできます。
今時点で要件確認のためのファイルをこのリポジトリからダウンロードしてくる必要があるため、 Clone によるインストールを推奨します。

#### Get Requirements File

```bash
wget https://raw.githubusercontent.com/oshamashama/g-checker-for-itf/main/coins20.json
```

などで卒業要件を定義したファイルをダウンロードしてきてください。

## Usage

```bash
gchk -i target_csv_file -r requirements_json_file
```

で実行できます。

`target csv file` は twins の成績ページからダウンロードしたファイル (UTF, CSV) を想定しています。

```shellsession
$ gchk
usage: gchk [-h] [-i INPUT] [-r REQUIREMENTS] [-g] [-d] [-n] [-s] [-e] [-V]

A checker if your credits meet the graduation requirements or not.

optional arguments:
  -h, --help                  show this help message and exit
  -i INPUT, --input INPUT     target file from twins (UTF-8, CSV) (default: sample.csv)
  -r REQUIREMENTS, --requirements REQUIREMENTS
                              requirements file (default: coins20.json)
  -g, --gpa                   print GPA (default: False)
  -d, --drop                  print drop credit (default: True)
  -n, --name                  print name and id (default: False)
  -s, --save                  save as JSON (default: False)
  -e, --expect                count 履修中 (default: False)
  -V, --version               show program's version number and exit
```

## Test

```bash
gchk -i sample.csv -r coins20.json
```

で予め用意されたサンプルで動作を確認することが出来ます。

```bash
wget https://raw.githubusercontent.com/oshamashama/g-checker-for-itf/main/coins20.json
wget https://raw.githubusercontent.com/oshamashama/g-checker-for-itf/main/sample.csv
```


## Viewer

現状、このリポジトリを clone することが必要です。

```bash
gchk -s -i target_csv_file
cp saved_file ~/g-checker-for-itf/src/grade.json
cd tani
npm install
npm start
```


## Screenshots

<img width="1358" alt="イメージ画像(CUI)" src="https://user-images.githubusercontent.com/65126083/151887795-b8b7bca4-b8bc-4822-ad60-e7e721b23805.png">
<img width="1358" alt="イメージ画像(GUI)" src="https://user-images.githubusercontent.com/65126083/151988273-44ae9485-3358-4e93-b28f-7686ae65fef5.png">
