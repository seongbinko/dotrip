function infinity(){
  window.onscroll = function(e){
    if((window.innerHeight + window.scrollY) >= document.body.offsetHeight){
      console.log('다 내려왔다.')
      const temp_html = `<div class="card" style="width: 350px">
                            <img src="../static/img/img.jpg" class="card-img-top" alt="...">
                            <div class="card-body">
                              <h5 class="card-title">
                              <a href="...">첫번째 카드</a> //TODO: 주소 변경 필요
                              </h5>
                              <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                            </div>
                            <ul class="list-group list-group-flush">
                              <li class="list-group-item">작성일</li>
                              <li class="list-group-item">작성자 아이디</li>
                            </ul>
                        </div>
`
      $('.card__wrap').append(temp_html);
    }
  }
}






infinity();
