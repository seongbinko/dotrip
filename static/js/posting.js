$(document).ready(function () {
  bsCustomFileInput.init();
  listing();
});

function listing() {
  $.ajax({
    type: 'GET',
    url: '/api/reviews',
    data: {},
    success: function (response) {
      let reviews = response['all_reviews'];
      for (let i = 0; i < reviews.length; i++) {
        let title = reviews[i]['title'];
        let content = reviews[i]['content'];
        let file = reviews[i]['file'];
        let time = reviews[i]['time'];

        let temp_html = `<div class="card">
                                            <img src="../static/img/${file}" class="card-img-top">
                                            <div class="card-body">
                                                <h5 class="card-title">${title}</h5>
                                                <p class="card-text">${content}</p>
                                                <p class="save-date">${time}</p>
                                            </div>
                                        </div>`;
        $('#cards-box').append(temp_html);
      }
    },
  });
}

function posting() {
  let title = $('#title').val();
  let content = $('#content').val();
  let file = $('#file')[0].files[0];
  let form_data = new FormData();

  form_data.append('file_give', file);
  form_data.append('title_give', title);
  form_data.append('content_give', content);

  $.ajax({
    type: 'POST',
    url: '/api/reviews',
    data: form_data,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      alert(response['msg']);
      window.location.reload();
    },
  });
}

function preview(input) {
  if (input.files && input.files[0]) {
    let reader = new FileReader();
    reader.onload = function (e) {
      $('#img-preview').attr('src', e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
}
