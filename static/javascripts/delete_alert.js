function deleteComfirm(plan_id){

         const result = window.confirm("この投稿を消去しますか？");
         console.log(result)
         if(result){
            location.href=`/delete/${plan_id}`;
            //console.log("ok");
         }
//});
}