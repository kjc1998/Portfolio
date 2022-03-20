/// DOM MANAGEMENT ///
function keywordParser(event){
	var string = event.target.value.toLowerCase();
	var string_list = string.split(" ")
		.map(element=> element.replaceAll(",", "").trim())
		.filter(element=>element);
	var value_string = string_list.join(",");
	$("#sKeywords_final").val(value_string).trigger("change");
};

function metadataDOMManagement(project_list, story_list){
	var projectDOM = $("#queryProjects ul");
	var storyDOM = $("#queryStories ul");

	projectDOM.empty();
	storyDOM.empty();
	for(var i in project_list){
		var project = project_list[i];

		var li_tag = document.createElement("li");
		var a_tag = `<a href=${project.url}>${project.name}</a>`;
		li_tag.innerHTML = a_tag;
		projectDOM.append(li_tag);
	}
	for(var i in story_list){
		var story = story_list[i];

		var li_tag = document.createElement("li");
		var a_tag = `<a href=${story.url}>${story.name}</a>`;
		li_tag.innerHTML = a_tag;
		storyDOM.append(li_tag);
	}
}

/// CLASS HANDLING ///
class MetadataHandling{
	constructor(project_list, story_list, tag_list){
		this._project_dict = new Object();
		this._story_dict = new Object();

		this._key_list = ["keywords", "start", "end", "tags"]
		this._project_list = project_list;
		this._story_list = story_list;
		this._tag_list = tag_list;
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

	filter_results(key){
		var value = localStorage.getItem(key);
		var projects = this._project_list;
		var stories = this._story_list;

		if(key == "keywords"){
			var keyword_list = JSON.parse(value);
			for(var i in keyword_list){
				var keyword = keyword_list[i];
				// name
				var current_projects = this._project_list.filter(element=>element.name.toLowerCase().includes(keyword));
				var story_name = this._story_list.filter(element=>element.name.toLowerCase().includes(keyword));
				// content
				var story_content = this._story_list.filter(element=>element.content.toLowerCase().includes(keyword));
				var current_stories = [...new Set([...story_name, ...story_content])];
				// match
				projects = projects.filter(value=>current_projects.includes(value));
				stories = stories.filter(value=>current_stories.includes(value));
			}
		}else if(key == "start"){
			var start_date = value;
			if(start_date){
				start_date = Date.parse(start_date);
				projects = this._project_list.filter(element=>Date.parse(element.start_date) >= start_date);
				stories = this._story_list.filter(element=>Date.parse(element.date) >= start_date);
			}
		}else if(key == "end"){
			var end_date = value;
			if(end_date){
				end_date = Date.parse(end_date);
				projects = this._project_list.filter(element=>Date.parse(element.end_date) <= end_date);
				stories = this._story_list.filter(element=>Date.parse(element.date) <= end_date);
			}
		}else if(key == "tags"){
			var tag_list = JSON.parse(value);
			for(var i in tag_list){
				var tag = tag_list[i];
				if(tag){
					var current_projects = this._project_list.filter(element=>element.tags.includes(tag));
					var current_stories = this._story_list.filter(element=>element.tags.includes(tag));
					// match
					projects = projects.filter(value=>current_projects.includes(value));
					stories = stories.filter(value=>current_stories.includes(value));
				}else{
					break;
				}
			}
		}

		// update instance dictionary
		this._project_dict[key] = projects;
		this._story_dict[key] = stories;
	}

	update_results(update_list){
		for(var i=0; i<update_list.length;++i){
			var key = update_list[i];
			if(key != "order"){
				this.filter_results(key);
			}else{
				this._order = localStorage.getItem(key)
			}
		}

		// match
		this.project_match = [...this._project_list];
		this.story_match = [...this._story_list];
		for(var i in this._key_list){
			var key = this._key_list[i];
			var key_projects = this._project_dict[key];
			var key_stories = this._story_dict[key];

			this.project_match = this.project_match.filter(value=>key_projects.includes(value));
			this.story_match = this.story_match.filter(value=>key_stories.includes(value));
		}

		// order
		if(this._order=="descending"){
			this.project_match.sort((obA, obB)=>{return new Date(obB.start_date) - new Date(obA.start_date)});
			this.story_match.sort((obA, obB)=>{return new Date(obB.date) - new Date(obA.date)});
		}else{
			this.project_match.sort((obA, obB)=>{return new Date(obA.start_date) - new Date(obB.start_date)});
			this.story_match.sort((obA, obB)=>{return new Date(obA.date) - new Date(obB.date)});
		}
	}
}