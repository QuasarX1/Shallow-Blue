/* Open when someone clicks on the span element */
function openNav() {
    if ($(window).width() > 576) {
        document.getElementById("myNav").style.height = "100%";
        
        setTimeout(function () {
            document.getElementById("myNav").style.transition = "0.5s";
            document.getElementById("myNav").style.width = "100%";
        }, 1);
    }
    else {
        document.getElementById("myNav").style.width = "100%";

        setTimeout(function () {
            document.getElementById("myNav").style.transition = "0.5s";
            document.getElementById("myNav").style.height = "100%";
        }, 1);
    }
    
}

/* Close when someone clicks on the "x" symbol inside the overlay */
function closeNav() {
    if ($(window).width() > 576) {
        document.getElementById("myNav").style.width = "0%";
        
        setTimeout(function () {
            document.getElementById("myNav").style.transition = "unset";
            document.getElementById("myNav").style.height = "0%";
        }, 500);
    }
    else {
        document.getElementById("myNav").style.height = "0%";
        
        setTimeout(function () {
            document.getElementById("myNav").style.transition = "unset";
            document.getElementById("myNav").style.width = "0%";
        }, 500);
    }
    
} 