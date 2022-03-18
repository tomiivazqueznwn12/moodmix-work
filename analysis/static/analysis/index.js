function myFunction(output) {
    var loader = document.getElementById("loader");
    var songs = document.getElementById("songs");
    if (songs.style.display == 'block'){
        songs.style.display = "none";
        loader.style.display = "block";
    }
    loader.style.display = "block";
  }