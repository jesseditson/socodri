from restless import dj
from restless.resources import skip_prepare
from django.db.models import Count
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt
from socodri import authorization, models, preparers


class FunnelResource(dj.DjangoResource):
    preparer = preparers.LaxFieldsPreparer(fields={
        'id': 'id',
        'slug': 'slug',
        'name': 'name',
        'adaccount': 'adaccount.name',
        'stage_count': 'stage_count',
        'action_count': 'action_count',
    })

    def __init__(self, *args, **kwargs):
        super(FunnelResource, self).__init__(*args, **kwargs)

        self.http_methods.update({
            'insights': {
                'GET': 'insights',
            }
        })

    def is_authenticated(self):
        return authorization.is_request_authorized(self.request)

    @classmethod
    def urls(cls, name_prefix=None):
        "Add insights edge and enable slug detail view"
        urlpatterns = super(FunnelResource, cls).urls(name_prefix=name_prefix)
        return urlpatterns + patterns('',
            url(r'^(?P<slug>[\w-]+)/$', cls.as_detail(), name='api_funnel_detail'),
            url(r'^(?P<pk>\d+)/insights/$', cls.as_view('insights'), name='api_funnel_insights'),
            url(r'^(?P<slug>[\w-]+)/insights/$', cls.as_view('insights'), name='api_funnel_insights')
        )

    def list(self):
        return models.Funnel.objects.all().annotate(stage_count=Count('stage'))

    def _get_lookup_filter(self, pk=None, slug=None):
        return pk and {'pk': pk} or {'slug': slug}

    def detail(self, pk=None, slug=None):
        #funnel.insights['groups'] = sorted(campaign_insights, key=lambda x: x.get('cost_per_conversion'), reverse=False)
        return models.Funnel.objects.filter(**self._get_lookup_filter(pk, slug)).annotate(stage_count=Count('stage')).first()

    @skip_prepare
    def insights(self, pk=None, slug=None):
        funnel = models.Funnel.objects.filter(**self._get_lookup_filter(pk, slug)).first()
        """
        fn_map = {
            'audience': insights.get_audience_insights,
            'creative': insights.get_creative_insights,
            'campaign': insights.get_campaign_insights
        }
        _type = self.request.GET.get('type')
        data = _type in fn_map and fn_map[_type](funnel.adaccount.id, *map(lambda x: x.id, funnel.campaigns.all())) or []
        return {
            'data': [d for d in data]
        }
        """
        #data = insights.get_funnel_insights(funnel)
        data = {'spend': 0.00, 'conversions': 0, 'conversion_revenue': 0.00}

        return {
            'data': data
        }


class ActionResource(dj.DjangoResource):
    preparer = preparers.LaxFieldsPreparer(fields={
        'id': 'id',
        'pixel_id': 'pixel_id',
        'pixel_name': 'pixel.name',
        'name': 'name',
        'tag': 'tag'
    })

    def is_authenticated(self):
        return authorization.is_request_authorized(self.request)

    def list(self):
        stage = self.request.GET.get('stage')
        all_actions = models.Action.objects.all()
        return all_actions.filter(stage=stage) if stage else all_actions

    def detail(self, pk):
        return models.Action.objects.get(id=pk)


class StageResource(dj.DjangoResource):
    preparer = preparers.LaxFieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
        'number': 'number',
        'funnel_id': 'funnel_id',
    })

    def is_authenticated(self):
        return authorization.is_request_authorized(self.request)

    def list(self):
        funnel = self.request.GET.get('funnel')
        all_stages = models.Stage.objects.all()
        stages = all_stages.filter(funnel=funnel) if funnel else all_stages
        return stages

    def detail(self, pk):
        return models.Stage.objects.get(pk=pk)
