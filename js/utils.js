// read parameter specified on the URL
function get_from_url(name, def){
   if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
      return decodeURIComponent(name[1]);
  return def;
}

// Load a new page in the current tab
function load_url(url){
    console.log("Loading URL: " + url);
    window.location.href = url;
}

//function call_sequential(functions, i=0){
//    var func = functions[i];
//    console.log("Calling function " + func);
//    var result = func();
//    $.when(result).done(function (){
//        console.log("-> returned");
//        if (i < (functions.length-1))
//            call_sequential(functions, i+1);
//    });
//};
