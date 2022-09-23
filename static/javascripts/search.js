function initMap() {

    // goole.maps.Mapクラスのコンストラクタは第1引数にmapを挿入するタグ、第2引数にoptionを指定
    // const map = new google.maps.Map(document.getElementById("map"), opts)

    // Autocompleteのインスタンスを作成する際に使用するOPTIONの指定（施設、日本地域限定に設定）
    const option = {
        types: ["establishment"],
        componentRestrictions: {"country": ["jp"]},
    };


    // 場所選択BOXにオートコンプリート機能の追加・place_idの取得 → app.pyへ渡す
    const place_box = document.getElementById("place_box");
    const place_id_box = document.getElementById("place_id_box");

    autocomplete = new google.maps.places.Autocomplete(place_box, option);

    autocomplete.addListener("place_changed", function() {
        const place_info = autocomplete.getPlace();
        const place_id = place_info.place_id;

        place_id_box.value = place_id;
    })
}