from mutagen.easyid3 import EasyID3

# 書き込み可能なメタデータタグを表示する
print('書き込み可能なメタデータのタグを表示します。')
for key in EasyID3.valid_keys.keys():
    print(key)
