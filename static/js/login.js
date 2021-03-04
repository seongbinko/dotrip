function login() {

    let id_give = $("#id_give").val();
    let pw_give = $("#pw_give").val();

    if (id_give == "") {
        alert("아이디를 입력해주세요");
        return false;
    }
    if (pw_give == "") {
        alert("패스워드를 입력해주세요");
        return false;
    }

    $.ajax({
        type: "POST",
        url: "/api/login",
        data: { id_give: id_give, pw_give: pw_give },
        success: function (response) {
            if (response['result'] == 'success') {
                // 로그인이 정상적으로 되면, 토큰을 받아옵니다.
                // 이 토큰을 mytoken이라는 키 값으로 쿠키에 저장합니다.
                $.cookie('mytoken', response['token']);
                window.location.href = '/'
            } else {
                // 로그인이 안되면 에러메시지를 띄웁니다.
                alert(response['msg'])
            }
        }
    })
}