
function Show() {
	let typ = document.getElementById("pasw");
	if (typ.type === "password") {
		typ.type = "text";
	}
	else {
		typ.type = "password";
	}
}