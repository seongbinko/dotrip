// 간단한 회원가입 함수입니다.
// 아이디, 비밀번호, 닉네임을 받아 DB에 저장합니다.
function signUp() {
    if(check_dup()) {
        $.ajax({
            type: "POST",
            url: "/api/sign-up",
            data: {
                id_give: $('#id_give').val(),
                pw_give: $('#pw_give').val(),
                pwConfirm_give: $('#pwConfirm_give').val()
            },
            success: function (response) {
                if (response['result'] == 'success') {
                    alert('회원가입이 완료되었습니다.') 
                    $.cookie('mytoken', response['token']);
                    window.location.href = "/";
                } else {
                    alert(response['msg'])
                }
            }
        })
    }                
}
function check_dup() {
    let id = $("#id_give").val()
    let password = $("#pw_give").val();
    let passwordConfirm = $("#pwConfirm_give").val();
    if (id == "") {
        alert("아이디를 입력해주세요")
        $("#id_give").focus()
        return false;
    }
    if (!is_nickname(id)) {
        $("#idHelp").text("아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 3-20자 길이까지").removeClass("text-muted").addClass("text-danger");
        $("#id_give").focus()
        return false;
    }
    if (password == "") {
        alert("패스워드를 입력해주세요");
        $("#pw_give").focus()
        return false;
    }
    if (!is_password(password)) {
        $("#passwordHelp").text("패스워드 형식을 확인해주세요. 영문과 숫자조합, 일부 특수문자(._-) 사용 가능. 8-20자 길이까지").removeClass("text-muted").addClass("text-danger");
        $("#pw_give").focus()
        return false;
    }
    if (passwordConfirm == "") {
        alert("패스워드 확인을 입력해주세요");
        $("#pwConfirm_give").focus()
        return false;
    }
    if (!is_password(passwordConfirm)) {
        $("#passwordConfirmHelp").text("패스워드 형식을 확인해주세요. 영문과 숫자조합, 일부 특수문자(._-) 사용 가능. 8-20자 길이").removeClass("text-muted").addClass("text-danger");
        $("#pwConfirm_give").focus()
        return false;
    }
    return true;
}
function is_nickname(asValue) {
    var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{3,10}$/;
    return regExp.test(asValue);
}

function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}                      