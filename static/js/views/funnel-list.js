var toolbar = require('../../templates/toolbar.hbs')
var modelView = require('../../templates/model-view.hbs')
var template = require('../../templates/funnel-list.hbs')
var request = require('superagent-bluebird-promise')
var Promise = require("bluebird");

module.exports.path = '/'
module.exports.run = function(params) {
    'use strict'
    var toolbarEl = document.querySelector('#header-toolbar')
    toolbarEl.innerHTML = toolbar({viewName: 'funnel', funnel: {name: 'All Funnels'}})

    var contentEl = document.querySelector('#content')
    contentEl.innerHTML = modelView()

    var funnels

    request.get('/api/funnel/')
      .then(function(response){
            funnels = response.body.objects
            contentEl.innerHTML = template({funnels: funnels})

            var promises = []
            var i = 0
            for(i; i < funnels.length; i++){
              promises.push(request.get('/api/funnel/' + funnels[i].id + '/insights/'))
            }
            return Promise.all(promises)
      })
      .map(function(response){
          return response.body.data[0]
      })
      .then(function(insights){
          var i = 0
          for(i; i < funnels.length; i++){
            funnels[i].insights = insights[i]
          }
          contentEl.innerHTML = template({funnels: funnels})
      })
      .catch(function(err){
          console.log(err)
      })
}
