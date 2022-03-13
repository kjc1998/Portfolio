function getElementByXpath(path) {
	return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function confirmationPopUp(button){
	var text = `Are you sure to proceed with ${button.getAttribute('name')}?`;
	if (confirm(text)==false){
		return false;
	};
}