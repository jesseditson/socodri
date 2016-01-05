var toolbar = require('../../templates/toolbar.hbs')
var modelView = require('../../templates/model-view.hbs')
var funnelSummary = require('../../templates/funnel-summary.hbs')
var card = require('../../templates/card.hbs')
var request = require('superagent-bluebird-promise')
var Promise = require("bluebird");

module.exports.path = '/funnel/:funnel/'
module.exports.run = function(params) {
    'use strict'
    var toolbarEl = document.querySelector('#header-toolbar')
    toolbarEl.innerHTML = toolbar({viewName: 'funnel'})

    var contentEl = document.querySelector('#content')
    contentEl.innerHTML = modelView()

    var funnel

    request.get('/api/funnel/' + params.funnel + '/')
      .then(function(response){
          funnel = response.body
          toolbarEl.innerHTML = toolbar({viewName: 'funnel', funnel: funnel})
          return Promise.all([
            request.get('/api/stage/').query({funnel: funnel.id}),
            request.get('/api/funnel/' + funnel.id + '/insights/')
          ])
        })
        .spread(function(stage_response, insights_response){
            var stages = stage_response.body.objects
            var insights = insights_response.body.data

            var summaryEl = document.querySelector('#funnel-summary')
            summaryEl.innerHTML = funnelSummary({funnel: funnel, insights: insights})

            var i, stage
            for(i = 0; i < stages.length; i++){
                  stage = stages[i]
                //stage.insights = insights.stages[stage.number]
                stage.insights = {}
            }
            var cardsEl = document.querySelector('#card-list')
            cardsEl.innerHTML += card({funnel: funnel, stages: stages, insights: insights})
        })
        .catch(function(err){
            console.log(err)
        })
}
