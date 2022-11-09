// Create a request variable and assign a new XMLHttpRequest object to it.
var request = new XMLHttpRequest()

// Open a new connection, using the GET request on the URL endpoint
request.open('GET', 'http://localhost:8000/bears/bear_list.json/', true)

request.onload = function () {
  // Begin accessing JSON data here
var data = JSON.parse(this.response)

data.forEach(bear => {
  // Log each movie's title
  console.log(bear.id)
})

}

// Send request
request.send()