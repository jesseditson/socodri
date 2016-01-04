var toolbar = require('../templates/toolbar.hbs')
var funnelCard = require('../templates/funnel-list.hbs')
var request = require('superagent-bluebird-promise')

module.exports.path = '/'
module.exports.run = function(params) {
    'use strict'
    var toolbarEl = document.querySelector('#header-toolbar')
    toolbarEl.innerHTML = toolbar({viewName: 'funnel', funnel: {name: 'All Funnels'}})

    var contentEl = document.querySelector('#content')
    contentEl.innerHTML = modelView()

    request.get('/api/funnel/')
      .then(function(response){
            var funnels = response.body.objects
            console.log(funnels)
            var cardsEl = document.querySelector('#card-list')
            cardsEl.innerHTML += funnelCard({funnels: funnels})
      })
      .catch(function(err){
          console.log(err)
      })
}
