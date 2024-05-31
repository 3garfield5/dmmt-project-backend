let numb=0;
let num=0;
const slides = document.querySelectorAll( ".slider-img");
const navi = document.querySelectorAll( ".contr");
function Show() {
	slides[num].classList.add("bl");
    navi[num].classList.add("act");
}
function next_slid(nu){
     num = nu;
    hide();
    numb=num;
    Show();
}
function hide(){
    slides[numb].classList.remove("bl");
    navi[numb].classList.remove("act");
}

let numb1=0;
let num1=0;
const slides1 = document.querySelectorAll( ".slider-img1");
const navi1 = document.querySelectorAll( ".contr1");
function Show1() {
	slides1[num1].classList.add("bl");
    navi1[num1].classList.add("act");
}
function next_slid1(nu){
    num1 = nu;
    hide1();
    numb1=num1;
    Show1();
}
function hide1(){
    slides1[numb1].classList.remove("bl");
    navi1[numb1].classList.remove("act");
}
function Menu(){
    let me_ak = document.getElementById("me_ak1");
    let header = document.getElementById("header1");
    let cent = document.getElementById("cent1");
    let end = document.getElementById("end1");
    let bod = document.getElementById("bod1");
    let can = document.getElementById("can1");
    let a = document.getElementById("a-men");
    let os_za = document.getElementById("os_za1");
	if (me_ak.style.display === "none") {
        os_za.style.display = "none";
		me_ak.style.display = "flex";
        cent.style.display = "none";
        header.style.display = "none";
        end.style.display = "none";
        bod.style.height = "100vh";
        can.classList.remove("can1");
        a.innerHTML = "закрыть";
	}
	else {
		me_ak.style.display = "none";
        cent.style.display = "block";
        header.style.display = "flex";
        end.style.display = "flex";
        bod.style.height = "300vh";
        can.classList.add("can1");
        a.innerHTML = "меню";
	}

}
function Zaifk(){
    let me_ak = document.getElementById("me_ak1");
    let os_za = document.getElementById("os_za1");
    let header = document.getElementById("header1");
    let cent = document.getElementById("cent1");
    let end = document.getElementById("end1");
    let bod = document.getElementById("bod1");
    let cen = document.getElementById("can2");
    let r = document.getElementById("a-ost");
    if (os_za.style.display === "none") {
        me_ak.style.display = "none";
		os_za.style.display = "flex";
        cent.style.display = "none";
        header.style.display = "none";
        end.style.display = "none";
        bod.style.height = "100vh";
        cen.classList.remove("can2");
        r.innerHTML = "закрыть";
	}
	else {
		os_za.style.display = "none";
        cent.style.display = "block";
        header.style.display = "flex";
        end.style.display = "flex";
        bod.style.height = "300vh";
        cen.classList.add("can2");
        r.innerHTML = "оставить заявку";

	}
}
function sub(){
    let chekk1 = document.getElementById("checkk");
    let otpr1 = document.getElementById("otpr");
    if (chekk1.checked){
        otpr1.disabled="";
    }
    else{
        otpr1.disabled="disabled";
    }
}