// callback function
var input_num;
let autocomplete = {};

function initMap() {
    const test_place = { lat: 34.6460706, lng: 135.5134771 };
    let opts = {
        zoom: 15,
        center: test_place,
    }

    // goole.maps.Mapクラスのコンストラクタは第1引数にmapを挿入するタグ、第2引数にoptionを指定
    const map = new google.maps.Map(document.getElementById("map"), opts)

    const marker = new google.maps.Marker({
        position: test_place,
        map: map,
    })


    let countPlaces;

    // Autocompleteのインスタンスを作成する際に使用するOPTIONの指定（施設、日本地域限定に設定）
    var option = {
        types: ["establishment"],
        componentRestrictions: {"country": ["jp"]},
    };

    // https://developers.google.com/maps/documentation/javascript/reference/places-widget#SearchBox
    // 1番目のinputタグにautocomplete機能を搭載（1番目の要素のみid = "autocomplete"をもつため）
    first_input = document.getElementById("autocomplete");
    autocomplete[0] = new google.maps.places.Autocomplete(first_input, option);


    //ボタンが押された回数だけautocompleteクラスを持ったinputタグができる(addplan.js)→2番目の要素を持ったものを取得
    var addPlanBtn = document.getElementById('add-plan-btn');

    // 後でdocument全体からクラス検索ではなく、あるidをもつ親要素を指定して検索範囲を限定する（リファクタリングで実装）https://www.sejuku.net/blog/68588
    addPlanBtn.addEventListener('click', function() {
        countPlaces = document.getElementsByClassName("autocomplete"); //autocompleteクラスを持つ要素を取得
        input_num = countPlaces.length; //autocompleteクラスを持つ要素の数を取得
        num = input_num - 1; //autocompleteのインスタンスをinputの順番に応じたキーに対して配列に格納するので、配列のゼロインデックスに合わせるため1を引く
        // console.log(countPlaces[num]);
        autocomplete[num] = new google.maps.places.Autocomplete(countPlaces[num], option);
    });



    // autocomplete.forEach((elm) => {
    //     elm.addListener("place_changed", console.log([].slice.call(autocomplete).indexOf(elm)));
    // });

    // https://developers.google.com/maps/documentation/javascript/reference/places-widget#Autocomplete.place_changed
    // autocomplete.addListener("place_changed", onPlaceChanged); //event

    // // 検索候補がクリックされた際のイベントの定義
    // function onPlaceChanged(key) {
    //     // 選択された場所の情報を取得
    //     var place = autocomplete[key].getPlace();

    //     // place.キー名で情報受け取れる
    //     console.log(place);
    //     // console.log(place.website);
    //     // console.log(document.getElementById("site_url").getAttribute("src"))

    //     // geometryがあるかどうか（場所が実在するか否か）
    //     if(!place.geometry) {
    //         document.getElementById("autocomplete").placeholder = "Enter a place";
    //         console.log("not")
    //     } else {
    //         // 場所が存在している場合
    //         // 場所の名前表示
    //         // document.getElementById("details").innerHTML = place.name;
    //         // webサイトを取ってきて、aタグに入れる
    //         // var website = document.getElementById("site_url");
    //         // website.setAttribute("href", place.website);
    //         // website.innerHTML = place.website;
    //         console.log(place.name);
    //     }
    // }
}


// window.initMap = initMap