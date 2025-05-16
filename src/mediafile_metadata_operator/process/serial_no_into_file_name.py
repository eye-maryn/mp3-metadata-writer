import shutil

class SerialNumberIntoFileName:
    def __init__(self, path: str, number: str):
        self.path = path
        self.number = number

    def add_number(self) -> str:
        # パスの/ごとで区切る
        spritted_path = self.path.split('/')
        # パスの/で区切った末尾のファイル名を取り出す
        filename = spritted_path[-1].strip()
        # 連番を0パディングして2桁で設定
        serial_no = self.number.zfill(2)
        # 00_filename.mp3の形式でファイル名を設定
        filename = serial_no + '_' + filename
        # パスの中のファイル名を連番付きのものに変更する
        spritted_path[-1] = filename
        # パスを/で復元する
        path = '/'.join(spritted_path)

        # ファイル名をリネーム
        shutil.move(self.path, path)

        return path
        