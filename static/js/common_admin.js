function modifyLinkContent(id) {
    let element = document.getElementById(id);
    if (element) {
        let content = `<i class="fa-solid fa-chevron-right" style="font-weight: bold;"></i> <u>{TEXT}</u> <i class="fa-solid fa-chevron-left" style="font-weight: bold;"></i>`;
        let innerText = element.innerText.trim();
        content = content.replace("{TEXT}", innerText);
        element.innerHTML = content;

        let parentElement = element.parentElement;
        if (parentElement.classList.contains("expand")) {
            parentElement.classList.replace("expand", "expand-active");
        }
    } else {
        console.error("Element with id '" + id + "' not found.");
    }
}
modifyLinkContent(linkId);

$("#UPS").click(function(){
    $(".expand").not("#expandUPS").slideUp(200);
    $("#expandUPS").slideToggle(200);
});
$("#UPSMON").click(function(){
    $(".expand").not("#expandUPSMON").slideUp(200);
    $("#expandUPSMON").slideToggle(200);
});
$("#UPSD").click(function(){
    $(".expand").not("#expandUPSD").slideUp(200);
    $("#expandUPSD").slideToggle(200);
});