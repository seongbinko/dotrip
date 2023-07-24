const count = parseInt($("#review_count").val());
const total_count = parseInt($("#total_count").val());
let skipIndex = parseInt(count);
const limit = parseInt(count);

function infinity(){
  window.onscroll = function(e){
    if((window.innerHeight + window.scrollY) >= document.body.offsetHeight){
      if(total_count <= skipIndex) {
        return false;
      } else {
        $.ajax({
          type: "GET",
          url: "/api/reviews",
          data: {
              skipIndex: skipIndex,
              limit: limit
          },
          success: function (response) {
              const reviews = (response['reviews'])
              const file_url = "/static/img/";
              $.each(reviews, function (index, review) {
                let appendInfo = `<div class="card" style="width: 350px">
                                    <img src="${file_url + review.review_file}" class="card-img-top" alt="...">
                                    <div class="card-header">
                                      <h5 class="text-center">
                                        <a href="reviews/${review._id}">${review.review_title}</a>
                                      </h5>
                                      </div>
                                      <ul class="list-group list-group-flush">
                                        <li class="list-group-item">${review.review_content}</li>
<!--                                        <li class="list-group-item">${review.review_create_date}</li> -->
                                        <li class="list-group-item">${review.author}</li>
                                    </ul>
                                </div>`
                $("#reviews_list").append(appendInfo);
                skipIndex++;
            })
  
          }
        })
      }
    }
  }
}
infinity();
