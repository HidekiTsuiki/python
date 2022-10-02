# 「プログラミング演習（数理的応用）」　　　2021 年度
 
これは、京都大学全学共通科目「プログラミング演習（数理的応用）」のオンライン教材です。


## 起動方法など

### github からのコピー

この授業の教材は，github という，プログラム等を公開するためのプラットフォーム上に置かれています。このファイル自体が，github 上に置かれているので，皆さんは，Web で github にアクセスしてこのファイルを見ているはずです。github で管理されているようなデータの置き場所のことをリポジトリといいます。まず，自分のコンピュータにリポジトリを作って，github に公開されている，教材のリポジトリと同期させるようにしましょう。作業は，コマンドプロンプトで行います。コマンドプロンプトは，Windows の左下の2番目の◯をクリックして，cmd を検索したら出てきます。コマンドプロンプトで，以下の作業を行いましょう。

0. まず，Documents の下に移動しましょう。

  cd Documents

1. リポジトリを置くディレクトリ（フォルダ）を作ります。名前は，ここでは pyhton にしています
が，自分で決めてください。  

  mkdir python

2. そのディレクトリに移動します。

  cd python

3. このディレクトリを，github のリポジトリの置き場所にする準備をします。

  git init

4. Web 上の教材の置かれたリポジトリのコピーを，ここに作成します。

  git clone https://github.com/HidekiTsuiki/python.git

5. Web 上の教材の内容は，どんどん更新されていくはずです。それを取り込むには，このディレクトリで次のことを行います。例えば，授業の始まる前に行ってください。

  git pull

手元でファイルの変更を伴う作業を行ってから git pull すると，エラーが出ます。エラーが出たら，次のコマンドでファイルの状態を戻してから行ってください。
  
  git reset --hard
  
  自分が行った編集をとっておきたければ，
  対応するファイルを自分の覚えのある名前に変更してとっておいてから，もう一度行ってください。


### 大学のコンピュータで，jupyter lab の起動方法

次の２つがあります。

  1. Anaconda を起動し，その中で，jupyter lab の Launch ボタンを押す。
  2. 左下の検索(?) の所で cmd と入力してコマンドプロンプトを起動し，そこで，jupyter-lab と入力する。

起動すると，ブラウザのページが現れます。
左側のタグから Files を選び，ファイルの一覧から python フォルダを探し，ファイル名の先頭のアイコンをクリックします。そして，ファイルの一覧から，ファイル 1Jupyter.ipynb を選びます。ipynb という拡張子は，jupyter lab/notebook のファイルにつけられたものです。
左の Files タグをもう一度クリックすると，ファイルの選択画面が消えて画面全体を使えるようになります。



  


