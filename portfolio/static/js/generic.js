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

	setUserID(myValue) {
		$('#sTags_final').val(myValue).trigger('change');
	}
}

class MetadataHandling{
	constructor(project_list, story_list, tag_list){
		this._project_list = project_list;
		this._story_list = story_list;
		this._tag_list = tag_list;
	}

	get_tag_list(){
		var tag_list = this._tag_list.map(element=>element.name);
		return tag_list;
	}

	get_filtered_tags(input_string, hidden_id, datalist_id){
		var hidden_element = document.getElementById(hidden_id);
		var hidden_element_list = String(hidden_element.value).split(",");

		var datalist_element = document.getElementById(datalist_id);
		var answer = [];
		for(var i=0; i < this._tag_list.length; ++i){
			var tag_name = this._tag_list[i].name;
			if(tag_name.includes(input_string) && !hidden_element_list.includes(tag_name)){
				if(!answer.includes(tag_name)){
					answer.push(tag_name);
				}
			}
		}
		$(`#${datalist_id} option`).remove(); // clear then append
		for(var i=0; i < answer.length; ++i){
			var option = document.createElement('option');
			option.value = answer[i];
			datalist_element.appendChild(option);
		}
	}
}