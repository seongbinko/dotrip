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
  let imgfile = input.files;
  let filetype = imgfile[0].type.split('/').pop().toLowerCase();

  if (imgfile && imgfile[0]) {
    let reader = new FileReader();
    reader.onload = function (e) {
      if ($.inArray(filetype, ['jpg', 'jpeg', 'png', 'gif']) == -1) {
        alert('jpg, jpeg, png, gif 파일만 업로드 해주세요.');
        $('#img-preview').attr('src', `../static/img/defaultimg.jpg`);
        $('#posting-btn').attr('disabled', true);
        return;
      }

      $('#img-preview').attr('src', e.target.result);
      $('#posting-btn').removeAttr('disabled');
    };
    reader.readAsDataURL(input.files[0]);
  }
}
