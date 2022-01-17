# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# ! start .

# ! code .

# +
import os,git,shutil
import pandas as pd

# 指定されたデータサイズでファイルを分割する
def divide_file(filePath, chunkSize):
    readedDataSize = 0
    i = 0
    fileList = []
    # 対象ファイルを開く
    f = open(filePath, "rb")
    # ファイルを読み終わるまで繰り返す
    contentLength = os.path.getsize(filePath)
    while readedDataSize < contentLength:
        # 読み取り位置をシーク
        f.seek(readedDataSize)
        # 指定されたデータサイズだけ読み込む
        data = f.read(chunkSize)
        # 分割ファイルを保存
        saveFilePath = filePath + "." + str(i)
        with open(saveFilePath, 'wb') as saveFile:
            saveFile.write(data)
        # 読み込んだデータサイズの更新
        readedDataSize = readedDataSize + len(data)
        i = i + 1
        fileList.append(saveFilePath)
    return fileList

# 渡されたファイルリストの順序で１つのファイルに結合する
def join_file(fileList, filePath):
    with open(filePath, 'wb') as saveFile:
        for f in fileList:
            data = open(f, "rb").read()
            saveFile.write(data)
            saveFile.flush()
            
class env_util():
    def __init__(self):
        self.u_path = os.environ["userprofile"]
        self.miniconda_path = os.path.join(self.u_path,"miniconda3","pkgs")
        self.miniconda_path = os.path.join(self.u_path,"miniconda3","pkgs")
        self.freecad_path = os.path.join(self.u_path,"AppData","Roaming","FreeCAD")
        self.fac_path = os.path.join(self.u_path,"000_work","factory_env_miniconda39")
        self.fac_pkg_path = os.path.join(self.fac_path,"pkgs")
        self.repo_fac = git.Repo(self.fac_path)
    #         self.repo_freecad = git.Repo(self.freecad_path)
        self.remote_folder_path = os.path.join(self.u_path,"000_work","env_miniconda_39")
        self.remote_pkg_path = os.path.join(self.remote_folder_path,"pkgs")
        self.repo_remote_folder = git.Repo(self.remote_folder_path)

    def get_status_text(self,case):
        if case == 0:
            tex = self.repo_fac.git.status("-s")
        elif case == 1:
            tex = self.repo_remote_folder.git.status("-s")
#         elif case == 2:
#             tex = self.repo_freecad.git.status("-s")
        return tex

    def comfirm_file(self,case):
        tex = self.get_status_text(case)
        if tex.find("\n")  != 0:
            li = tex.split("\n")
            print(li)

        return li

    def get_list(self):
        file_list = []
        file_list_batsu = []
        for root, dirs, files in os.walk(self.miniconda_path):
            for filename in files:
                fname = os.path.join(root, filename)
                file_list.append([fname,os.path.getsize(fname) / 1000000])
            df = pd.DataFrame(file_list)
            df.columns=["path","MB"]
        return df

if __name__ == '__main__':
    self = env_util()
# -

# # おうち側作業

# リポジトリの中に未コミットがあれば、コミットとして0にする

li = self.comfirm_file(case=1)
li

if len(li) != 0:
    self.repo_remote_folder.git.add(r"*")
    li = self.comfirm_file(case=1)

if len(li) != 0:
    self.repo_remote_folder.git.commit("-m","gantt_s")

# ## nmp

os.environ["userprofile"]
f_path = os.path.join(os.environ["userprofile"],"000_work","env_miniconda_39","nmp_pkgs")
f_path













# ## pip

import os

os.environ["userprofile"]

f_path = os.path.join(os.environ["userprofile"],"000_work","env_miniconda_39","pip_pkgs")
f_path

# + active=""
# pip install 
# -

pkg_name = "anytree"
# print(f"pip download -d {f_path} --no-binary :all: {pkg_name}")
print(f"pip download -d {f_path} {pkg_name}")



# ! start .

# ## 初期化

# ### freecad

# ファイルをコピー

import pandas as pd
li_m = self.comfirm_file(case=2)
li_s = [[i[0:2],i[3:]] for i in li_m]
df = pd.DataFrame(li_s,columns=["code","file_name"])
df_tg = df[df["code"]=="??"]
li = list(df_tg["file_name"])

li_m

file_list = li
out_list = []
for file in file_list:
    f_path_moto = os.path.join(self.freecad_path,file)
    f_path_copy = os.path.join(self.remote_folder_path,"FreeCAD",file)
    out_list.append([f_path_copy,os.path.getsize(f_path_moto) / 1000000])
    try:
        shutil.copyfile(f_path_moto,f_path_copy)
    except :
        print(f"エラー:{f_path_moto}")
        pass
df = pd.DataFrame(out_list)
if len(df) != 0:
    df.columns=["path","MB"]

# 100M以上は分割（factory_env_miniconda39）

files = os.listdir(os.path.join(self.remote_folder_path,"FreeCAD"))
file_list = [os.path.join(self.remote_folder_path,"FreeCAD",f) for f in files ]
file_list = [[f,os.path.getsize(f) / 1000000] for f in file_list ]
df = pd.DataFrame(file_list)
df.columns=["path","MB"]

df_b = df[df["MB"]>99]
df_b

if len(df_b)!=0:
    for target in list(df_b["path"]):
        fileList = divide_file(target, 50*10**6)
        df_a = pd.DataFrame(fileList,columns=["path"])
        df_a.to_csv(os.path.join("sep_file_list_freecad/",os.path.basename(target)+".csv"),index=False)
        os.remove(target)

# ### env_miniconda_39

# pkgsとsep_file_listの中のファイルを削除

shutil.rmtree(self.remote_pkg_path)
os.mkdir(self.remote_pkg_path)
shutil.rmtree(os.path.join(self.remote_folder_path,"sep_file_list"))
os.mkdir(os.path.join(self.remote_folder_path,"sep_file_list"))

# ### factory_env_miniconda39

# 未コミットはコミットしておく

li = self.comfirm_file(case=0)

# 未コミットがあれば、コミットとして0にする

# +
if len(li) != 0:
    self.repo_fac.git.add(r"*")
    li = self.comfirm_file(case=0)

if len(li) != 0:
    self.repo_fac.git.commit("-m","initial commit")
# -

# ## miniconda→factory_env_miniconda39にコピー
# 同じ状態にします

files = os.listdir(self.miniconda_path)
file_list = [f for f in files if os.path.isfile(os.path.join(self.miniconda_path, f))]
for file in file_list:
    f_path_moto = os.path.join(self.miniconda_path,file)
    f_path_copy = os.path.join(self.fac_pkg_path,file)
    try:
        shutil.copyfile(f_path_moto,f_path_copy)
    except :
        print(f"エラー:{file}")
        pass

file_list

# ## factory_env_miniconda39→env_miniconda_39にコピー
# factory_env_miniconda39の未コミットのファイルをenv_miniconda_39にコピーします

import pandas as pd
li_m = self.comfirm_file(case=0)
li_s = [[i[0:2],i[3:]] for i in li_m]
df = pd.DataFrame(li_s,columns=["code","file_name"])
df_tg = df[df["code"]=="??"]
li = list(df_tg["file_name"])

li_m

file_list = li
out_list = []
for file in file_list:
    f_path_moto = os.path.join(self.fac_path,file)
    f_path_copy = os.path.join(self.remote_folder_path,file)
    out_list.append([f_path_copy,os.path.getsize(f_path_moto) / 1000000])
    try:
        shutil.copyfile(f_path_moto,f_path_copy)
    except :
        print(f"エラー:{f_path_moto}")
        pass
df = pd.DataFrame(out_list)
if len(df) != 0:
    df.columns=["path","MB"]

# ## 100M以上は分割（factory_env_miniconda39）

files = os.listdir(self.remote_pkg_path)
file_list = [os.path.join(self.remote_pkg_path,f) for f in files ]
file_list = [[f,os.path.getsize(f) / 1000000] for f in file_list ]
df = pd.DataFrame(file_list)
df.columns=["path","MB"]

df_b = df[df["MB"]>99]
df_b

if len(df_b)!=0:
    for target in list(df_b["path"]):
        fileList = divide_file(target, 50*10**6)
        df_a = pd.DataFrame(fileList,columns=["path"])
        df_a.to_csv(os.path.join("sep_file_list/",os.path.basename(target)+".csv"),index=False)
        os.remove(target)

# ! start .

# ## react

# +
import os
import pandas as pd

dir_path = r"C:\Users\M151325\000_work\env_miniconda_39\react"
file_list=[]
for (root, directories, files) in os.walk(dir_path):
#     for d in directories:
#         d_path = os.path.join(root, d)
#         print(d_path)
    for file in files:
        file_path = os.path.join(root, file)
#         print(file_path)
        file_list.append(file_path)
# -

file_list = [[f,os.path.getsize(f) / 1000000] for f in file_list ]
df = pd.DataFrame(file_list)
df.columns=["path","MB"]

df_b = df[df["MB"]>99]
df_b

# ## githubへpush(factory_env_miniconda39)

li_m = self.comfirm_file(case=1)
li_s = [[i[0:2],i[3:]] for i in li_m]
df = pd.DataFrame(li_s,columns=["code","file_name"])
df

if len(li_m) != 0:
    self.repo_remote_folder.git.add(r"*")
    li_mi= self.comfirm_file(case=1)

li_mi

if len(li_mi) != 0:
    self.repo_remote_folder.git.commit("-m","zeep")

# push

self.repo_remote_folder.git.push()

# # 相手側作業

# リポジトリをダウンロードして、000_workの下に移動する
#
# https://github.com/nyanko111777/env_miniconda_39/archive/refs/heads/main.zip
#

# ## 100M以上を復活

# +
import pandas as pd
import os

file_list =  os.listdir("sep_file_list")
for file in file_list:
    df_temp = pd.read_csv("sep_file_list/"+file)
    fileList = list(list(df_temp["path"]))
    target = fileList[0][:fileList[0].find(".0")]
    join_file(fileList, target)
    for d_file in fileList:
        os.remove(d_file)
# -

# ## インストール

# - conda の場合
#   `for /f %i in ('dir /A-d /B *') do conda install %i`
#
#
#
# - pip の場合
#   `for /f %i in ('dir /A-d /B *') do pip install %i`
#


