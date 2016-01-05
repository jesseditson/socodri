from facebookads.objects import AdAccount, Insights

def get_funnel_attr_window(funnel):
    return filter(lambda x: x, [
        getattr(Insights.ActionAttributionWindow, funnel.view_window, None),
        getattr(Insights.ActionAttributionWindow, funnel.click_window, None)
    ])

def aggregate_conversion_data(funnel, data):
    val = {'conversions': 0, 'conversion_revenue': 0.00}

    val['spend'] = data['spend']
    val['date_start'] = data['date_start']
    val['date_stop'] = data['date_stop']

    conversion_action_prefix = 'offsite_conversion.'
    funnel_attr_window = get_funnel_attr_window(funnel)
    for action in filter(lambda x: conversion_action_prefix in x[Insights.ActionBreakdown.action_type], data['actions']):
        pixel_id = long(action[Insights.ActionBreakdown.action_target_id])
        prefix, tag = action[Insights.ActionBreakdown.action_type].split(conversion_action_prefix)
        for stage in funnel.stage_set.filter(actions__pixel__id=pixel_id, actions__tag=tag):
            conversions = sum(map(lambda x: action.get(x, 0), funnel_attr_window))
            val['conversions'] += conversions

    for action_value in filter(lambda x: conversion_action_prefix in x[Insights.ActionBreakdown.action_type], data['action_values']):
        pixel_id = long(action_value[Insights.ActionBreakdown.action_target_id])
        prefix, tag = action_value[Insights.ActionBreakdown.action_type].split(conversion_action_prefix)
        for stage in funnel.stage_set.filter(actions__pixel__id=pixel_id, actions__tag=tag):
            conversion_revenue = sum(map(lambda x: action_value.get(x, 0.0), funnel_attr_window))
            val['conversion_revenue'] += conversion_revenue
    return val


def get_funnel_insights(funnel, daily=False):
    assert funnel
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
        'action_attribution_windows': get_funnel_attr_window(funnel),
        'filtering': [
            {
                'field': Insights.Field.impressions,
                'operator': Insights.Operator.greater_than_or_equal.upper(),
                'value': 0
            },
            {
                'field': 'campaign.id',
                'operator': Insights.Operator.in_.upper(),
                'value': tuple(funnel.campaigns.all().values_list('id', flat=True))
            }
        ]
    }
    account = AdAccount('act_%s' % funnel.adaccount.id)
    return [aggregate_conversion_data(funnel, data) for data in account.get_insights(params=params)]
