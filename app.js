const express = require('express')
const app = express()

app.get('/', (req, res) => res.send('Hello, I am the first application!'))
app.listen(3000, ()=>console.log('Server started'))
