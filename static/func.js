const applyClickEventToCollapsibleBtn = () => {
    var coll = document.getElementsByClassName("collapsible")
    for (var i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    }
}

const appliClickEventToContentDiv = () => {
    var content = document.getElementsByClassName("content")
    for (var i = 0; i < content.length; i++) {
        content[i].addEventListener("click", function() {
            if (this.style.display === "block") {
                this.style.display = "none";
                this.previousSibling.classList.toggle("active");
            } else {
                this.style.display = "block";
            }
        });
    }
}

window.onload = () => {
    applyClickEventToCollapsibleBtn()
    appliClickEventToContentDiv()
}