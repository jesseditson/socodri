var toolbar = require('../../templates/toolbar.hbs')
var modelView = require('../../templates/model-view.hbs')
var funnelSummary = require('../../templates/funnel-summary.hbs')
var stageList = require('../../templates/stage-list.hbs')
var request = require('superagent-bluebird-promise')
var Promise = require("bluebird");

module.exports.path = '/funnel/:funnel/'
module.exports.run = function(params) {
    'use strict'
    var toolbarEl = document.querySelector('#header-toolbar')
    toolbarEl.innerHTML = toolbar({viewName: 'funnel'})

    var contentEl = document.querySelector('#content')
    contentEl.innerHTML = modelView()

    var cardsEl = document.querySelector('#card-list')

    var funnel
    var stages

    request.get('/api/funnel/' + params.funnel + '/')
      .then(function(response){
          funnel = response.body
          toolbarEl.innerHTML = toolbar({viewName: 'funnel', funnel: funnel})
          return Promise.all([
            request.get('/api/stage/').query({funnel: funnel.id}),
            request.get('/api/funnel/' + funnel.id + '/insights/'),
            request.get('/api/funnel/' + funnel.id + '/insights/').query({stages: true})
          ])
        })
        .spread(function(stage_response, insights_response, stage_insights_response){
            stages = stage_response.body.objects
            funnel.insights = insights_response.body.data[0]
            var stage_insights = stage_insights_response.body.data[0]

            var summaryEl = document.querySelector('#funnel-summary')
            summaryEl.innerHTML = funnelSummary({funnel: funnel})

            var i = 0
            for(i; i < stages.length; i++){
              stages[i].insights = stage_insights[stages[i].number]
            }
            cardsEl.innerHTML = stageList({funnel: funnel, stages: stages})
          })
        .catch(function(err){
          console.log(err)
        })
}
