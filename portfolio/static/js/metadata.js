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

	get_filtered_tags(input_string, hidden_id){
		var hidden_element = document.getElementById(hidden_id);
		var hidden_element_list = String(hidden_element.value).split(",");

		var answer = [];
		for(var i=0; i < this._tag_list.length; ++i){
			var tag_name = this._tag_list[i].name;
			if(tag_name.includes(input_string) && !hidden_element_list.includes(tag_name)){
				if(!answer.includes(tag_name)){
					answer.push(tag_name);
				}
			}
		}
        return answer;
	}

	getKeyUpdates(keywords, start, end, order, tags){
		var answer = [];
		if(keywords!=localStorage.getItem("keywords")){
			localStorage.setItem("keywords", keywords);
			answer.push("keywords");
		}

		if(start!=localStorage.getItem("start")){
			localStorage.setItem("start", start);
			answer.push("start");
		}
		
		if(end!=localStorage.getItem("end")){
			localStorage.setItem("end", end);
			answer.push("end");
		}

		if(order!=localStorage.getItem("order")){
			localStorage.setItem("order", order);
			answer.push("order");
		}

		if(tags!=localStorage.getItem("tags")){
			localStorage.setItem("tags", tags);
			answer.push("tags");
		}
		return answer
	}

	get_filtered_results(key){
		
	}
}