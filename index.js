// This file just starts our proxy when required, and returns an extendable router.
// In most cases, if you're using the scarab-django app, you won't need to edit this file.
var scarab = module.exports = require('scarab-proxy')
if (require.main === module) scarab.serve()
