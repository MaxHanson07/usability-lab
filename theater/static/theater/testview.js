// sidebar.js
function showTranscript(data) {
    console.log(data)


    $("#sidebar-content h2").text("Transcript");
    $("#sidebar p").text(data.utterances);
  }
  