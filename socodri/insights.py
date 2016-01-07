from copy import copy
from facebookads.objects import AdAccount, Insights


def get_funnel_attr_window(funnel):
    return filter(lambda x: x, [
        getattr(Insights.ActionAttributionWindow, funnel.view_window, None),
        getattr(Insights.ActionAttributionWindow, funnel.click_window, None)
    ])


def get_funnel_attr_multipliers(funnel):
    return filter(lambda x: x, [
        funnel.view_multiplier if funnel.view_window else None,
        funnel.click_multiplier if funnel.click_window else None
    ])


def aggregate_funnel_data(funnel, data):
    val = {'conversions': 0, 'conversion_revenue': 0.00}

    val['spend'] = data['spend']
    val['date_start'] = data['date_start']
    val['date_stop'] = data['date_stop']

    conversion_action_prefix = 'offsite_conversion.'
    funnel_attr_window = get_funnel_attr_window(funnel)
    funnel_attr_multipliers = get_funnel_attr_multipliers(funnel)
    for action in filter(lambda x: conversion_action_prefix in x[Insights.ActionBreakdown.action_type], data['actions']):
        pixel_id = long(action[Insights.ActionBreakdown.action_target_id])
        prefix, tag = action[Insights.ActionBreakdown.action_type].split(conversion_action_prefix)
        conversions = sum(
            map(lambda (window, multiplier): action.get(window, 0) * multiplier,
                zip(funnel_attr_window, funnel_attr_multipliers)
               )
        )
        val['conversions'] += conversions

    for action_value in filter(lambda x: conversion_action_prefix in x[Insights.ActionBreakdown.action_type], data['action_values']):
        pixel_id = long(action_value[Insights.ActionBreakdown.action_target_id])
        prefix, tag = action_value[Insights.ActionBreakdown.action_type].split(conversion_action_prefix)
        conversion_revenue = sum(
            map(lambda (window, multiplier): action_value.get(window, 0.0) * multiplier,
                zip(funnel_attr_window, funnel_attr_multipliers)
               )
        )
        val['conversion_revenue'] += conversion_revenue
    return val


def aggregate_stage_data(funnel, data):
    stages = {}
    val = {'conversions': 0, 'conversion_revenue': 0.00}
    val['spend'] = data['spend']
    val['date_start'] = data['date_start']
    val['date_stop'] = data['date_stop']

    for stage_num in funnel.stage_set.values_list('number', flat=True):
        stages[stage_num] = copy(val)

    conversion_action_prefix = 'offsite_conversion.'
    funnel_attr_window = get_funnel_attr_window(funnel)
    funnel_attr_multipliers = get_funnel_attr_multipliers(funnel)
    for action in filter(lambda x: conversion_action_prefix in x[Insights.ActionBreakdown.action_type], data['actions']):
        pixel_id = long(action[Insights.ActionBreakdown.action_target_id])
        prefix, tag = action[Insights.ActionBreakdown.action_type].split(conversion_action_prefix)
        for stage in funnel.stage_set.filter(actions__pixel__id=pixel_id, actions__tag=tag):
            conversions = sum(
                map(lambda (window, multiplier): action.get(window, 0) * multiplier,
                    zip(funnel_attr_window, funnel_attr_multipliers)
                   )
            )
            stages[stage.number]['conversions'] += conversions

    for action_value in filter(lambda x: conversion_action_prefix in x[Insights.ActionBreakdown.action_type], data['action_values']):
        pixel_id = long(action_value[Insights.ActionBreakdown.action_target_id])
        prefix, tag = action_value[Insights.ActionBreakdown.action_type].split(conversion_action_prefix)
        for stage in funnel.stage_set.filter(actions__pixel__id=pixel_id, actions__tag=tag):
            conversion_revenue = sum(
                map(lambda (window, multiplier): action_value.get(window, 0.0) * multiplier,
                    zip(funnel_attr_window, funnel_attr_multipliers)
                   )
            )
            stages[stage.number]['conversion_revenue'] += conversion_revenue
    return stages


def get_facebook_insights(adaccount, attr_window, campaigns, daily=False):
    params = {
        'time_increment': 1 if daily else Insights.Increment.all_days,
        'fields': [
            Insights.Field.spend,
            Insights.Field.actions,
            Insights.Field.action_values,
        ],
        'action_breakdowns': [
            Insights.ActionBreakdown.action_destination,
            Insights.ActionBreakdown.action_type,
            Insights.ActionBreakdown.action_target_id
        ],
        'action_attribution_windows': attr_window,
        'filtering': [
            {
                'field': Insights.Field.impressions,
                'operator': Insights.Operator.greater_than_or_equal.upper(),
                'value': 0
            },
            {
                'field': 'campaign.id',
                'operator': Insights.Operator.in_.upper(),
                'value': campaigns
            }
        ]
    }
    account = AdAccount('act_%s' % adaccount.id)
    return account.get_insights(params=params)


def get_funnel_insights(funnel):
    assert funnel
    return [
        aggregate_funnel_data(funnel, data)
        for data in get_facebook_insights(
            funnel.adaccount,
            get_funnel_attr_window(funnel),
            tuple(funnel.campaigns.all().values_list('id', flat=True))
        )
    ]


def get_stage_insights(funnel):
    assert funnel
    return [
        aggregate_stage_data(funnel, data)
        for data in get_facebook_insights(
            funnel.adaccount,
            get_funnel_attr_window(funnel),
            tuple(funnel.campaigns.all().values_list('id', flat=True))
        )
    ]
