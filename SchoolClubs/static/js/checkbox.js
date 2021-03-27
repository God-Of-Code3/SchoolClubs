function check(el) {
	var checkbox = el.children[1]
	checkbox.checked = !checkbox.checked
	if (checkbox.checked) {
		el.classList.add('active')
	} else {
		el.classList.remove('active')
	}
}