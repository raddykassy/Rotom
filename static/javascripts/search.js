// callback function
const autocomplete = [];
let places_info = [];
let specific_place_info = {};
// var zoo;

function initMap() {
    const test_place = { lat: 34.6460706, lng: 135.5134771 };
    const opts = {
        zoom: 15,
        center: test_place,
    }

    // goole.maps.Mapクラスのコンストラクタは第1引数にmapを挿入するタグ、第2引数にoptionを指定
    const map = new google.maps.Map(document.getElementById("map"), opts)

    const marker = new google.maps.Marker({
        position: test_place,
        map: map,
    })


    // Autocompleteのインスタンスを作成する際に使用するOPTIONの指定（施設、日本地域限定に設定）
    const option = {
        types: ["establishment"],
        componentRestrictions: {"country": ["jp"]},
    };

    // https://developers.google.com/maps/documentation/javascript/reference/places-widget#SearchBox
    // 1番目のinputタグにautocomplete機能を搭載（1番目の要素のみid = "autocomplete"をもつため）
    const first_input = document.getElementById("autocomplete");
    autocomplete[0] = new google.maps.places.Autocomplete(first_input, option);
    autocomplete[0].addListener("place_changed", function() {
        const first_info = autocomplete[0].getPlace();
        const place_name = first_info.name;
        const place_id = first_info.place_id;
        const name_1 = document.getElementById("place_name_1");
        const id_1 = document.getElementById("place_id_1");

        name_1.value = place_name;
        id_1.value = place_id;

        

        // console.log(first_info);
        // console.log(first_info.geometry.viewport.Bb.hi);
        // console.log(first_info.geometry.viewport.Va.hi);


        specific_place_info = { place_name : place_name,
                                place_id : place_id
                            };
        places_info[0] = specific_place_info;
        console.log(places_info);
        const hiddenField = document.getElementById("places_data");
        // console.log(places_info.join());

        // places_info.forEach(function(value){
        //     var property = Object.entries(value);


        //     property.forEach(function(v) {
        //         zoo += v.join(':');
        //         zoo += ',';
        //     });
        // });
        // console.log(zoo);
        // hiddenField.value = places_info;

    })


    //ボタンが押された回数だけautocompleteクラスを持ったinputタグができる(addplan.js)→2番目の要素を持ったものを取得
    const addPlanBtn = document.getElementById('add-plan-btn');

    // 後でdocument全体からクラス検索ではなく、あるidをもつ親要素を指定して検索範囲を限定する（リファクタリングで実装）https://www.sejuku.net/blog/68588
    addPlanBtn.addEventListener('click', function() {
        const countPlaces = document.getElementsByClassName("autocomplete"); //autocompleteクラスを持つ要素を取得
        const input_num = countPlaces.length; //autocompleteクラスを持つ要素の数を取得
        const num = input_num - 1; //autocompleteのインスタンスをinputの順番に応じたキーに対して配列に格納するので、配列のゼロインデックスに合わせるため1を引く
        const ac = new google.maps.places.Autocomplete(countPlaces[num], option); //autocomplete機能をinputタグに付加
        autocomplete[num] = ac; //autocomplete機能をinputタグに付加 (クロージャのため一度変数に格納し、代入ている(ac))

        // console.log(autocomplete[num]);

        ac.addListener("place_changed", function() {
            const place = ac.getPlace();
            place_name = place.name;
            place_id = place.place_id;
            specific_place_info = { place_name : place_name,
                                    place_id : place_id
                        };
            places_info[num] = specific_place_info;

            const name_tag = document.getElementById("place_name_" + input_num);
            const id_tag = document.getElementById("place_id_" + input_num);

            name_tag.value = place_name;
            id_tag.value = place_id;


            // places_info.forEach(function(value){
            //     var property = Object.entries(value);


            //     property.forEach(function(v) {
            //         zoo += v.join(':');
            //         zoo += ',';
            //     });
            // });
            // console.log(zoo);


            // hiddenField = document.getElementById("places_data");
            // hiddenField.value = places_info;

            console.log(places_info);
            // console.log(place);
        });
    });




    // autocomplete.forEach(function(elem) {
    //     console.log(elem)
    // }
        // elm.addListener("place_changed", console.log([].slice.call(autocomplete).indexOf(elm)));

    // https://developers.google.com/maps/documentation/javascript/reference/places-widget#Autocomplete.place_changed
    // autocomplete.addListener("place_changed", onPlaceChanged); //event

    // // 検索候補がクリックされた際のイベントの定義
    // function onPlaceChanged(content) {
    //     // 選択された場所の情報を取得
    //     // console.log(content.getPlace());
    //     var place = content.getPlace();

    //     // place.キー名で情報受け取れる
        // console.log(place);
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