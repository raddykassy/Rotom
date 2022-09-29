$.validator.setDefaults({
  submitHandler: function() { alert("submitted!"); }
});

$().ready(function() {
  $('#login_form').validate({
    rules: {
      email: {
        required: true,
        email: true
      },
      password: {
        required: true,
        password: true,
      }
    },
      messages: {
        email: {
          required: 'メールアドレスが入力されていません',
          email: '正しいemail形式で入力してください'
        },
        password: {
          required: '入力されていません',
          password:'パスワードが入力されていません'
        }
      }
  });
});

$().ready(function() {
  $("#register_id").validate({
    rules: {
      email: {
        required: true,
        email: true
      },
      password: {
        required: true,
        password: true,
      },
      confirm_password: {
        required: true,
        password: true,
        equalTo: '[name=password]',
      },
      username: {
        required: true,
      },
    },
      messages: {
        email: {
          required: 'メールアドレスが入力されていません',
          email: '正しいemail形式で入力してください'
        },
        password: {
          required: '入力されていません',
          password:'パスワードが入力されていません'
        },
        confirm_password: {
          required:'入力されていません',
          password: 'パスワードが入力されていません',
          equalTo: '同じパスワードを入力してください'
        },
        username: {
          required: 'ユーザーネームが入力されていません',
        },
      },
          // エラーメッセージ出力箇所
      errorPlacement: function(error, element){
        var name = element.attr('name');
        error.appendTo($('.is-error-'+name));
    },

      errorElement: "span",
      errorClass: "is-error",
  });
});


$().ready(function() {
  $("#form_id").validate({
  rules: {
      plan_title: {
        required: true
      },
      vlog_url: {
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
      plan_title: {
        required: "プランタイトルを入力してください"
      },
      vlog_url: {
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
    },

      // エラーメッセージ出力箇所
      errorPlacement: function(error, element){
        var name = element.attr('name');
        error.appendTo($('.is-error-'+name));
    },

      errorElement: "span",
      errorClass: "is-error",
  });
  });
