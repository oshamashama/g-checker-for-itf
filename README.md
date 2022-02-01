<!-- markdownlint-disable MD033 -->
# g-checker-for-itf

ITF の卒業要件を確認したい。(今はcoins20 だけ)

提供されているプログラム、またそのプログラムによる実行結果に関する保証はできかねます。

## Usage

```bash
git clone --depth 1 https://github.com/oshamashama/g-checker-for-itf
cd g-checker-for-itf
pip install .
```

で`gchk`コマンドをインストールできます。

```bash
gchk -i target_csv_file
```

で実行できます。
複数ファイルを引数に与えることができ、その場合は連続して判定が行なわれます。
`target csv file` は twins の成績ページからダウンロードしたファイル (UTF, CSV) を想定しています。

```shellsession
$ gchk
usage: gchk [-h] [-i INPUT] [-r REQUIREMENTS] [-g] [-d] [-n] [-s] [-e] [-V]

This program is check that your credit can meet the graduation requirements.

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

## Viewer

```bash
gchk -s -i target_csv_file
cd tani
npm install
npm start
```

[http://localhost:3001/](http://localhost:3001/) にアクセスすると確認できます。

## Screenshots

<img width="1358" alt="イメージ画像(CUI)" src="https://user-images.githubusercontent.com/65126083/151887795-b8b7bca4-b8bc-4822-ad60-e7e721b23805.png">
<img width="1358" alt="イメージ画像(GUI)" src="https://user-images.githubusercontent.com/65126083/151988273-44ae9485-3358-4e93-b28f-7686ae65fef5.png">
