console.log("読み込みおk")
// 投稿ボタンクリック時
function butotnClick(){
    console.log("クリックOK")
    
    const rating_obj = document.querySelectorAll('.plan-place-details-star-input');
    const price_obj = document.querySelectorAll('.plan-place-details-price);

    rating_obj.forEach(function(rating, index){
        const elememt1 = rating.value;
        console.log(elememt1);
    });


}

document.addEventListener('DOMContentLoaded', () => {
    let checkButton = document.querySelector('.post-form-button');
    checkButton.addEventListener('click', butotnClick);

})