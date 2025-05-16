import os
import pydub
from exceptions import InvalidFileFormat

class ExtensionTransformer:
    def __init__(self, file_path: str, need_format: str):
        # パスを/で区切る
        splitted_file_path = file_path.split('/')
        # /で区切ったパスの末尾のファイル名を取得する
        file_name = splitted_file_path[-1]
        # 取得したファイル名を.で区切る
        splitted_file_name = file_name.split('.')
        # .で区切ったファイル名の末尾を拡張子として取得
        file_extension = splitted_file_name[-1]

        self.file_path = file_path
        self.file_extension = file_extension
        self.need_format = need_format
    
    def need_transform(self) -> bool:
        # 拡張子と要求された拡張子が違う場合はファイルフォーマットの変換が必要であると報告する
        return self.file_extension != self.need_format
    
    def extension_transform(self) -> str:
        if self.file_extension == 'mp3':
            # 現在のファイルがmp3の拡張子を持っている場合はmp3として読み込み
            sound_file = pydub.AudioSegment.from_mp3(self.file_path)
        elif self.file_extension == 'wav':
            # 現在のファイルがwavの拡張子を持っている場合はwavとして読み込み
            sound_file = pydub.AudioSegment.from_wav(self.file_path)
        else:
            # mp3とwavのどちらでもない場合はファイルフォーマット例外を出す
            raise InvalidFileFormat('ファイルフォーマットが不正です。ファイルフォーマットはmp3かwavである必要があります。')
        
        # ファイルパスを/で区切る
        splitted_file_path = self.file_path.split('/')
        # 区切ったファイルパスの末尾をファイル名として、ファイル名を.で区切る
        splitted_file_name = splitted_file_path[-1].split('.')
        # .で区切ったファイル名の末尾を拡張子として要求された拡張子に置換する
        splitted_file_name[-1] = self.need_format
        # ファイル名の配列を.で繋げて復元
        save_file_name = '.'.join(splitted_file_name)
        # ファイル名をパスに設定する
        splitted_file_path[-1] = save_file_name
        # パスを/で復元する
        save_file_path = '/'.join(splitted_file_path)

        # ファイルを変換対象のフォーマットに変換してエクスポート
        sound_file.export(save_file_path, format=self.need_format)

        # 変換後のファイルのパスを返却する
        return save_file_path
    
    def remove_base_file(self):
        # 変換済みのファイルを削除
        os.remove(self.file_path)