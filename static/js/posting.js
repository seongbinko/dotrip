$(document).ready(function () {
  bsCustomFileInput.init();
});

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
