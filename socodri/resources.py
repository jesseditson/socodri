from restless import dj
from restless.resources import skip_prepare
from django.db.models import Count
from django.conf import settings
from django.conf.urls import patterns, url
from socodri import authorization, models, preparers, insights, utils


class InsightsMixin(object):
    def __init__(self, *args, **kwargs):
        super(InsightsMixin, self).__init__(*args, **kwargs)

        self.http_methods.update({
            'insights': {
                'GET': 'insights',
            }
        })

    @classmethod
    def urls(cls, name_prefix=None):
        "Add insights edge"
        urlpatterns = super(InsightsMixin, cls).urls(name_prefix=name_prefix)
        return urlpatterns + patterns('',
            url(r'^(?P<pk>\d+)/insights/$', cls.as_view('insights'), name=cls.build_url_name('insights', name_prefix)),
            url(r'^(?P<slug>[\w-]+)/insights/$', cls.as_view('insights'), name=cls.build_url_name('insights', name_prefix))
        )

    @skip_prepare
    def insights(self, pk=None, slug=None):
        return {
            'data': {'spend': 0.00, 'conversions': 0, 'conversion_revenue': 0.00}
        }


class GetCurrentUserMixin(object):
    def is_authenticated(self):
        self.request.user = utils.get_current_user(self.request.COOKIES)
        return self.request.user is not None


class AuthorizationMixin(object):
    def is_authorized(self):
        return authorization.is_request_authorized(self.request)

    def get_authorized_queryset(self):
        assert self.model
        return self.model.objects.all().filter(pk__in=settings.WHITELISTED_FUNNELS.get(self.request.user.get('id'), []))


class FunnelResource(GetCurrentUserMixin, AuthorizationMixin, InsightsMixin, dj.DjangoResource):
    name_prefix = 'funnel'
    model = models.Funnel
    preparer = preparers.LaxFieldsPreparer(fields={
        'id': 'id',
        'slug': 'slug',
        'name': 'name',
        'adaccount': 'adaccount.name',
        'stage_count': 'stage_count',
        'action_count': 'action_count',
    })

    @classmethod
    def urls(cls, name_prefix=None):
        "Add slug detail view"
        name_prefix = name_prefix or cls.name_prefix
        urlpatterns = super(FunnelResource, cls).urls(name_prefix=name_prefix)
        return urlpatterns + patterns('',
            url(r'^(?P<slug>[\w-]+)/$', cls.as_detail(), name=cls.build_url_name('insights', name_prefix)),
        )

    def list(self):
        return self.get_authorized_queryset().annotate(stage_count=Count('stage'))

    def _get_lookup_filter(self, pk=None, slug=None):
        return pk and {'pk': pk} or {'slug': slug}

    def detail(self, pk=None, slug=None):
        return self.get_authorized_queryset().filter(**self._get_lookup_filter(pk, slug)).annotate(stage_count=Count('stage')).first()

    @skip_prepare
    def insights(self, pk=None, slug=None):
        funnel = models.Funnel.objects.filter(**self._get_lookup_filter(pk, slug)).first()
        daily = self.request.GET.get('daily', False)
        return {'data': insights.get_funnel_insights(funnel, daily=daily)}


class ActionResource(dj.DjangoResource):
    preparer = preparers.LaxFieldsPreparer(fields={
        'id': 'id',
        'pixel_id': 'pixel_id',
        'pixel_name': 'pixel.name',
        'name': 'name',
        'tag': 'tag'
    })

    def list(self):
        stage = self.request.GET.get('stage')
        all_actions = models.Action.objects.all()
        return all_actions.filter(stage=stage) if stage else all_actions

    def detail(self, pk):
        return models.Action.objects.get(id=pk)


class StageResource(InsightsMixin, dj.DjangoResource):
    preparer = preparers.LaxFieldsPreparer(fields={
        'id': 'id',
        'name': 'name',
        'number': 'number',
        'funnel_id': 'funnel_id',
    })

    def list(self):
        funnel = self.request.GET.get('funnel')
        all_stages = models.Stage.objects.all()
        stages = all_stages.filter(funnel=funnel) if funnel else all_stages
        return stages

    def detail(self, pk):
        return models.Stage.objects.get(pk=pk)
