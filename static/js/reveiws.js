function infinity(){
  window.onscroll = function(e){
    if((window.innerHeight + window.scrollY) >= document.body.offsetHeight){
      console.log('이거 왜 안되지..?')
      const temp_html = `<div class="card" style="width: 350px">
                            <img src="../static/img/img.jpg" class="card-img-top" alt="...">
                            <div class="card-body">
                              <h5 class="card-title">
                              <a href="...">왜 안바뀌지 소름</a> 
                              </h5>
                              <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                            </div>
                            <ul class="list-group list-group-flush">
                              <li class="list-group-item">${date}</li>
                              <li class="list-group-item">${userId}</li>
                            </ul>
                        </div>
`
      $('.card__wrap').append(temp_html);
    }
  }
}




infinity();
