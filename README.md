# g-checker-for-itf
ITF の卒業要件を確認したい。(今はcoins20 だけ)

提供されているプログラム、またそのプログラムによる実行結果に関する保証はできかねます。


# usage

```
python3 main.py -i $(target csv file)
```

で実行できます。
複数ファイルを引数に与えることができ、その場合は連続して判定が行なわれます。
`target csv file` は twins の成績ページからダウンロードしたファイル (UTF, CSV) を想定しています。

```
options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        target file from twins (UTF-8, CSV)
  -r REQUIREMENTS, --requirements REQUIREMENTS
                        requirements file
  -g, --gpa             print GPA Flag
  -d, --drop            print drop credit unable Flag
  -n, --name            print name and id, able Flag
```

# test 

```
python3 main.py -i sample.csv -r coins20.json
```


で予め用意されたサンプルで動作を確認することが出来ます。

# image

<img width="1358" alt="イメージ画像" src="https://user-images.githubusercontent.com/65126083/151887795-b8b7bca4-b8bc-4822-ad60-e7e721b23805.png">
