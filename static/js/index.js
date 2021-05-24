d3.select('.search_icon').on('click',search);
d3.select('.searchbar').on('submit',search);

function search(){
  var key = d3.select("#searchBar").node().value;
  sessionStorage.setItem("key", key); 
}
