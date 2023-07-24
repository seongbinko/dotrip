$(document).ready(function () {
    const url_string = window.location.search;
    if(url_string.includes('token_expired')) {
        $.removeCookie('mytoken', {path: '/'})
        const not_login_user_html = `<li class="nav-item">
                                        <a class="nav-link" href="/login"><i class="fa fa-sign-in" aria-hidden="true"></i>로그인</a>
                                    </li>
                                    <li class="nav-item">
                                        <a class="nav-link" href="/sign-up"><i class="fa fa-address-card" aria-hidden="true"></i>회원가입</a>
                                    </li>`
        $("#show_user_by_token").empty().append(not_login_user_html);
        $("#show_review_save_button_by_token").empty();
    }

    let token = $.cookie('mytoken');
    if (token !== undefined) {
        token = JSON.parse(atob(token.split('.')[1]));
        $("#user_id").text(token.id + '님 환영합니다')

    }

    let now = new Date();
    let start = new Date('2023-04-15');

    let timeDiff = now.getTime() - start.getTime();
    let day = Math.floor(timeDiff / (1000 * 60 * 60 * 24) + 2);
    $('#love-day').text('  +' + day);
})

function logout() {
    $.removeCookie('mytoken', {path: '/'});
    window.location.href = '/';
}