/**
 * Created by Jackson on 10/3/16.
 */
$(document).ready(function () {
    function update() {
        if (!checkAuth()) {
            $('#usernav').remove();
        } else {
            $('#actionnav').remove();
            $('#userbar').text(getUsername());
        }
    }

    $('#login-form').submit(function (e) {
        e.preventDefault();

        $.post('/login', {
            username: $('#username-login').val(),
            password: $('#password-login').val()
        }).done(function (res) {
            if (res.status === 200) {
                $('#login').modal('hide');
                Cookies.set('token', res.token);
                update()
            } else {
                alert("Bad login!");
            }
        });
    });

    $('#register-form').submit(function (e) {
        e.preventDefault();

        $.post('/register', {
            username: $('#username-register').val(),
            password: $('#password-register').val(),
            email: $('#email').val(),
            full_name: $('#name').val()
        }).done(function (res) {
            if (res.status === 200) {
                $('#register').modal('hide');
                Cookies.set('token', res.token);
                update()
            } else {
                alert("Bad registration!");
            }
        });
    });

    update();
});

var checkAuth = function () {
    return (function () {
        var response = null;

        $.ajax({
            'method': 'POST',
            'async': false,
            'global': false,
            'url': '/auth',
            'data': {token: Cookies.get('token') || -1},
            'success': function (res) {
                response = res.status == 200;
            }
        });

        return response;
    })();
};

var getUsername = function () {
    if (checkAuth()) {
        return (function () {
            var response = null;

            $.ajax({
                'method': 'POST',
                'async': false,
                'global': false,
                'url': '/get_user',
                'data': {token: Cookies.get('token') || -1},
                'success': function (res) {
                    console.dir(res);
                    response = res.username;
                }
            });

            return response;
        })();
    } else {
        return '';
    }
};