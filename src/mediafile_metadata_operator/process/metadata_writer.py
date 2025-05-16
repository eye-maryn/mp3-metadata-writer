from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError

class MetadataWriter:
    def __init__(self, path: str, metadatas: dict):
        self.path = path
        self.metadatas = metadatas

    def check_unavailable_keys(self) -> list:
        unavailable_keys = []
        for tagName in self.metadatas.keys():
            # 指定されたタグ名がmutagen.easyid3で設定不能なものである場合はリストに挿入
            if tagName not in EasyID3.valid_keys.keys():
                unavailable_keys.append(tagName)

        self.unavailable_keys = unavailable_keys
        # 無効なタグ指定を返却する
        return unavailable_keys
    
    def write_metadata(self):
        # メタデータの取得
        try:
            tags = EasyID3(self.path)
        except ID3NoHeaderError:
            # メタデータがなければ作成する
            ID3().save(self.path)
            tags = EasyID3(self.path)

        # タグ名を指定してメタデータを挿入
        for tagName, tagValue in self.metadatas.items():
            # 無効なキーは無視する
            if tagName in self.unavailable_keys:
                print('メタデータキー"' + tagName + '"は無効であるため、メタデータの登録はスキップされました。')
                continue
            print('メタデータキー"' + tagName + '"を値"' + tagValue + '"として登録しています...')
            tags[tagName] = tagValue
        tags.save()