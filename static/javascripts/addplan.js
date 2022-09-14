var placeContainer = document.getElementById('place-container');

var placeCount = 1;
// var elements = {};

// 場所を追加ボタンが押された際のinputタグの追加処理
var addPlanBtn = document.getElementById('add-plan-btn');

addPlanBtn.addEventListener('click', function() {
    var placeBox = getInputTag();
    InsertInputTag(placeBox);
});

// aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

// 場所選択ボックスの作成
function getInputTag() {
    placeCount++;
    var elements = '<div class="mb-3">\
                        <label for="place" class="form-label">' + placeCount + '番目</label>\
                        <input type="text" class="form-control" id="place" name="place0' + placeCount + '"placeholder="場所を入力し、選択して下さい">\
                    </div>';
    return elements;
}

function InsertInputTag(placeBox) {
    placeContainer.insertAdjacentHTML('beforeend', placeBox);
}