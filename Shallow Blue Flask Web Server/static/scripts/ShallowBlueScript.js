/* Open when someone clicks on the span element */
function openNav() {
    if ($(window).width() > 576) {
        document.getElementById("myNav").style.display = "unset";
        document.getElementById("myNav").style.width = "100%";
    }
    else {
        document.getElementById("myNav").style.display = "unset";
        document.getElementById("myNav").style.height = "100%";
    }
    
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    if ($(window).width() > 576) {
        document.getElementById("myNav").style.width = "0%";

        setTimeout(function () { document.getElementById("myNav").style.display = "none"; }, 500); 
    }
    else {
        document.getElementById("myNav").style.height = "0%";

        setTimeout(function () { document.getElementById("myNav").style.display = "none"; }, 500);
    }
    
} 