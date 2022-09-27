var placeContainer = document.getElementById('place-container');

var placeCount = 1;
// var elements = {};

// 場所を追加ボタンが押された際のinputタグの追加処理
var addPlanBtn = document.getElementById('add-plan-btn');

addPlanBtn.addEventListener('click', function() {
    var placeBox = getInputTag();
    InsertInputTag(placeBox);
});


// 場所選択ボックスの作成
function getInputTag() {
    placeCount++;
    //値が一致するかの検証。data-equal-to で指定した要素と比ベル、data-equal-toを追加 9/24航輔（後日コメント削除してください）
    var elements = '<div class="mb-3">\
                        <input type="text" class="form-control post-form-control autocomplete" data-equal-to="autocomplete" id="autocomplete_' + placeCount + '" name="place_' + placeCount + '"placeholder="場所を入力し、選択して下さい" required>\
                        <input type="hidden" id="place_name_' + placeCount + '" name="place_name_' + placeCount + '"placeholder="場所を入力し、選択して下さい">\
                        <input type="hidden" id="place_id_' + placeCount + '" name="place_id_' + placeCount + '"placeholder="場所を入力し、選択して下さい">\
                    </div>';
    return elements;
}

function InsertInputTag(placeBox) {
    placeContainer.insertAdjacentHTML('beforeend', placeBox);
}
