// Loaded by the WebGL page. Only the same-origin studio parent can control a
// review build. Normal play never accepts review commands.
(()=>{
  if(new URLSearchParams(location.search).get('review')!=='1')return;
  let unity=null, pending=[];
  window.addEventListener('mou-review',e=>{
    if(window.parent!==window)window.parent.postMessage({channel:'mou-studio-event',packet:e.detail},location.origin);
  });
  window.addEventListener('message',e=>{
    if(e.origin!==location.origin||e.source!==window.parent||window.parent===window||e.data?.channel!=='mou-studio-command')return;
    const command=e.data.command;if(!command||typeof command.op!=='string')return;
    const json=JSON.stringify(command);if(json.length>500000){window.dispatchEvent(new CustomEvent('mou-review',{detail:{type:'error',error:'送信内容が大きすぎます。絵コンテの画像を外して送信してください。'}}));return;}
    if(unity)unity.SendMessage('MouReviewBridge','Receive',json);else if(pending.length<10)pending.push(json);
  });
  window.mouAttachReview=instance=>{unity=instance;for(const json of pending)unity.SendMessage('MouReviewBridge','Receive',json);pending=[];};
})();
