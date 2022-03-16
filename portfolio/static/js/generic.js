function getElementByXpath(path) {
	return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function confirmationPopUp(button){
	var text = `Are you sure to proceed with ${button.getAttribute('name')}?`;
	if (confirm(text)==false){
		return false;
	};
}


// Tag Handling
class TagHandling{
	constructor(tag_input_id, tag_holder_id, hiddenID, tag_list=null){
		this.tag_input_id = tag_input_id;
		this.tag_holder_id = tag_holder_id;
		this.hiddenID = hiddenID;

		this.tag_input = document.getElementById(tag_input_id);
		this.tag_holder = document.getElementById(tag_holder_id);
		this.hidden_tag = document.getElementById(hiddenID);

		if(tag_list){
			this.tags = tag_list;
		}else{
			this.tags = [];
		}
	}

	displayTag(instance_name){
		$(`#${this.tag_holder_id} li`).remove();
		this.tags.slice().reverse().forEach(tag=>{
			var liTag = `<li class="tags">${tag} <i class="uit uit-multiply" onclick="${instance_name}.removeTag('${tag}', '${instance_name}')"></i></li>`;
			this.tag_holder.insertAdjacentHTML("afterbegin", liTag);
		})
	}

	removeTag(tag, instance_name){
		var index = this.tags.indexOf(tag);
		this.tags = [...this.tags.slice(0, index), ...this.tags.slice(index + 1)];
		this.displayTag(instance_name);
		this.appendToHiddenTag();
	}

	appendToHiddenTag(){
		this.hidden_tag.value = ""; // reset to default before readjust
		var hidden_string = ""
		for(var i=0; i < this.tags.length; ++i){
			hidden_string += `,${this.tags[i]}`;
		}
		$(`#${this.hiddenID}`).val(hidden_string.substring(1)).trigger("change");
	}

	appendToDataList(datalist, datalist_id){
		var datalist_element = document.getElementById(datalist_id);
		$(`#${datalist_id} option`).remove(); // clear then append
		for(var i=0; i < datalist.length; ++i){
			var option = document.createElement('option');
			option.value = datalist[i];
			datalist_element.appendChild(option);
		}
	}
}