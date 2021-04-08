function update_stats() {
  console.log("Updating stats...");
  $.getJSON( '/stats', function(data) {
    // console.log(data);
    $("#temp").html(`Temp: ${data.TEMP}`);
    $("#mode").html(`Mode: ${data.MODE}`);
    $("#fan").html(`Fan: ${data.FAN}`);
  });
  // repeat
  setTimeout( update_stats, 5000);
}
update_stats();
