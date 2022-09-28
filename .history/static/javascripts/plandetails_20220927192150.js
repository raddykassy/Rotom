console.log("読み込みおk")
// 投稿ボタンクリック時
function butotnClick(){
    console.log("クリックOK")
    
    const rating_obj = document.querySelectorAll('.plan-place-details-star-input');
    const price_obj = document.querySelectorAll('.plan-place-details-price');
    const url_obj = document.querySelectorAll('.plan-place-details-url');
    const comment_obj = document.querySelectorAll('.plan-place-details-comment-2');

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
        comment_li.push(url.comment)
    });

    console.log(rating_li)
    console.log(price_li)
    console.log(url_li)





}

document.addEventListener('DOMContentLoaded', () => {
    let checkButton = document.querySelector('.post-form-button');
    checkButton.addEventListener('click', butotnClick);

})