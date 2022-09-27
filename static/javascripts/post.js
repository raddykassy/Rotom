
//読み込む位置に関わらず機能するように DOMContentLoadedイベントを利用
document.addEventListener('DOMContentLoaded', () => {
    //formのclassのplanning-formを指定した最初のformを取得
    const planningForm = document.querySelector(".planning-form");

    //.planning-formを指定したformが存在するとき
    if (planningForm) {
      //エラーを表示するspan要素に付与するクラス名
      const errorClassName = 'error';
      //console.log(errorClassName); これいけてる

        //maxlength クラスを指定された要素の集まり
        const maxlengthElems =  document.querySelectorAll('.maxlength');

        //required クラスを指定された要素の集まり
        const requiredElems = document.querySelectorAll('.required');
        console.log(requiredElems);

        //plan-titleクラスの指定された要素
        const plantitleElems = document.querySelector('.plan-title');

        //vlog-urlクラスの指定された要素
        const vlogurlElems = document.querySelector('.vlog-url')

        //autocompleteクラスの指定された要素
        const autocompleteElems = document.querySelector('.autocomplete')
        console.log(autocompleteElems);

        //equal-to クラスを指定された要素の集まり
        const equalToElems = document.querySelectorAll('.equal-to');
        console.log(equalToElems);

        //エラーメッセージを表示する span 要素を生成して親要素に追加する関数
        //elem ：対象の要素
        //errorMessage ：表示するエラーメッセージ
        const createError = (elem, errorMessage) => {
          //span 要素を生成
          const errorSpan = document.createElement('span');
          //エラー用のクラスを追加（設定）
          errorSpan.classList.add(errorClassName);
          //aria-live 属性を設定
          errorSpan.setAttribute('aria-live', 'polite');
          //引数に指定されたエラーメッセージを設定
          errorSpan.textContent = errorMessage;
          //elem の親要素の子要素として追加
          elem.parentNode.appendChild(errorSpan);
        }
        console.log(createError);

        //form要素のsubmitイベントを使った送信時の処理
        planningForm.addEventListener('submit', (e) => {
          //エラーを表示する要素をすべて取得して削除(初期化)
          const errorElems = planningForm.querySelectorAll('.' + errorClassName);
          errorElems.forEach( (elem) => {
            elem.remove();
          });

          //.requiredを指定した要素を検証
          requiredElems.forEach((elem) => {
            //値(valueプロパティ)の前後の空白文字を削除
            const elemValue = elem.value.trim();

            //値がからの場合はエラーを表示してフォームの送信を中止
            if (elemValue.legth === 0) {
              createError(elem, '入力が必要です');
              e.preventDefault();
            }
          });

          //.plan-titleを指定した要素の検証
          plantitleElems.forEach((elem) => {
            //値(valueプロパティ)の前後の空白文字を削除
            const elemValue = elem.value.trim();

            //値がからの場合はエラーを表示してフォームの送信を中止
            if (elemValue.legth === 0) {
              createError(elem, '入力が必要です');
              e.preventDefault();
            }
          });

                //.maxlength を指定した要素を検証
        maxlengthElems.forEach( (elem) => {
          //data-maxlength 属性から最大文字数を取得
          const maxlength = elem.dataset.maxlength;
          //または const maxlength = elem.getAttribute('data-maxlength');
          //値が空でなければ
          if(elem.value !=='') {
            //値が maxlength を超えていればエラーを表示してフォームの送信を中止
            if(elem.value.length > maxlength) {
              createError(elem, maxlength + '文字以内でご入力ください');
              e.preventDefault();
            }
          }
        });

          //.vlog-urlを指定した要素の検証
          vlogurlElems.forEach((elem) => {
            //値(valueプロパティ)の前後の空白文字を削除
            const pattern =  /^(https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)$/;
            console.log(pattern)

            //値が空じゃない場合
            if (elem.value !== '') {
              //test()メソッドで値を判定し、マッチしなければエラーを表示してフォームの送信んを中止

              //test() メソッドは、正規表現と指定された文字列の一致を調べるための検索を実行しま
              if (!pattern.test(elem.value)) {
                createError(elem, "Emailアドレスの形式が正しくないようです");
                e.preventDefault();
              }
            }
          });

          //エラーの最初の要素を取得
          const errorElem = planningForm.querySelector('.' + errorClassName);
          //エラーがあれば最初の要素の位置へスクロール
          if (errorElem) {
            const errorElemOffsetTop = errorElem.offsetTop;
            window.scrollTo({
              top: errorElemOffsetTop - 40,  //40px 上に位置を調整
              //スムーススクロール
              behavior: 'smooth'
            });
          }
        });
    }
  });


// callback function
const autocomplete = [];
let places_info = [];
let specific_place_info = {};
// var zoo;

function initMap() {

    // ---------------------Map表示部分-------------------------------
    const test_place = { lat: 34.665442, lng: 135.4323382 };
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
    // -----------------------------------------------------------------


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
        const place_sum = document.getElementById("place_sum");

        name_1.value = place_name;
        id_1.value = place_id;

        // console.log(first_info);
        // console.log(first_info.geometry.location.lat());
        // console.log(first_info.geometry.location.lng());
        // console.log(first_info.geometry.viewport.Bb.hi);
        // console.log(first_info.geometry.viewport.Va.hi);


        specific_place_info = { place_name : place_name,
                                place_id : place_id
                            };
        places_info[0] = specific_place_info;
        console.log(places_info);
        // const hiddenField = document.getElementById("places_data");
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

    var input_num = 1;


    //ボタンが押された回数だけautocompleteクラスを持ったinputタグができる(addplan.js)→2番目の要素を持ったものを取得
    const addPlanBtn = document.getElementById('add-plan-btn');

    // 後でdocument全体からクラス検索ではなく、あるidをもつ親要素を指定して検索範囲を限定する（リファクタリングで実装）https://www.sejuku.net/blog/68588
    addPlanBtn.addEventListener('click', function() {
        const countPlaces = document.getElementsByClassName("autocomplete"); //autocompleteクラスを持つ要素を取得
        input_num = countPlaces.length; //autocompleteクラスを持つ要素の数を取得
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

            console.log(places_info);
        });
    });


    // 場所の数をinputタグ(hidden)に挿入
    const place_sum = document.getElementById('place_sum');
    const post_btn = document.getElementById('submit-plan-btn');
    post_btn.addEventListener('click', function() {
        place_sum.value = input_num;
    });

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
