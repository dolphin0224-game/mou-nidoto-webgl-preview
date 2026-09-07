# 台詞の音声と再生中の編集

AivisSpeechを起動して `python -X utf8 Tools/Voice/generate.py` を実行すると、ゲーム内の台詞から音声を生成します。生成済みの同じ台詞は再利用します。本文や話者が変わった台詞だけ新しいファイルになります。

|役|モデル|演出|
|---|---|---|
|蒼|にせ|近い距離で自然に話す青年。通常速度を少し上げる|
|澪|まお・おちつき|世話を焼く柔らかさ。甘い演技に寄せすぎない|
|律|M2|明瞭で落ち着く。悲しみの場面は対応スタイル|
|栞|花音|静かな声、少し遅い間|
|蓮|澤原 玄二郎・close|人を引っ張る勢い。危険な場面のみclose-shout|
|運転手・老人|阿井田 茂|Calm / Heavyを使い分ける|

モデルの役名とゲームの人物は別物であり、モデルの公式作品・声優本人の出演を意味しません。これは合成音声です。

## 編集

1. Unityで本編のカットシーンを再生し、**F8**（Tools → Mou Nidoto → 再生中のカットシーンを編集）を押します。
2. **現在のTimelineを開いて編集**で進行を止め、カメラ・字幕・Voiceトラックを編集します。
3. 音声ファイルを選び、**現在位置にボイスクリップを追加**で追加できます。VoiceトラックはAudioSourceに接続されます。
4. **編集を保存して次回にも反映**を押します。保存先は `Resources/MouNidoto/Timelines`。Play終了後も残ります。
5. **ゲームの台詞進行へ戻る**で再開します。保存済みTimelineは次回同じ会話が始まったときに読み込みます。

体験制作室で絵コンテJSONを読み込む場合も、各カットの「台詞の音声」を選択できます。既存台詞に一致する音声は自動選択します。未生成の台詞は字幕を維持し、音声を無理に代用しません。

生成内容・話者・スタイル・秒数・ハッシュは `Docs/MouNidoto/Voice/manifest.json`。採用モデルのライセンスも同じフォルダーに収録しています。M2由来の音声はJVNVコーパスをクレジットし、CC BY-SA 4.0として提供します。音声には速度調整、音量調整、弱いノイズ抑制を行っています。その他の採用モデルはACML 1.0です。モデル本体はゲームに同梱しません。

モデル配布元：
- https://hub.aivis-project.com/aivm-models/6d11c6c2-f4a4-4435-887e-23dd60f8b8dd
- https://hub.aivis-project.com/aivm-models/2e1fdde8-d089-42d7-b64f-cf89952b1bdc
- https://hub.aivis-project.com/aivm-models/d1a7446f-230d-4077-afdf-923eddabe53c
- https://sites.google.com/site/shinnosuketakamichi/research-topics/jvnv_corpus
- https://creativecommons.org/licenses/by-sa/4.0/

地図は内蔵画像生成で制作。村の南北の高低差、中央の橋、北の滝と広場、南東の祠、西の道祖神を指定し、紙と墨・淡い水彩の案内図として生成しました。最終画像は `Resources/MouNidoto/VillageAtlas.png`。地名、調査、既知の地下道と人物情報は画像に焼かずUIで重ねています。
