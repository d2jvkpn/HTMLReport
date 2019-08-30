// https://github.com/d2jvkpn/HTMLReport

"use strict"

function chaIndex () {
    var nav = document.getElementById("mySidenav");
    var eles = document.getElementById("main").children;
    var index = [0, 0, 0], p = 0, k=0;

    for (let el of eles) {
        if (el.nodeName != "DIV") {
            continue;
        }
        var dv = el.getAttribute("data-level");
        var n = parseInt(dv, 10), t = el.getAttribute("name"), e;
        if (t == undefined) { t =""; }

        if (isNaN(n)) {n = 0;};
        if (n > index.length || n < 0) {
            console.log("Invalid div data-level: " + n);
            return;
        }

        if (p > n && n > 0) {
            for (var j=n; j<index.length; j++ ) {index[j] = 0;}
        }

        if (n>0) {
                p = n;    index[n-1]++;
                t = index.slice(0, n).join(".") + ". "+ t;
                e = document.createElement("h"+n);
        } else {
                e = document.createElement("h1");
        }

        e.innerHTML = t;
        el.prepend(e);

        if (el.id == "") {
            if (n>0) {
                el.id = "h"+index.slice(0, n).join(".");
            } else {
                k++; el.id = "k"+k;
            }
        }

        console.log("Add heading: " + t);

        var e = document.createElement("a");
        e.href = "#" + el.id;
        e.title = t;
        if (n>0) {
                e.innerHTML = "&nbsp".repeat((n-1)*2) + t;
        } else {
                e.innerHTML = t;
        }
        if (n <= 1) { e.setAttribute("class", "nav1");}
        if (n == 2) { e.setAttribute("class", "nav2");}
        nav.appendChild(e);
        console.log("Add heading: " + t);
    }
}

function tabIndex () {
    var eles = document.querySelectorAll("figure.myTable");

    for (var i=0; i < eles.length; i++) {
        var prefix = "<span style='font-weight:bold'>Table " + (i+1) + ". </span>";
        var name = eles[i].getAttribute("name");
        var el = document.createElement("figcaption");

        if (name == null) {name="";};
        if (eles[i].id == "") { eles[i].id = "Table" + (i+1);};
        el.innerHTML = prefix + name;
        eles[i].prepend(el);
        console.log("Edit table.myTable figcaption: " + el.innerText);

        if (eles[i].querySelector("table") == null) {
            console.log("Warning not children table in figure.myTable: " + el.innerText);
            continue;
        }

        var maxchar = 20, tds = eles[i].querySelectorAll("td, th");
        for(let e of tds) {
            e.innerHTML = e.innerHTML.replace(/^\s+|\s+$/g, '');
            if(e.innerHTML.length > maxchar ) {
                e.title = e.innerHTML;
                e.innerHTML = e.innerHTML.slice(0, maxchar-3) + "...";
            }
        }
    }
}


function displayImg(id, n){
    if (n != -1 && n != 1) { return; }

    var fig = document.getElementById(id);
    var imgs = fig.getElementsByTagName("img");
    var k = parseInt(fig.getAttribute("data-imgIdx"));
    imgs[k].style.display = "none";
    k = k+n;

    if (k > imgs.length -1) { k = 0;}

    if (k < 0) { k = imgs.length-1;}
    // console.log("process " + id    + ", change to " +(k+1));
    imgs[k].style.display = "block";
    fig.setAttribute("data-imgIdx", k);
    var ratio = fig.getElementsByTagName("span")[0];
    ratio.innerHTML = k + 1 + " / " + imgs.length +", " + imgs[k].alt;
}

function baseName(s, rmsuffix) {
    var tmp = s.split("/"), title = tmp[tmp.length-1];
    if (rmsuffix) {
        title = title.split(".").slice(0, -1).join(".");
    }
    return title;
}


function figSlide() {
    var figs = document.querySelectorAll("figure.mySlide");

    for (var i=0; i<figs.length; i++) {
        var prefix = "<span style='font-weight:bold'>Figure " + (i+1) + ". </span>";
        var name = figs[i].getAttribute("name");
        var el = document.createElement("figcaption");
        var children = figs[i].childNodes;
        if ( name == null) { name = "";};
        el.innerHTML = prefix + name;
        if(figs[i].id == "") {figs[i].id = "Figure" + (i+1);};
        figs[i].appendChild(el);

        console.log("Edit figure.mySlide figcaption: " + el.innerText);

        figs[i].setAttribute("data-imgIdx", 0);

        var imgs = figs[i].getElementsByTagName('img');
        console.log("Process figure.mySlide: "+ el.innerText + ", x" + imgs.length);

        if (imgs.length == 0) { continue;}

        for (let j=0; j< imgs.length; j++) {
	    var bn = baseName(imgs[j].src, true);
            if (!imgs[j].hasAttribute("alt")) { imgs[j].alt = bn; }
            if (!imgs[j].hasAttribute("title")) { imgs[j].title = bn; }
            if (j == 0) {
                imgs[j].style.display = "block";
            } else {
                imgs[j].style.display = "none";
            }
        }

        if (imgs.length == 1) { continue; }

        var bt = document.createElement("p");
        var b1 = document.createElement("button");
        var b2 = document.createElement("button");
        var ratio = document.createElement("span");
        bt.setAttribute("class", "title");
        b1.innerHTML = "&#10094;";
        b2.innerHTML = "&#10095;";
        ratio.innerHTML =    1 + " / " + imgs.length +", " + imgs[0].alt;

        bt.appendChild(b1);
        bt.appendChild(ratio);
        bt.appendChild(b2);
        imgs[imgs.length -1].insertAdjacentElement("afterend", bt)

        b1.addEventListener("click", displayImg.bind(null, figs[i].id, -1));
        b2.addEventListener("click", displayImg.bind(null, figs[i].id, 1));
    }
}

function refIndex() {
    var ref = document.getElementById("reference");
    if (ref == undefined) { return; };

    var n = 0;
    for (let p of ref.querySelectorAll("p")) {
        var anchors = document.getElementsByName(p.id);

        if (p.id == "") {
            console.log("Skip referenc withoutid");
        }

        if (anchors.length == 0) {
             console.log("Skip unused reference: " + p.id);
        }

        if (p.id == "" || anchors.length == 0) {
             p.style.display = "none";
             continue;
        }

        n+=1;
        console.log("Found anchor(s) match reference: " + p.id);
        p.innerHTML = "[" + n + "] " + p.innerText.replace(/^\s+|\s+$/g, '');

        for (let a of anchors) {
            a.href = "#" + a.name;
            a.innerHTML = "[" + n + "]";
            a.style.textDecoration = "none";
            a.title = p.innerHTML;
        }
    }
}

function Index() {
    console.log("Indexing...");
    chaIndex(); tabIndex(); figSlide(); refIndex();
    console.log("Done!")
}
