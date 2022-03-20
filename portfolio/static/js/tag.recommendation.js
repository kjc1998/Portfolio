class TagRecommendation{
    constructor(instance_name, holder_id, input_id, hidden_input_id, datalist_id, holder_tags, full_list_tags, match_input=false){
        this._instance_name = instance_name;

        this._holder_id = holder_id;
        this._input_id = input_id;
        this._hidden_input_id = hidden_input_id;
        this._datalist_id = datalist_id;

        this._holder_tags = holder_tags;
        this._full_tag_list = full_list_tags.map(element=>element.name);
        this._match_input = match_input;
    }

    /// GET METHODS ///
    get_input_field(){
        var input_element = document.getElementById(this._input_id);
        var tag = input_element.value.replace(/\s+/g, " ");
        return tag.trim().toLowerCase();
    }

    get_filtered_tags(input_string){
		var hidden_element_list = String(document.getElementById(this._hidden_input_id).value).split(",");
		var answer = [];
		for(var i=0; i < this._full_tag_list.length; ++i){
			var tag_name = this._full_tag_list[i];
			if(tag_name.includes(input_string) && !hidden_element_list.includes(tag_name)){
				if(!answer.includes(tag_name)){
					answer.push(tag_name);
				}
			}
		}
        return answer;
	}

    /// DOM METHODS ///
    display_tag(){
        $(`#${this._holder_id} li`).remove();
		this._holder_tags.slice().reverse().forEach(tag=>{
			var liTag = `<li class="tags">${tag} <i class="uit uit-multiply" onclick="${this._instance_name}.remove_tag('${tag}')"></i></li>`;
			document.getElementById(this._holder_id).insertAdjacentHTML("afterbegin", liTag);
		})
    }

    remove_tag(tag){
		var index = this._holder_tags.indexOf(tag);
		this._holder_tags = [...this._holder_tags.slice(0, index), ...this._holder_tags.slice(index + 1)];
		this.display_tag();
        this.append_hidden_tag();
        var input_field = this.get_input_field();
        this.append_datalist(this.get_filtered_tags(input_field));
	}

    append_hidden_tag(){
		document.getElementById(this._hidden_input_id).value = "";
		var hidden_string = ""
		for(var i=0; i < this._holder_tags.length; ++i){
			hidden_string += `,${this._holder_tags[i]}`;
		}
		$(`#${this._hidden_input_id}`).val(hidden_string.substring(1)).trigger("change");
	}

    append_datalist(datalist){
		$(`#${this._datalist_id} option`).remove();
		for(var i=0; i < datalist.length; ++i){
			var option = document.createElement('option');
			option.value = datalist[i];
			document.getElementById(this._datalist_id).appendChild(option);
		}
	}

    /// EVENT LISTENER METHODS ///
    tag_bar_event(instance, event){
        if(instance._match_input){
            if(event.key=="Enter" || event.key==undefined){
                var tag = instance.get_input_field();
                if(instance._full_tag_list.includes(tag) && tag){
                    if(!instance._holder_tags.includes(tag) && tag){
                        event.target.value = "";
                        
                        instance._holder_tags.push(tag);
                        instance.display_tag();
                        instance.append_hidden_tag();
                        instance.append_datalist(instance.get_filtered_tags(""));
                    }else{alert("This tag has been added")}
                }else{
                    if(tag){alert("No Such Tag")}
                };
            };
        }else{
            if(event.key=="Enter"){
                var tag_string = document.getElementById(instance._input_id).value.replace(/\s+/g, " ");
                if(tag_string.length > 0){
                    var tag_array = tag_string.split(",").map(element => element.trim());
                    var unique_array = [...new Set(tag_array)];
                    unique_array.forEach(tag=>{
                        tag = tag.trim();
                        if(!instance._holder_tags.includes(tag) && tag){
                            instance._holder_tags.push(tag.toLowerCase());
                        }
                    });
                    instance.display_tag();
                    instance.append_hidden_tag();
                    instance.append_datalist(instance.get_filtered_tags(""));
                };
                event.target.value = "";
            }
        }
    };

    hidden_input_event(instance, event){
        var filtered_tags = instance.get_filtered_tags(event.target.value);
        instance.append_datalist(filtered_tags);
    }
}