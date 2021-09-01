# setup

`/miniconda3/pkgs`の中身を追いかけて、環境のコピーを作成する

## utility

### git の差分を取得する

コミットした後に下記を実行すると、差分がアーカイブされる
https://www.sukerou.com/2021/03/git.html

`git archive HEAD `git diff --name-only HEAD^ HEAD --diff-filter=ACMR`-o archive.zip`

### 差分パッケージのインストール

https://qiita.com/uguisuheiankyo/items/40bcbe4c993504cac09a

パッケージを保存したフォルダに移動して下記を実行
　※中身はインストールできるものだけにしておく

- conda の場合
  `for /f %i in ('dir /A-d /B *') do conda install %i`

- pip の場合
  `for /f %i in ('dir /A-d /B *') do pip install %i`

- Dir /b :/b を付けると要約や日時、サイズなどを省略し直下のファイル・フォルダの名前のみ出力
- Dir /a-d : /a-d を付けると直下のファイル名のみ出力(サブフォルダは無視)

## start miniconda version

Miniconda3-py39_4.10.3-Windows-x86_64.exe

## SETP 1

Freecad をインストールする

https://github.com/FreeCAD/FreeCAD_Conda

```
conda config --add channels conda-forge
conda install freecad
conda install jupyter

conda install -y -c conda-forge jupyter_contrib_nbextensions
conda install -c conda-forge nodejs
jupyter contrib nbextension install --user
conda install gitpython
conda install pandas
```

## STEP2

```
conda install pyntcloud -c conda-forge
conda install -c conda-forge pdfminer.six
conda install -c conda-forge shapely
conda install -c conda-forge opencv
conda install -c conda-forge trimesh
conda install -c conda-forge meshpy
conda install dtale -c conda-forge
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```
