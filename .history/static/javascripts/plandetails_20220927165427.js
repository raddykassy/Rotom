console.log("読み込みOK")

function butotnClick(){
    console.log("クリックOK")
    const rating_obj = document.querySelectorAll('.plan-place-details-star-input');
    rating_obj.forEach(function(rating, index){
        console.log(rating)
        const elememt1 = rating.value;
        const element = rating_obj[index].value;
        console.log(elememt1);
        console.log(element);
        //セレクトのオブジェクト

        //オプションのオブジェクト
    });
}

document.addEventListener('DOMContentLoaded', () => {
    let checkButton = document.querySelector('.post-form-button');
    checkButton.addEventListener('click', butotnClick);

})