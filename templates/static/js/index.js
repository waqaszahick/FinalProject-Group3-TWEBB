function searchByNameData(){
    var key = d3.select("#searchBar").node().value;
    d3.json('recommended_movies/'+key).then(function(data){
      console.data(data);
    }); 
  }