console.log("読み込みOK")

function butotnClick(){
    console.log("クリックOK")
    document.addEventListener('DOMContentLoaded', () => {
        const rating_obj = document.querySelectorAll('.plan-place-details-star-input');
        rating_obj.forEach(function(rating, index){
            const elememt1 = rating.value;
            const element = rating_obj[index].value;
            console.log(elememt1);
            console.log(element);
            //セレクトのオブジェクト

            //オプションのオブジェクト
        });
    });
}

let checkButton = document.getElementById('#plan-details-post-button');
checkButton.addEventListener('click', butotnClick);
