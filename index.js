var scarab = module.exports = require('scarab')

var links = require('docker-links').parseLinks(process.env)

var djangoURL = 'http://' + links.django.hostname + ':' + links.django.port
console.log(`Proxying requests to django server at ${djangoURL}`)
scarab.proxy('/', djangoURL)

if (require.main === module) scarab.serve()
