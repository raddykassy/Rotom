console.log("読み込みおk")
// 投稿ボタンクリック時
function butotnClick(){
    console.log("クリックOK")
    
    const rating_obj = document.querySelectorAll('.plan-place-details-star-input');
    const price_obj = document.querySelectorAll('.plan-place-details-price');
    const url_obj = document.querySelectorAll('.plan-place-details-url');
    const comment_obj = document.querySelectorAll('.plan-place-details-comment-2');

    // 場所のインデックスと紐づいた場所の詳細情報
    let rating_li = [];
    let price_li = [];
    let url_li = [];
    let comment_li = [];

    rating_obj.forEach(function(rating, index){
        rating_li.push(rating.value)
    });

    price_obj.forEach(function(price, index){
        price_li.push(price.value)
    });

    url_obj.forEach(function(url, index){
        url_li.push(url.value)

    });

    comment_obj.forEach(function(comment, index){
        comment_li.push(comment.value)
    });

    console.log(rating_li)
    console.log(price_li)
    console.log(url_li)


    const btn = document.querySelector('.post-form-button');

    data=[]
    data.push(rating_li)
    data.push(price_li)
    data.push(url_li)

    sendData(data);

}

document.addEventListener('DOMContentLoaded', () => {
    let checkButton = document.querySelector('.post-form-button');
    checkButton.addEventListener('click', butotnClick);

})


function sendData(data) {
    console.log('Sending data');
  
    const XHR = new XMLHttpRequest();
  
    const urlEncodedDataPairs = [];
  
    // data オブジェクトを、URL エンコードしたキーと値のペアの配列に変換します
    for (const [name, value] of Object.entries(data)) {
      urlEncodedDataPairs.push(`${encodeURIComponent(name)}=${encodeURIComponent(value)}`);
    }


  //   送信
  
   // キーと値のペアをひとつの文字列に連結して、ウェブブラウザーのフォーム送信方式に
   // 合うよう、エンコードされた空白をプラス記号に置き換えます。
    const urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');
  
    // データが正常に送信された場合に行うことを定義します
    XHR.addEventListener('load', (event) => {
      alert('Yeah! Data sent and response loaded.');
    });
  
    // エラーが発生した場合に行うことを定義します
    XHR.addEventListener('error', (event) => {
      alert('Oops! Something went wrong.');
    });
  
    // リクエストをセットアップします
    XHR.open('POST', '/post-details');
  
    // フォームデータの POST リクエストを扱うために必要な HTTP ヘッダを追加します
    XHR.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  
    // 最後に、データを送信します
    XHR.send(urlEncodedData);
  }
  
  btn.addEventListener('click', () => {
    sendData({ test: 'ok' });
  })

