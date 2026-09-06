# 素材・制作出典

企画原案は創作部屋の議論および『もう二度と』企画書0.2。台詞、ゲーム規則、専用シーンの構成、UIと接続処理、BGM・笛のモチーフ・一部効果音は今回の作業で制作。環境音と足音には、以下の録音素材を使用しています。

## 人物

MakeHuman / MPFB の身体、衣服、髪、目、眉、睫毛、歯、靴から生成し、骨格、衣装の材質分け、身長、配色を調整しました。「人物の全形状をゼロから手作りした」という扱いではありません。

- [MPFB](https://github.com/makehumancommunity/mpfb2)
- [MakeHuman System Assets CC0](https://static.makehumancommunity.org/assets/assetpacks/makehuman_system_assets.html)
- 元アセットの権利表記：Data Collection AB、Joel Palmius、Jonas Hauquier。2020年9月のCC0提供。本文は `Licenses/MakeHuman-CC0.md`。
- 歩行・走行・待機・会話・死亡・引く動作：**Quaternius / Universal Animation Library — Standard、CC0**。https://quaternius.com/packs/universalanimationlibrary.html 。配布ミラー https://github.com/J-Ponzo/gltf-universal-animation-library 。Unity Humanoidへリターゲットし、速度ブレンド・足の接地を設定。
- 顔：MakeHuman faceunits01 / visemes01、Mika Suominen、CC0。52 ARKit相当の表情チャンネルと22音素をモデルに移植。https://files.makehumancommunity.org/functional/faceunits01.zip
- **Mindfront (Sweden) / Cardigan Long Open Front、CC BY 4.0**。https://www.makehumancommunity.org/node/1528 。配布パック https://static.makehumancommunity.org/assets/assetpacks/shirts02.html 。丈・配色・身体へのフィットを変更し、重なった内側の袖を除去。ライセンス https://creativecommons.org/licenses/by/4.0/ 。作者が本ゲームを推奨していることを示すものではありません。
- 2Dキャラクター方向画を先に生成し、その配色・シルエットを上記の身体・衣装素材に反映。Blenderの編集元はプロジェクト `Docs/MouNidoto/Source/V3`。

## 背景

- 指定プロジェクトの JTS Shrine Torii Gates / JTS Stone Lanterns（Tanuki Digital）。元アセットは変更せず、専用シーン用のURP材質を作成しました。
- [Forest Ground 04](https://polyhaven.com/a/forest_ground_04)：Rob Tuytel、Rico Cilliers。
- [Wood Floor Deck](https://polyhaven.com/a/wood_floor_deck)：Dimitrios Savva。
- [Pine Sapling Medium](https://polyhaven.com/a/pine_sapling_medium)：Rob Tuytel、Rico Cilliers。3種をBlenderでゲーム向けに軽量化。
- 上記Poly HavenアセットはCC0。取得元API：Powered by Poly Haven。ゲームはAPI接続を必要としません。
- 読み取り用メタデータに掲載されたMD5で、ダウンロードしたファイルを照合しました。

## 文字

Shippori Mincho、Zen Kaku Gothic New、Klee One、Allura。SIL Open Font License 1.1。各ライセンス本文を `Licenses` に同梱しています。

- [Allura](https://github.com/google/fonts/tree/main/ofl/allura)
- [Klee One](https://github.com/google/fonts/tree/main/ofl/kleeone)

## システム

Unity 6000.3.23f1 / Universal Render Pipeline。既存の Cutscene Studio を拡張して使用。Steam SDK、Steam実績、収録ボイスは含みません。

## V3で追加した背景素材（CC0）

- [Moss Rocks](https://polyhaven.com/a/rock_moss_set_01)：Kless Gyzen。配置、スケール、URP材質を調整。
- [Fern 02](https://polyhaven.com/a/fern_02)：Rico Cilliers、Rob Tuytel。風で揺れるシェーダーを接続。
- [Fir Sapling](https://polyhaven.com/a/fir_sapling)：Poly Haven。URP材質・表示距離を調整。
- [Rough Plaster Broken](https://polyhaven.com/a/rough_plaster_broken)、[Cobblestone Floor 05](https://polyhaven.com/a/cobblestone_floor_05)：Rob Tuytel。村の壁・敷石に使用。
- 川、滝、地下道、時計台、バス、112枚の曲面石で組んだ井戸、落下する鞄・玩具・衣服・木、行列の笛、風・水面用シェーダー：本プロジェクト用に制作。

## 録音素材

- **Nature Sounds Pack — Antoine Goumain / Antoinemax、CC BY 4.0**。https://opengameart.org/content/nature-sounds-pack 。雨、雷、沢、草地の足音。ゲーム内で音量・距離・ループ・組合せを変更。ライセンス https://creativecommons.org/licenses/by/4.0/ 。
- **Crickets Ambient Noise (Loopable) — Wolfgang_ / Ted Kerr、CC0**。https://opengameart.org/content/crickets-ambient-noise-loopable 。夜の虫の環境音。地域の特定種「鈴虫」の録音と確認できたものではありません。
- **Different Steps on Wood, Stone, Leaves, Gravel and Mud — TinyWorlds、CC0**。https://opengameart.org/content/different-steps-on-wood-stone-leaves-gravel-and-mud 。木と石の足音を使用。元pdSounds録音を編集した配布素材。

## 生成画像

OpenAI image generationでオリジナルの五人の方向画と、白椿・時計・鳥居写真を含む開いた日記の画像を生成。`ArtDirection/CastDesign.png`、`ArtDirection/JournalBook.png`。参照作品のキャラクターや画像を抜き出した素材ではありません。人物の3D化は画像からの自動復元ではなく、上記ライセンス済みモデルをBlenderで調整する工程です。
