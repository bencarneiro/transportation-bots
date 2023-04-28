"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from views.views import spending_by_budget,\
spending_by_category,\
spending_by_mode,\
spending_by_mode_type,\
opexp_by_service,\
spending_by_budget,\
upt,\
pmt,\
vrm,\
vrh,\
drm,\
voms,\
upt_by_mode_type,\
pmt_by_mode_type,\
vrm_by_mode_type,\
vrh_by_mode_type,\
drm_by_mode_type,\
voms_by_mode_type,\
upt_by_service,\
pmt_by_service,\
vrm_by_service,\
vrh_by_service,\
drm_by_service,\
voms_by_service,\
upt_by_mode,\
pmt_by_mode,\
vrm_by_mode,\
vrh_by_mode,\
drm_by_mode,\
voms_by_mode,\
cost_per_upt,\
cost_per_pmt,\
frr,\
cost_per_vrh,\
cost_per_vrm,\
cost_per_vrh,\
vrm_per_vrh,\
upt_per_vrh,\
upt_per_vrm,\
pmt_per_vrh,\
pmt_per_vrm,\
cost_per_upt_by_mode_type,\
cost_per_pmt_by_mode_type,\
frr_by_mode_type,\
cost_per_vrh_by_mode_type,\
cost_per_vrm_by_mode_type,\
cost_per_vrh_by_mode_type,\
vrm_per_vrh_by_mode_type,\
upt_per_vrh_by_mode_type,\
upt_per_vrm_by_mode_type,\
pmt_per_vrh_by_mode_type,\
pmt_per_vrm_by_mode_type,\
cost_per_upt_by_mode,\
cost_per_pmt_by_mode,\
frr_by_mode,\
cost_per_vrh_by_mode,\
cost_per_vrm_by_mode,\
cost_per_vrh_by_mode,\
vrm_per_vrh_by_mode,\
upt_per_vrh_by_mode,\
upt_per_vrm_by_mode,\
pmt_per_vrh_by_mode,\
pmt_per_vrm_by_mode,\
cost_per_upt_by_service,\
cost_per_pmt_by_service,\
frr_by_service,\
cost_per_vrh_by_service,\
cost_per_vrm_by_service,\
cost_per_vrh_by_service,\
vrm_per_vrh_by_service,\
upt_per_vrh_by_service,\
upt_per_vrm_by_service,\
pmt_per_vrh_by_service,\
pmt_per_vrm_by_service,\
get_uzas,\
get_states,\
get_agencies

urlpatterns = [
    path('admin/', admin.site.urls),
    path('spending_by_budget/', spending_by_budget, name='spending_by_budget'),
    path('spending_by_category/', spending_by_category, name='spending_by_category'),
    path('spending_by_mode_type/', spending_by_mode_type, name='spending_by_mode_type'),
    path('spending_by_mode/', spending_by_mode, name='spending_by_mode'),
    path('opexp_by_service/', opexp_by_service, name='opexp_by_service'),
    path('upt/', upt, name='upt'),
    path('pmt/', pmt, name='pmt'),
    path('vrm/', vrm, name='vrm'),
    path('vrh/', vrh, name='vrh'),
    path('drm/', drm, name='drm'),
    path('voms/', voms, name='voms'),
    path('upt_by_mode_type/', upt_by_mode_type, name='upt_by_mode_type'),
    path('pmt_by_mode_type/', pmt_by_mode_type, name='pmt_by_mode_type'),
    path('vrm_by_mode_type/', vrm_by_mode_type, name='vrm_by_mode_type'),
    path('vrh_by_mode_type/', vrh_by_mode_type, name='vrh_by_mode_type'),
    path('drm_by_mode_type/', drm_by_mode_type, name='drm_by_mode_type'),
    path('voms_by_mode_type/', voms_by_mode_type, name='voms_by_mode_type'),
    path('upt_by_service/', upt_by_service, name='upt_by_service'),
    path('pmt_by_service/', pmt_by_service, name='pmt_by_service'),
    path('vrm_by_service/', vrm_by_service, name='vrm_by_service'),
    path('vrh_by_service/', vrh_by_service, name='vrh_by_service'),
    path('drm_by_service/', drm_by_service, name='drm_by_service'),
    path('voms_by_service/', voms_by_service, name='voms_by_service'),
    path('upt_by_mode/', upt_by_mode, name='upt_by_mode'),
    path('pmt_by_mode/', pmt_by_mode, name='pmt_by_mode'),
    path('vrm_by_mode/', vrm_by_mode, name='vrm_by_mode'),
    path('vrh_by_mode/', vrh_by_mode, name='vrh_by_mode'),
    path('drm_by_mode/', drm_by_mode, name='drm_by_mode'),
    path('voms_by_mode/', voms_by_mode, name='voms_by_mode'),
    path('cost_per_upt/', cost_per_upt, name='cost_per_upt'),
    path('cost_per_pmt/', cost_per_pmt, name='cost_per_pmt'),
    path('frr/', frr, name='frr'),
    path('cost_per_vrh/', cost_per_vrh, name='cost_per_vrh'),
    path('cost_per_vrm/', cost_per_vrm, name='cost_per_vrm'),
    path('cost_per_vrh/', cost_per_vrh, name='cost_per_vrh'),
    path('vrm_per_vrh/', vrm_per_vrh, name='vrm_per_vrh'),
    path('upt_per_vrh/', upt_per_vrh, name='upt_per_vrh'),
    path('upt_per_vrm/', upt_per_vrm, name='upt_per_vrm'),
    path('pmt_per_vrh/', pmt_per_vrh, name='pmt_per_vrh'),
    path('pmt_per_vrm/', pmt_per_vrm, name='pmt_per_vrm'),
    path('cost_per_upt_by_mode_type/', cost_per_upt_by_mode_type, name='cost_per_upt_by_mode_type'),
    path('cost_per_pmt_by_mode_type/', cost_per_pmt_by_mode_type, name='cost_per_pmt_by_mode_type'),
    path('frr_by_mode_type/', frr_by_mode_type, name='frr_by_mode_type'),
    path('cost_per_vrh_by_mode_type/', cost_per_vrh_by_mode_type, name='cost_per_vrh_by_mode_type'),
    path('cost_per_vrm_by_mode_type/', cost_per_vrm_by_mode_type, name='cost_per_vrm_by_mode_type'),
    path('cost_per_vrh_by_mode_type/', cost_per_vrh_by_mode_type, name='cost_per_vrh_by_mode_type'),
    path('vrm_per_vrh_by_mode_type/', vrm_per_vrh_by_mode_type, name='vrm_per_vrh_by_mode_type'),
    path('upt_per_vrh_by_mode_type/', upt_per_vrh_by_mode_type, name='upt_per_vrh_by_mode_type'),
    path('upt_per_vrm_by_mode_type/', upt_per_vrm_by_mode_type, name='upt_per_vrm_by_mode_type'),
    path('pmt_per_vrh_by_mode_type/', pmt_per_vrh_by_mode_type, name='pmt_per_vrh_by_mode_type'),
    path('pmt_per_vrm_by_mode_type/', pmt_per_vrm_by_mode_type, name='pmt_per_vrm_by_mode_type'),
    path('cost_per_upt_by_mode/', cost_per_upt_by_mode, name='cost_per_upt_by_mode'),
    path('cost_per_pmt_by_mode/', cost_per_pmt_by_mode, name='cost_per_pmt_by_mode'),
    path('frr_by_mode/', frr_by_mode, name='frr_by_mode'),
    path('cost_per_vrh_by_mode/', cost_per_vrh_by_mode, name='cost_per_vrh_by_mode'),
    path('cost_per_vrm_by_mode/', cost_per_vrm_by_mode, name='cost_per_vrm_by_mode'),
    path('cost_per_vrh_by_mode/', cost_per_vrh_by_mode, name='cost_per_vrh_by_mode'),
    path('vrm_per_vrh_by_mode/', vrm_per_vrh_by_mode, name='vrm_per_vrh_by_mode'),
    path('upt_per_vrh_by_mode/', upt_per_vrh_by_mode, name='upt_per_vrh_by_mode'),
    path('upt_per_vrm_by_mode/', upt_per_vrm_by_mode, name='upt_per_vrm_by_mode'),
    path('pmt_per_vrh_by_mode/', pmt_per_vrh_by_mode, name='pmt_per_vrh_by_mode'),
    path('pmt_per_vrm_by_mode/', pmt_per_vrm_by_mode, name='pmt_per_vrm_by_mode'),
    path('cost_per_upt_by_service/', cost_per_upt_by_service, name='cost_per_upt_by_service'),
    path('cost_per_pmt_by_service/', cost_per_pmt_by_service, name='cost_per_pmt_by_service'),
    path('frr_by_service/', frr_by_service, name='frr_by_service'),
    path('cost_per_vrh_by_service/', cost_per_vrh_by_service, name='cost_per_vrh_by_service'),
    path('cost_per_vrm_by_service/', cost_per_vrm_by_service, name='cost_per_vrm_by_service'),
    path('cost_per_vrh_by_service/', cost_per_vrh_by_service, name='cost_per_vrh_by_service'),
    path('vrm_per_vrh_by_service/', vrm_per_vrh_by_service, name='vrm_per_vrh_by_service'),
    path('upt_per_vrh_by_service/', upt_per_vrh_by_service, name='upt_per_vrh_by_service'),
    path('upt_per_vrm_by_service/', upt_per_vrm_by_service, name='upt_per_vrm_by_service'),
    path('pmt_per_vrh_by_service/', pmt_per_vrh_by_service, name='pmt_per_vrh_by_service'),
    path('pmt_per_vrm_by_service/', pmt_per_vrm_by_service, name='pmt_per_vrm_by_service'),
    path('get_uzas/', get_uzas, name='get_uzas'),
    path('get_states/', get_states, name="get_states"),
    path('get_agencies/', get_agencies, name="get_agencies")
]
