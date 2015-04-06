<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>My Queue</title>
	<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootswatch/3.3.4/cosmo/bootstrap.min.css">
</head>
<body style="padding-top:70px;">
	<nav class="navbar navbar-default navbar-fixed-top">
		<div class="container-fluid">
			<div class="navbar-header">
				<a href="#" class="navbar-brand">Project Queue of {{username}}</a>
			</div>
			<p class="navbar-text"><span class="badge">{{number_projects}}</span></p>
			<button class="btn btn-default">Pick Another Project</button>
		</div>
	</nav>
	<div class="col-md-6 col-md-offset-3 text-center">
		<div class="lead">
			<h1><a href="{{pattern_link}}" target="_blank">{{project['short_pattern_name']}}</a></h1>
			<p>by {{project['pattern_author_name']}}</p>
			<p><i class="glyphicon glyphicon-time"></i> {{date_added}}</p>
		</div>
		<div>
			<img src="{{project['best_photo']['small_url']}}" />
		</div>
	</div>
<div class="col-md-6 col-md-offset-3">
<p>My Friends</p>
<ul class="list-inline">
% for friend in friends['friendships']:
<li><a href="/myqueue/{{friend['friend_username']}}">{{friend['friend_username']}}</a></li>
% end
</ul>
</div>
</body>
</html>
