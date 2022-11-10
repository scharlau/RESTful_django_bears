const app = document.getElementById('root')

const container = document.createElement('div')
container.setAttribute('class', 'container')

app.appendChild(container)

// Create a request variable and assign a new XMLHttpRequest object to it.
var request = new XMLHttpRequest()

// Open a new connection, using the GET request on the URL endpoint
request.open('GET', 'http://localhost:8000/?format=json', true)

request.onload = function () {
  // Begin accessing JSON data here
var data = JSON.parse(this.response)
if (request.status >= 200 && request.status < 400) {
    data.forEach(bear => {
      const card = document.createElement('div')
      card.setAttribute('class', 'card')

      const h2 = document.createElement('h2')
      h2.textContent = bear.bearID

      const p = document.createElement('p')
      bear.id = bear.id
      p.textContent = `This is a ${ bear.age_class} aged bear 
      ${bear.bearID}, a ${ bear.sex } bear, who has has an tag in its' ${bear.ear_applied } ear, 
      with ${bear.pTT_ID } device, and was
      tagged at ${ bear.capture_lat } and ${ bear.capture_long }`

      container.appendChild(card)
      card.appendChild(h2)
      card.appendChild(p)
    })
  } else {
    const errorMessage = document.createElement('marquee')
    errorMessage.textContent = `Gah, it's not working!`
    app.appendChild(errorMessage)
  }
}

// Send request
request.send()