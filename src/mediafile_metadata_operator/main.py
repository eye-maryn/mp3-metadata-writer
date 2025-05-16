import json
import os
from exceptions import InvalidInputFormat
from process import ExtensionTransformer, MetadataWriter, SerialNumberIntoFileName

def json_format_checker(target: dict) -> bool:
    return 'metadatas' in target.keys() and \
        type(target['metadatas']) == 'dict' and \
        'tracknumber' in target['metadatas'].keys() and \
        'extension' in target

def make_missing_json_key_message(target: dict) -> str:
    missingKey = []
    missingDictTypeKey = []

    if 'metadatas' not in target.keys():
        missingKey.append('metadatas')
    elif 'metadatas' in target.keys() and type(target['metadatas']) != 'dict':
        missingDictTypeKey.append('metadatas')
    elif 'tracknumber' not in target['metadatas'].keys():
        missingKey.append('tracknumber')
    
    if 'extension' not in target:
        missingKey.append('extension')
    
    message = ', '.join(missingKey) + 'が欠損しています。'
    if len(missingDictTypeKey != 0):
        if len(missingKey) != 0:
            message = message + 'また、'
        message = message + ', '.join(missingDictTypeKey) + 'はdict型を予期していますが、指定されているのはdictではないようです。'

    return message


def main():
    print('ファイル変換処理/メタデータ書き込みを開始します！')
    print('メタデータ設定ファイルのロードを開始します！')
    with open('./mediafiles/file_meta.json') as f:
        file_meta = json.load(f)
    print('メタデータ設定ファイルのロードが完了しました！')
    
    print('メタデータ設定ファイルのバリデーションを開始します！')
    if not json_format_checker(file_meta):
        raise InvalidInputFormat('メタデータの設定に不足しているキーがあります。: ' + make_missing_json_key_message(file_meta))
    print('メタデータ設定ファイルで問題は検出されませんでした！')

    print('メタデータの登録処理を開始します！')
    for file_name, file_information in file_meta.items():
        print('ファイル"' + file_name + '"のメタデータ登録処理を実行します！')
        path = os.path.dirname(__file__) + '/mediafiles/' + file_name

        print('ファイル名先頭へのトラック番号の付与処理を実行します！')
        # トラック番号と同様の連番をファイル名先頭に付与
        serial_no_add = SerialNumberIntoFileName(path, file_information['metadatas']['tracknumber'])
        path = serial_no_add.add_number()
        print('ファイル名先頭へのトラック番号付与処理に成功しました！')

        print('ファイルを指定したフォーマットへ変換します！')
        # 意図したファイルフォーマットに変換
        ext_transformer = ExtensionTransformer(path, file_information['extension'])
        if ext_transformer.need_transform():
            print('ファイル"' + file_name + '"は変換処理が必要です！')
            print('ファイルのフォーマット変換を開始します！')
            path = ext_transformer.extension_transform()
            print('ファイルのフォーマット変換が完了しました！')
        
        print('メタデータの書き込み処理を実行します！')
        # メタデータ書き込み
        metadata_writer = MetadataWriter(path, file_information['metadatas'])
        unavailable_keys = metadata_writer.check_unavailable_keys()
        if len(unavailable_keys) != 0:
            print('[NOTICE] メタデータキー "' + ', '.join(unavailable_keys) + '" は無効であるため無視されます。')
        print('メタデータの書き込みを開始します！')
        metadata_writer.write_metadata()
        print('メタデータの書き込み処理が完了しました！')
    
    print('全ての処理が完了しました！')

main()