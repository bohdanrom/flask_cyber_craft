$( document ).ready(function() {
    $("#submit-button").click(
		function(){
			if($("#github-login-input").val() !== ""){
				sendAjaxForm();
			}
			return false;
		}
	);
function sendAjaxForm() {
	let githubLogin = $("#github-login-input").val()
	let query = `query{
            user(login: "${githubLogin}") {
                name
                repositories(first: 100) {
                    nodes {
                        name
                    }
                }
            }
        }`
    $.ajax({
        url: '/graphql',
        type: "POST",
        dataType: "html",
        data: query,
        success: function(response) {
			if ($(".repos-names").length){
				$(".repos-names").remove()
			}
			let githubName = JSON.parse(response)['github_name']
			let githubRepos = JSON.parse(response)['github_repos']
			if (githubName === null){
				$("#github-name").html("null");
			}
			else{
				$("#github-name").html(githubName);
			}
			for (elem=0; githubRepos.length; elem+=1){
				if (elem === githubRepos.length){
					break
				}
				if ($(".repos-names").length < githubRepos.length){
					$("#repos").append(`<p class="repos-names">${githubRepos[elem]}</p>`);
				}
			}
    	}
 	});
}
});
