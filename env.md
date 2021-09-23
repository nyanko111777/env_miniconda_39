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

`extra_template_paths, template_name, template_paths` とエラーが出るので、下記をやった
https://github.com/ipython-contrib/jupyter_contrib_nbextensions/issues/1529

```
My solution, which seems to work in my computer, is like this:

Replace template_path with template_paths in the following files:

%userprofile%/miniconda3/lib/site-packages/latex_envs/latex_envs.py
%userprofile%/miniconda3/lib/site-packages/jupyter_contrib_nbextensions/nbconvert_support/exporter_inliner.py
%userprofile%/miniconda3/lib/site-packages/jupyter_contrib_nbextensions/nbconvert_support/toc2.py
```

## STEP3

```
conda install --name base autopep8 -y
conda install jupyter-dash
conda install colorlover
```

## STEP4

```
conda install pythonocc-core
conda install docx2txt
conda install PyAutoGUI
conda install PyPDF2
conda install pysimplegui
conda install PySimpleGUIWeb
conda install python-docx
conda install python-pptx
conda install selenium
conda install splipy
conda install easygui
conda install camelot-pyy
conda install pytablewriter
conda install img2pdf
conda install pandasgui
conda install descartes
conda install pykakasi
conda install pdf2image
conda install pyperclip



```

## STEP4

```
conda install pyinstaller
```

## STEP5

```
conda install beautifulsoup4
conda install xlwings

```

## STEP6

FREECAD initial commit

```
pip install mouse
```

## 適宜

'''

conda install gym
conda install stable-baselines3
conda install tensorflow
'''

## 入らない。。。

```
pip install streamlit
pip install solidpython
pip install viewscad
set PYTHONUTF8=1
pip install sectionproperties
```

## memo

```
pip install python-redmine
pip install cufflinks
pip install PyMuPDF
pip install blender-notebook
pip install frosch
pip install pptx2md
pip insatll mammoth
pip install pyvtk
pip install pyqt5
```

```
blender_notebook install --blender-exec="$prefix\blender\blender-2.90.1-windows64\blender.exe"
```
