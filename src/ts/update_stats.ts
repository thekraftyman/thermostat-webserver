function update_stats() {
  $.getJSON( '/stats', function(data) {
    // determine C or F
    var temp_unit: string = "C";
    var temp_int: number | string = parseInt(data.TEMP);
    if (temp_int > 50){
      temp_unit = "F";
    }

    // convert to F for comfort comparison
    if (temp_unit == "C") {
      temp_int = (temp_int * (9/5)) + 32;
      if (typeof temp_int === "string"){
        temp_int = parseInt(temp_int);
      }
    }

    // get temp span class
    var temp_class: string = "perfect";
    if (temp_int < 64) {
      temp_class = "cold";
    } else if (temp_int > 75) {
      temp_class = "hot";
    }

    // set the temp, mode, and fan values
    $("#temp").html(`${data.TEMP}&deg;${temp_unit}`);
    $("#mode").html(`${data.MODE}`);
    $("#fan").html(`${data.FAN}`);
    $("#tempstat").attr("class","stat " + temp_class);
  });
  // repeat
  setTimeout( update_stats, 5000);
}
update_stats();
