let map;
let infoWindow = [];
let center = {
  lat: 34.7019399, // 緯度
  lng: 135.51002519999997 // 経度
};

let youtube_url = plan_info[0]["url"];
let youtube_id = youtube_url.split("/")[3]

let markerData = [ // マーカーを立てる場所名・緯度・経度
  {
    //    name: 'TAM 東京',
    //    lat: 35.6954806,
    //     lng: 139.76325010000005,
    //     icon: 'tam.png' // TAM 東京のマーカーだけイメージを変更する
 }
];

for (place_data in place_info_li){
    place_array = {

    name: place_data['place'],
    lat: place_data['latitude'],
    lng: place_data['longitude'],

    }

    markerData.push(place_array)

}

console.log(markerData)


let open_or_close = Array(markerData.length);

function initMap() {
    let opts = {
        center: center, // 地図の中心を指定
        zoom: 15,
        center: new google.maps.LatLng({lat: markerData[0]['lat'], lng: markerData[0]['lng']})
    };
    let map = new google.maps.Map(document.getElementById("map"), opts);
    marker = new google.maps.Marker({ // マーカーの追加
        position: center, // マーカーを立てる位置を指定
        map: map // マーカーを立てる地図を指定
   });

 // マーカー毎の処理
 for (let i = 0; i < markerData.length; i++) {
        markerLatLng = new google.maps.LatLng({lat: markerData[i]['lat'], lng: markerData[i]['lng']}); // 緯度経度のデータ作成
        marker[i] = new google.maps.Marker({ // マーカーの追加
         position: markerLatLng, // マーカーを立てる位置を指定
            map: map // マーカーを立てる地図を指定
       });
 
     infoWindow[i] = new google.maps.InfoWindow({ // 吹き出しの追加
         content: '<div class="sample">' + markerData[i]['name'] + '</div>' // 吹き出しに表示する内容
       });
 
     markerEvent(i); // マーカーにクリックイベントを追加
 }

 // マーカーにクリックイベントを追加
function markerEvent(i) {
    marker[i].addListener('click', function() { // マーカーをクリックしたとき
        open_or_close_window(i)
    });
 
  }
}


//windowの表示、非表示
function open_or_close_window(i){
    if (open_or_close[i] == null || open_or_close[i] == "close"){
        //開いていたwindowがある場合は閉じる
        for (j in open_or_close){
 
            if (open_or_close[j] == "open"){
                infoWindow[j].close(map, marker[j]);
                open_or_close[j] = "close"
            }
        }
        infoWindow[i].open(map, marker[i]);
        open_or_close[i] = "open"
      } else if (open_or_close[i] = "open"){
        infoWindow[i].close(map, marker[i]);
        open_or_close[i] = "close"
    }
}

//youtube動画を反映
document.addEventListener('DOMContentLoaded', function() {
    let element = document.querySelector('.youtube-video');
    element.src = `https://www.youtube.com/embed/${ youtube_id }?autoplay=1`
})

//liをクリックしてマーカーのwindowを表示させる
document.addEventListener('DOMContentLoaded', function() {
    let place_li = document.querySelectorAll(".list-item");
    place_li.forEach(function(li, index){
        li.onclick =function() {
            open_or_close_window(index)
            //対応する動画の部分を再生させる。
            let youtube_video = document.querySelector('.youtube-video');
            youtube_video.setAttribute("src", `https://www.youtube.com/embed/${youtube_id}?autoplay=1&start=${50*index}`);
        }
    })
})
