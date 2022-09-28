console.log("読み込みおk")
// 投稿ボタンクリック時
function butotnClick(){
    console.log("クリックOK")
    
    const rating_obj = document.querySelectorAll('.plan-place-details-star-input');
    const price_obj = document.querySelectorAll('.plan-place-details-price');
    const url_obj = document.querySelectorAll('.plan-place-details-url');

    rating_obj.forEach(function(rating, index){
        const elememt1 = rating.value;
        console.log(elememt1);
    });

    price_obj.forEach(function(price, index){
        const elememt1 = price.value;
        console.log(elememt1);
    });

    url_obj.forEach(function(url, index){
        const elememt1 = url.value;
        console.log(elememt1);
    });




}

document.addEventListener('DOMContentLoaded', () => {
    let checkButton = document.querySelector('.post-form-button');
    checkButton.addEventListener('click', butotnClick);

})