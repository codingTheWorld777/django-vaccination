// Change background color for parallax layout (self-defined)
const parallaxBg = document.getElementsByClassName("parallax")[0];
let title = document.getElementsByClassName("titre")[0];
title = (title === undefined) ? "" : title.innerHTML;
const imageBg = [
    'url("../images/vaccin_1.jpeg")',
    'url("../images/vaccin_2.jpeg")',
    'url("../images/vaccin_3.jpeg")',
    'url("../images/vaccin_4.jpeg")',
    'url("../images/vaccin_5.jpeg")',
    'url("../images/vaccin_6.jpeg")',
    'url("../images/vaccin_7.jpeg")',
];
let imageId = 0, bg;


function changeBg() {
    if (imageId < imageBg.length) {
        bg = imageBg[imageId];
        
        try {
            if (imageId === imageBg.length - 1) document.getElementsByClassName("titre")[0].innerHTML = "";
            else if (imageId === 0) document.getElementsByClassName("titre")[0].innerHTML = title;
        } catch (Exception) {
            return;
        }
        
        imageId++;
        
    } else imageId = 0;
    
    parallaxBg.style.height = "70%";
    parallaxBg.style.width = "100%";
    parallaxBg.style.transition = "all 2s";
    parallaxBg.style.background = bg;
    parallaxBg.style.backgroundPosition = "center";
    parallaxBg.style.backgroundAttachment = "fixed";
    parallaxBg.style.backgrounPosition = "center";
    parallaxBg.style.backgroundRepeat = "no-repeat";
    parallaxBg.style.backgroundSize = "cover";
}

setInterval(changeBg, 4000);