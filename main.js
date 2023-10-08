import request from "request";

var options = {
  method: 'GET',
  url: 'https://v3.football.api-sports.io/teams',
  qs: {id: '33'},
  headers: {
    'x-rapidapi-host': 'v3.football.api-sports.io',
    'x-rapidapi-key': 'bf72dccdf2e5eb13abe192baf7c6916c'
  }
};

request(options, function (error, response, body) {
	if (error) throw new Error(error);

	console.log(body);
});
