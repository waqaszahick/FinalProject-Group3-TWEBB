var key = sessionStorage.getItem('key');

d3.json('/recommend_movies/'+key).then(function(data){
console.log(data.length);
if(data.length > 1){
	d3.select('#name').text(data[0].name);
	d3.select('#rating').text("RATING: "+data[0].rating+" / 10");
	d3.select('#synopsis').text(data[0].synopsis);

	d3.select('.poster').attr("src", function() {
    const imagePath =data[0].poster;
    return imagePath;
  });
  d3.select('#trailer').on('click',function(){
  	window.open(data[0].trailer,'_blank');
  });
 
		var items = d3.select('.items').append('div').attr('class','row');
		console.log(data[1].length);
		data[1].every(item => {
		console.log(item);
		//  items.append('li').append('div').attr('class','bg-img').attr('style','background-image: url('+item.poster+');').append('a').attr('href',`javascript:fetchRelatedMovie(\"${item.name}\");`).append('div').attr('class','content').append('h2').text(item.name);
		 items.append('div').attr('class','card col-sm-2').append('a').attr('href',`javascript:fetchRelatedMovie(\"${item.name}\");`).append('img').attr('src',item.poster);
		console.log(item.name);
		console.log(item.poster);
		return true;
		});

  }else{
	alert("No Movie Found");
  }
});
function fetchRelatedMovie(newkey){
 var oldkey = key;
 sessionStorage.setItem("key", newkey);
 location.reload();
}
