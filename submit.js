document.getElementById('submit').addEventListener('click', submitHandler)

function submitHandler() {
    const filePath = document.getElementById('file').files[0].path;
    const formData = new FormData()
    formData.append('file', file)
    
    fetch('http://localhost:5000/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ filePath })
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById('response').innerHTML = data.status
    })
}
