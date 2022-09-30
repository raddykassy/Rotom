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
        },
      },

      // エラーメッセージ出力箇所
      errorPlacement: function(error, element){
        var errorKey = $(element).attr('id') + 'Error';
        $('#error_' + errorKey).remove();
        element.addClass('is-invalid');
        const errorP = $('<p>').text(error[0].innerText);
        const errorDiv = $('<div class="invalid-feedback" id="error_' + errorKey + '">').append(errorP);
        element.parent().append(errorDiv);
      },
      success: function(error, element) {
        var errorKey = $(element).attr('id') + 'Error';
        $('#error_' + errorKey).remove();
        $(error).remove();
        $(element).removeClass('is-invalid');
        $(element).removeClass('error');
      },
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
        var errorKey = $(element).attr('id') + 'Error';
        $('#error_' + errorKey).remove();
        element.addClass('is-invalid');
        const errorP = $('<p>').text(error[0].innerText);
        const errorDiv = $('<div class="invalid-feedback" id="error_' + errorKey + '">').append(errorP);
        element.parent().append(errorDiv);
      },
      success: function(error, element) {
        var errorKey = $(element).attr('id') + 'Error';
        $('#error_' + errorKey).remove();
        $(error).remove();
        $(element).removeClass('is-invalid');
        $(element).removeClass('error');
      },
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
      days: {
        required: true,
      },
      costs: {
        required: true,
        number: true,
        digits: true
      },
      place01: {
        required: true,
      },
      place_2: {
        required: true
      },
      place_3: {
        required: true
      },
      place_4: {
        required: true
      },
      place_5: {
        required: true
      },
      place_6: {
        required: true
      },
      place_7: {
        required: true
      },
      place_8: {
        required: true
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
        required:"URLを入力してください",
        url:"URL形式で入力してください"
      },
      days: {
        required: "旅行日数を選んでください",
      },
      costs: {
        required: '予算を入力してください',
        number: '予算を入力してください',
        digits: '数字のみを入力してください'
      },
      place01: {
        required: "場所を選択してください",
      },
      place_2: {
        required: "場所を選択してください",
      },
      place_3: {
        required: "場所を選択してください",
      },
      place_4: {
        required: "場所を選択してください",
      },
      place_5: {
        required: "場所を選択してください",
      },
      place_6: {
        required: "場所を選択してください",
      },
      place_7: {
        required: "場所を選択してください",
      },
      place_8: {
        required: "場所を選択してください",
      },
      description: {
        required: '旅行の概要を入力してください'
      },
    },

      // エラーメッセージ出力箇所
      errorPlacement: function(error, element){
        var errorKey = $(element).attr('id') + 'Error';
        $('#error_' + errorKey).remove();
        element.addClass('is-invalid');
        const errorP = $('<p>').text(error[0].innerText);
        const errorDiv = $('<div class="invalid-feedback" id="error_' + errorKey + '">').append(errorP);
        element.parent().append(errorDiv);
      },
      success: function(error, element) {
        var errorKey = $(element).attr('id') + 'Error';
        $('#error_' + errorKey).remove();
        $(error).remove();
        $(element).removeClass('is-invalid');
        $(element).removeClass('error');
      },
  });
  });
