//読み込む位置に関わらず機能するように DOMContentLoadedイベントを利用
document.addEventListener('DOMContentLoaded', () => {
  //formのclassのplanning-formを指定した最初のformを取得
  const planningForm = document.querySelector(".planning-form");

  //.planning-formを指定したformが存在するとき
  if (planningForm) {
    //エラーを表示するspan要素に付与するクラス名
    const errorClassName = 'error';
      const maxlengthElems =  document.querySelectorAll('.maxlength');

      //required クラスを指定された要素の集まり
      const requiredElems = document.querySelectorAll('.required');

      //plan-titleクラスの指定された要素
      const plantitleElems = document.querySelector('.plan-title');

      //vlog-urlクラスの指定された要素
      const vlogurlElems = document.querySelector('.vlog-url')

      //autocompleteクラスの指定された要素
      const autocompleteElems = document.querySelector('.autocomplete')


      //equal-to クラスを指定された要素の集まり
      const equalToElems = document.querySelectorAll('.equal-to');


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

    //form 要素の submit イベントを使った送信時の処理
    planningForm.addEventListener('submit', (e) => {
      //エラーを表示する要素を全て取得して削除（初期化）
      const errorElems = planningForm.querySelectorAll('.' + errorClassName);
      errorElems.forEach( (elem) => {
        elem.remove();
      });

      //.required を指定した要素を検証
      requiredElems.forEach( (elem) => {
        //値（value プロパティ）の前後の空白文字を削除
        const elemValue = elem.value.trim();
        //値が空の場合はエラーを表示してフォームの送信を中止
        if(elemValue.length === 0) {
          createError(elem, '入力は必須です');
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

      //.equal-to を指定した要素を検証
      equalToElems.forEach( (elem) => {
        //比較対象の要素の id
        const equalToId = elem.dataset.equalTo;
        //または const equalToId = elem.getAttribute('data-equal-to');
        //比較対象の要素
        const equalToElem = document.getElementById(equalToId);
        //値が空でなければ
        if(elem.value !=='' && equalToElem.value !==''){
          if(equalToElem.value !== elem.value) {
            createError(elem, '入力された値が異なります');
            e.preventDefault();
          }
        }
      });

      // //.vlog-urlを指定した要素の検証
      // vlogurlElems.forEach((elem) => {
      // //値(valueプロパティ)の前後の空白文字を削除
      // const pattern =  /^(https?|ftp)(:\/\/[-_.!~*\'()a-zA-Z0-9;\/?:\@&=+\$,%#]+)$/;


      // //値が空じゃない場合
      // if (elem.value !== '') {
      //   //test()メソッドで値を判定し、マッチしなければエラーを表示してフォームの送信んを中止
      //   //test() メソッドは、正規表現と指定された文字列の一致を調べるための検索を実行しま
      //   if (!pattern.test(elem.value)) {
      //     createError(elem, "Emailアドレスの形式が正しくないようです");
      //     e.preventDefault();
      //   }
      // }
      // });



    //エラーの最初の要素を取得
    const errorElem =  planningForm.querySelector('.' + errorClassName);
    //エラーがあればエラーの最初の要素の位置へスクロール
    if(errorElem) {
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


