burgers = document.querySelectorAll('.burger')
Array.from(burgers).forEach((burger) => {
	burger.onclick = activateBurger;
});
function activateBurger () {
	var sidebar = document.querySelector(".mobile-sidebar[data-trigger='" + this.id + "']");
	if (this.classList.contains('active')) {
		this.classList.remove('active');
		sidebar.classList.remove('active');
		document.body.classList.remove('lock')
	} else {
		this.classList.add('active');
		sidebar.classList.add('active');
		document.body.classList.add('lock')
	}
}