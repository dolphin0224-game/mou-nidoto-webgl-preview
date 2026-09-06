export const BUILD='studio-20260906-01';
export const KINDS={order:'体験オーダー',storyboard:'カットシーン絵コンテ',review:'プレイレビュー'};
export const SURFACES=['ゲーム全体','タイトル・起動','自由探索・移動','調査・謎解き','会話・カットシーン','戦闘・QTE・選択','日記・フローチャート','スマホ','メニュー・設定・セーブ','音・環境・天候','エンディング'];
export const STATUSES=['下書き','相談したい','制作に進める','制作中','レビュー待ち','修正が必要','体験を確認済み','保留'];
export function newDoc(kind='order') {return {schema:1,id:crypto.randomUUID(),revision:1,kind,title:'',surface:SURFACES[0],status:'下書き',owner:'',intent:'',understanding:'',action:'',before:'',after:'',avoid:'',acceptance:'',related:'',implementation:'',build:BUILD,updated:new Date().toISOString(),shots:[],actual:'',expected:'',category:'理解・感情',priority:'体験を壊す',steps:'',verdict:'未確認',recheck:'',attachments:[]};}
export function newShot(){return {id:crypto.randomUUID(),speaker:'律',text:'',place:2,actor:1,seconds:5,composition:'',action:'',sound:'',input:'操作なし',transition:'元の位置・向きで探索へ戻す',emotion:'',fear:0,sorrow:0,smile:0,exposure:.15,focalLength:42,customCamera:false,cameraPosition:{x:0,y:0,z:0},cameraRotation:{x:0,y:0,z:0},image:'',strokes:[]};}
export function validateDoc(d){
  if(!d||d.schema!==1||!KINDS[d.kind]||typeof d.id!=='string'||!/^[\w-]{1,100}$/.test(d.id))throw Error('この制作データの形式・版は読み込めません。');
  if(!Number.isInteger(d.revision)||d.revision<1)throw Error('改訂番号が不正です。');
  for(const k of ['title','surface','status','owner','intent','understanding','action','before','after','avoid','acceptance','related','implementation','build','actual','expected','category','priority','steps','verdict','recheck'])if(d[k]!=null&&(typeof d[k]!=='string'||d[k].length>30000))throw Error('文章が不正、または長すぎます。');
  if(!Array.isArray(d.shots)||d.shots.length>60)throw Error('絵コンテは60カットまでです。');
  for(const s of d.shots){if(!s||!Number.isFinite(s.seconds)||s.seconds<.5||s.seconds>120||!Number.isInteger(s.place)||s.place<0||s.place>7||!Number.isInteger(s.actor)||s.actor< -1||s.actor>3)throw Error('カットの尺・場所・人物を確認してください。');
    for(const k of ['speaker','text','composition','action','sound','input','transition','emotion'])if(s[k]!=null&&(typeof s[k]!=='string'||s[k].length>30000))throw Error('カットの文章が不正です。');
    for(const k of ['fear','sorrow','smile'])if(!Number.isFinite(s[k])||s[k]<0||s[k]>1)throw Error('表情は0〜1です。');
    if(!Number.isFinite(s.exposure)||Math.abs(s.exposure)>3||!Number.isFinite(s.focalLength)||s.focalLength<12||s.focalLength>120)throw Error('カメラ・露出の設定が不正です。');
    for(const v of [s.cameraPosition,s.cameraRotation])if(!v||['x','y','z'].some(k=>!Number.isFinite(v[k])||Math.abs(v[k])>10000))throw Error('カメラ座標が不正です。');
    if(s.image&&!/^data:image\/(jpeg|png|webp);base64,[a-z0-9+/=]+$/i.test(s.image))throw Error('画像はPNG/JPEG/WebPにしてください。');
    if(s.strokes!=null&&(!Array.isArray(s.strokes)||s.strokes.length>1000))throw Error('描き込みが多すぎます。');
  }
  if(d.capture?.image&&!/^data:image\/(jpeg|png|webp);base64,[a-z0-9+/=]+$/i.test(d.capture.image))throw Error('画面画像が不正です。');
  return d;
}
export function withoutImages(doc){const d=structuredClone(doc);for(const s of d.shots||[])s.image='';if(d.capture)d.capture.image='';return d;}
export async function pack(doc){validateDoc(doc);const bytes=new TextEncoder().encode(JSON.stringify(withoutImages(doc)));const buffer=await new Response(new Blob([bytes]).stream().pipeThrough(new CompressionStream('gzip'))).arrayBuffer();return btoa(String.fromCharCode(...new Uint8Array(buffer))).replaceAll('+','-').replaceAll('/','_').replace(/=+$/,'');}
export async function unpack(encoded){
  if(!/^[\w-]+$/.test(encoded)||encoded.length>80000)throw Error('共有リンクが不正、または長すぎます。');
  const bytes=Uint8Array.from(atob(encoded.replaceAll('-','+').replaceAll('_','/')),c=>c.charCodeAt(0));
  const reader=new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip')).getReader();let n=0;const chunks=[];
  while(true){const {value,done}=await reader.read();if(done)break;n+=value.length;if(n>2000000){await reader.cancel();throw Error('共有データが大きすぎます。');}chunks.push(value);}
  return validateDoc(JSON.parse(await new Blob(chunks).text()));
}
export function acceptanceProblems(d){const p=[];if(!d.title.trim())p.push('タイトル');if(d.kind==='review'){if(!d.actual?.trim())p.push('実際に感じたこと');if(!d.expected?.trim())p.push('望んだ体験');}else {if(!d.intent?.trim())p.push('感じてほしいこと');if(!d.acceptance?.trim())p.push('体験の確認基準');if(d.kind==='storyboard'&&!d.shots.length)p.push('1枚以上のカット');}return p;}
export function issueBody(d,url){return `## ${KINDS[d.kind]}：${d.title}\n\n[制作室でこの版を開く](${url})\n\n- 対象：${d.surface}\n- 状態：${d.status}\n- 作成：${d.owner||'未記入'}\n- ID：${d.id} / 改訂 ${d.revision}\n- ゲーム版：${d.capture?.build||d.build}\n\n### 意図・望んだ体験\n${d.kind==='review'?d.expected:d.intent}\n\n### ${d.kind==='review'?'実際に感じたこと':'確認基準'}\n${d.kind==='review'?d.actual:d.acceptance}\n\n### 制作・再確認の記録\n${d.implementation||'制作側が変更内容・確認方法・次に見てほしい点を返す。'}\n\n画像はこの記録に添付してください。修正依頼・回答はこの記録のコメントに集約し、完成確認後に閉じます。\n\n<!-- mou-studio:${d.id}:r${d.revision} -->`;}
export function example(kind){const d=newDoc(kind);d.title=kind==='review'?'律を心配する前に、危機が始まってしまう':'律の返事が、少しずつ噛み合わなくなる';d.surface='会話・カットシーン';d.intent='いつもの友達が急に知らない人に見える怖さ。まだ手を伸ばせば戻せると思いたい。';d.understanding='笛は人の意識に作用する。音を遮れば助けられるかもしれない。';d.action='律の異変に気づいて呼び止める。反応がなければ近づいて腕を取る。';d.before='初日の深夜。井戸で律と話している。律が機械いじりを楽しむ姿を既に見ている。';d.after='成功なら律が音への違和感を覚える。失敗なら次の周回で連絡して備える動機が残る。';d.avoid='状態表示で危険を先に説明しない。意味深な台詞を連発しない。';d.acceptance='説明なしで、笛の前後の律の変化を指摘できる。\n操作が戻ったとき、律がどちらにいるかわかる。\n次の周回に試したい行動を一つ言える。';d.steps='古井戸で会話する → 笛が鳴る → 律を見る';d.expected=d.intent;d.actual='律と親しくなる会話を読む前に危機が始まり、助けたいという気持ちが追いつかなかった。';if(kind==='storyboard'){d.shots=[{...newShot(),text:'あと少し。今、いいところ。',composition:'蒼の肩越し。律の手元と顔を同じ画面に入れる。',action:'律が縄を持ち直し、蒼に少しだけ笑う。',sound:'桶の軋み。遠い虫の音。',seconds:6,smile:.25},{...newShot(),text:'……今、何か言った？',composition:'前の画角を維持。笑みだけが消える。',action:'律の手が止まる。視線は蒼を通り過ぎる。',sound:'笛の一音。虫の音が途切れる。',seconds:7,fear:.2}];}return d;}
