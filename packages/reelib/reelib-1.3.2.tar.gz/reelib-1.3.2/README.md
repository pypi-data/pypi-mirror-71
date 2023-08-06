# reelib

頻繁に利用する処理を集めたライブラリ

## インストール方法

```sh
pip install reelib
```

## ライブラリの内容

### timestamp

- 時刻文字列を扱う

```python
from reelib import timestamp

# 現在時刻のタイムスタンプを取得
ts = timestamp.get_timestamp()
# ex) 20191025164844890916

# タイムスタンプをdatetimeに変換
t = timestamp.conv_time_from_timestamp(ts)
# ex) datetime.datetime(2019, 10, 25, 16, 48, 44, 890916, tzinfo=datetime.timezone(datetime.timedelta(0, 32400)))
```

### contjson

- JSONを扱う

```python
from reelib import contjson

# ファイルからの読み込み
json_obj = load_from_file('test.json')

# ファイルへの書き込み
save_to_file(json_obj, 'test.json')

# JSONを整形して標準出力
print_json(json_obj)

# str型文字列をJSONに変換
json_obj = json_from_str('{"a":2, "b":3}')

# JSONをstr型文字列に変換
json_text = json_to_str(json_obj)
```

### contimg

- 画像ファイルを扱う

```python
from reelib import contimg

# PIL型をOpenCV型に変換
img_cv = contimg.pil2cv(img_pil)

# OpenCV型をPIL型に変換
img_pil = contimg.cv2pil(img_cv)

# 画像のリサイズ (トリミング)
resized = contimg.resize(img_cv, (画像のサイズ(x,yのtuple)), fill=False)

# 画像のリサイズ (パディング)
resized = contimg.resize(img_cv, (画像のサイズ(x,yのtuple)), fill=True)

# 画像タイルの作成
img_tile = contimg.get_imagetile((画像パスのリスト), (タイルのサイズ(x,yのtuple)), (タイルの数(x,yのtuple)))
```
