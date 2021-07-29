from django.conf.urls import url
from technical_indicator import views

urlpatterns = [
    url("future_analysis", views.FutureAnalysis.as_view(), name="future_analysis"),
    url("insider_trading_page", views.InsiderTradingPage.as_view(), name="insider_trading_page"),
    url("save_market_data", views.LoadData.as_view(), name="save_market_data"),
    url("save_chart_data", views.LoadChartData.as_view(), name="save_chart_data"),
    url("display_chart_data", views.DisplayResult.as_view(), name="display_chart_data"),
    url("get_pre_data", views.PreDataStore.as_view(), name="get_pre_data"),
    url("get_new_insider_data", views.PublishNewInsiderTrade.as_view(), name="get_new_insider_data"),
    url(
        "companies_for_long_position",
        views.MarketDataTesting.as_view(),
        name="companies_for_long_position",
    ),
    url(
        "check_future_price_cash_price_relationship",
        views.CheckFuturePriceCashPriceRelationship.as_view(),
        name="check_future_price_cash_price_relationship",
    ),
    # url('market_data', views, name=''),
]
