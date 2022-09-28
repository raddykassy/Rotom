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

    const btn = document.querySelector('.post-form-button');

    let tmp_data = {};

    tmp_data["rating_li"] = rating_li
    tmp_data["price_li"] = price_li
    tmp_data["url_li"] = url_li
    tmp_data["comment_li"] = comment_li


    let data = [{"data": tmp_data}];
    let json_data = JSON.stringify(data)
    console.log(data)

    sendData(data);

}


// 投稿ボタンクリック
document.addEventListener('DOMContentLoaded', () => {
    let checkButton = document.querySelector('.post-form-button');
    checkButton.addEventListener('click', butotnClick);

})


// データ送信
function sendData(data) {
    console.log('Sending data');
  
    const XHR = new XMLHttpRequest();
  
    // const urlEncodedDataPairs = [];
  
    // data: {

    //     "rating_li": [], 
    //     "price_li": [],

    // }

    // data オブジェクトを、URL エンコードしたキーと値のペアの配列に変換します
    // for (const [name, value] of Object.entries(data)) {
    //   urlEncodedDataPairs.push(`${encodeURIComponent(name)}=${encodeURIComponent(value)}`);
      
    //   urlEncodedDataPairs.push(`rating_li=${encodeURIComponent(value["rating_li"])}`);
    //   urlEncodedDataPairs.push(`price_li=${encodeURIComponent(value["price_li"])}`);
    //   urlEncodedDataPairs.push(`url_li=${encodeURIComponent(value["url_li"])}`);
    //   urlEncodedDataPairs.push(`comment_li=${encodeURIComponent(value["comment_li"])}`);

    // }


  //   送信
  
   // キーと値のペアをひとつの文字列に連結して、ウェブブラウザーのフォーム送信方式に
   // 合うよう、エンコードされた空白をプラス記号に置き換えます。
    // const urlEncodedData = urlEncodedDataPairs.join('&').replace(/%20/g, '+');
  
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
    XHR.send(data);
  }
  
  btn.addEventListener('click', () => {
    sendData({ test: 'ok' });
  })

