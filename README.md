# メタデータ書き込みスクリプト
MP3ファイルにメタデータを書き込みます。  
対象ファイルと指定したフォーマットが異なる場合は、指定したフォーマットにファイルを変換してからメタデータを書き込みます。（wav <-> mp3相互変換のみ）  
また、ファイル名の先頭にメタデータと同じトラック番号を2桁のゼロパディングを行なってから付与します。(トラック1番のsample.mp3 -> 01_sample.mp3)  

# 使い方
1. poetryの環境に入る
2. poetry installを実行
3. src/mediafile_metadata_operator/mediafiles/以下に楽曲ファイルを挿入
4. file_meta.jsonに対応するファイルとその情報を書き込みます。
5. src/mediafile_metadata_operator/main.pyを実行します。
6. src/mediafile_metadata_operator/mediafiles/ に連番 + 指定したファイルフォーマットと拡張子に変換されたファイルが出力されます。

# 注意点
使用前に実行するマシンへのffmpegのインストールが必要です。
