$.validator.setDefaults({
  submitHandler: function() { alert("submitted!"); }
});

$().ready(function() {
  $("#form_id").validate({
  rules: {
      plantitle: {
        required: true
      },
      vlogurl: {
        required: true,
        url: true,
      },
      place01: {
        required: true,
      },
      place_0: {
        required: true
      },
      autocomplete_1:{
        required: true,
      },
      autocomplete_0:{
        required: true,
      },
      description: {
        required: true,
      },
  },
  messages: {
      plantitle: {
        required: "プランタイトルを入力してください"
      },
      vlogurl: {
        required:"入力してください",
        url:"URL形式で入力してください"
      },
      place01: {
        required: "場所を選択してください",
      },
      place_1: {
        required:'場所を入力してください'
      },
      autocomplete_1: {
        required: '場所を入力してください'
      },
      autocomplete_0: {
        required: '場所を入力してください'
      },
      description: {
        required: '場所を入力してください'
      },
    }
  });
  // propose username by combining first- and lastname

  });
