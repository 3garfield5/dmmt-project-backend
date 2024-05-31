function tram(n){
    let lik = document.getElementById(`${n}`);
    let noty = document.getElementById(`l ${n}`);
    if (lik.style.display === "block"){
        lik.style.display = "none";
        noty.style.display = "block";
    }
    else{
        noty.style.display = "none";
        lik.style.display = "block";
    }
}
/*
function Show() {
	slides[num].classList.remove("no");
}
function tram(nu){
    num = nu;
    hide();
    numb=num;
    Show();
}
function hide(){
    slides[numb].classList.add("no");
    let NL = document.getElementById("NL");
    let LL = document.getElementById("LL");
   if (NL.style.display === "none"){
        lik.style.display = "block";
        no.style.display = "none";
    }
}*/
