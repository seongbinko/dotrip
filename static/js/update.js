$(document).ready(function () {
  bsCustomFileInput.init();
});

function update() {
  let title = $('#title').val();
  let content = $('#content').val();
  let file = $('#file')[0].files[0];
  let idValue = window.location.pathname.split('/')[2];

  if (title === '') {
    alert('제목을 추가해주세요.');
    $('#title').focus();
    return;
  } else if (content === '') {
    alert('내용을 추가해주세요.');
    $('#content').focus();
    return;
  }

  let form_data = new FormData();
  if (file === undefined) {
    form_data.append('title_give', title);
    form_data.append('content_give', content);
    form_data.append('id_give', idValue);
  } else {
    form_data.append('file_give', file);
    form_data.append('title_give', title);
    form_data.append('content_give', content);
    form_data.append('id_give', idValue);
  }

  $.ajax({
    type: 'PUT',
    url: '/api/reviews',
    data: form_data,
    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      alert(response['msg']);
      window.location.href = `/reviews/${idValue}`;
      console.log(data);
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

function deleteReview() {
  let idValue = window.location.pathname.split('/')[2];
  $.ajax({
    type: 'DELETE',
    url: '/api/reviews' + '?id_give=' + idValue,

    cache: false,
    contentType: false,
    processData: false,
    success: function (response) {
      alert(response['msg']);
      window.location.href = '/reviews';
    },
  });
}

function cancelBtn() {
  let idValue = window.location.pathname.split('/')[2];
  window.location.href = `/reviews/${idValue}`;
}
