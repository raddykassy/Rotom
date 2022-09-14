// callback function
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

    let autocomplete;

    // https://developers.google.com/maps/documentation/javascript/reference/places-widget#SearchBox
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById("autocomplete"),
        {
            // establishment 施設
            types: ["establishment"],
            componentRestrictions: {"country": ["jp"]},
        });

    // https://developers.google.com/maps/documentation/javascript/reference/places-widget#Autocomplete.place_changed
    autocomplete.addListener("place_changed", onPlaceChanged); //event

    // 検索候補がクリックされた際のイベントの定義
    function onPlaceChanged() {
        // 選択された場所の情報を取得
        var place = autocomplete.getPlace();

        // place.キー名で情報受け取れる
        console.log(place);
        // console.log(place.website);
        // console.log(document.getElementById("site_url").getAttribute("src"))

        // geometryがあるかどうか（場所が実在するか否か）
        if(!place.geometry) {
            document.getElementById("autocomplete").placeholder = "Enter a place";
            console.log("not")
        } else {
            // 場所が存在している場合
            // 場所の名前表示
            // document.getElementById("details").innerHTML = place.name;
            // webサイトを取ってきて、aタグに入れる
            // var website = document.getElementById("site_url");
            // website.setAttribute("href", place.website);
            // website.innerHTML = place.website;
            console.log(place.name);
        }
    }
}


// window.initMap = initMap