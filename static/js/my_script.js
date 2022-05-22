function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

$(".correct_answer").on('click', function (ev) {
    const $this = $(this)

    const request = new Request(
        'http://127.0.0.1:8000/correct_answer/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-type': 'application/x-www-form-urlencoded'
            },
            body: 'answer_id=' + $this.data('id')
        }
    );

    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            console.log(parsed.is_correct)
            $this.prop('checked', parsed.is_correct)
        });

    });
});


$(".button-like").on('click', function (ev) {
    const $this = $(this);


    const request = new Request(
        'http://127.0.0.1:8000/vote/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-type': 'application/x-www-form-urlencoded'
            },
            body: 'question_id=' + $this.data('id')+'&vote=1',

        }
    );
    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            console.log(parsed.likes);
            // $this.html('<button type="button" data-id="{{ question.id }}" class="btn btn-dark  button-like"><div>parsed.new_rating &#128293</div></button>'
            // )

            $this.text(parsed.likes );
            $this.next().text(parsed.dislikes);
        });

    })
})


$(".button-dislike").on('click', function (ev) {
    console.log('dislike');
    const $this = $(this);

    const request = new Request(
        'http://127.0.0.1:8000/vote/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-type': 'application/x-www-form-urlencoded'
            },
            body: ['question_id=' + $this.data('id')+'&vote=-1'
            ]
        }
    );

    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            console.log(parsed.dislikes);
            $this.prev().text(parsed.likes);
            $this.text(parsed.dislikes );
        });

    })
})

$(".button-like-answer").on('click', function (ev) {
    const $this = $(this);

    const request = new Request(
        'http://127.0.0.1:8000/vote/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-type': 'application/x-www-form-urlencoded'
            },
            body: 'answer_id=' + $this.data('id')+'&vote=1',

        }
    );
    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            console.log(parsed.likes);
            // $this.html('<button type="button" data-id="{{ question.id }}" class="btn btn-dark  button-like"><div>parsed.new_rating &#128293</div></button>'
            // )

            $this.text(parsed.likes );
            $this.next().text(parsed.dislikes);
        });

    })
})

$(".button-dislike-answer").on('click', function (ev) {
    const $this = $(this);

    const request = new Request(
        'http://127.0.0.1:8000/vote/',
        {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-type': 'application/x-www-form-urlencoded'
            },
            body: ['answer_id=' + $this.data('id')+'&vote=-1'
            ]
        }
    );

    fetch(request).then(function (response) {
        response.json().then(function (parsed) {
            console.log(parsed.dislikes);
            $this.prev().text(parsed.likes);
            $this.text(parsed.dislikes );
        });

    })
})
