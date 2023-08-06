# -*- coding: utf-8 -*-

__all__ = ['ExplainerDashboard', 'ExplainerDashboardStandaloneTab',
            'ModelSummaryTab']


import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.io as pio

from .dashboard_tabs.dashboard_methods import *
from .dashboard_tabs.model_summary_tab import *
from .dashboard_tabs.contributions_tab import *
from .dashboard_tabs.shap_dependence_tab import *
from .dashboard_tabs.shap_interactions_tab import *
from .dashboard_tabs.decision_trees_tab import *


class ExplainerDashboard:
    """Constructs a dashboard out of an ExplainerBunch object. You can indicate
    which tabs to include, and pass kwargs to individual tabs.
    """
    def __init__(self, explainer, title='Model Explainer',   
                tabs=None,
                model_summary=True,  
                contributions=True,
                shap_dependence=True,
                shap_interaction=True,
                decision_trees=True,
                plotly_template="none",
                **kwargs):
        """Constructs an ExplainerDashboard.
        
        :param explainer: an ExplainerBunch object
        :param title: Title of the dashboard, defaults to 'Model Explainer'
        :type title: str, optional
        :param model_summary: display model_summary tab or not, defaults to True
        :type model_summary: bool, optional
        :param contributions: display individual contributions tab or not, defaults to True
        :type contributions: bool, optional
        :param shap_dependence: display shap dependence tab or not, defaults to True
        :type shap_dependence: bool, optional
        :param shap_interaction: display tab interaction tab or not. 
        :type shap_interaction: bool, optional
        :param decision_trees: display tab with individual decision tree of random forest, defaults to False
        :type decision_trees: bool, optional
        """
        self.explainer=explainer
        self.title = title
        self.model_summary = model_summary
        self.contributions = contributions
        self.shap_dependence = shap_dependence
        self.shap_interaction = shap_interaction
        self.decision_trees = decision_trees
        self.plotly_template = plotly_template
        self.kwargs = kwargs

        # calculate lazily loaded properties before starting dashboard:
        if shap_dependence or contributions or model_summary:
            _ = explainer.shap_values, explainer.preds, explainer.pred_percentiles
            if explainer.cats is not None:
                _ = explainer.shap_values_cats
            if explainer.is_classifier:
                _ = explainer.pred_probas
        if model_summary:
            _ = explainer.permutation_importances
            if explainer.cats is not None:
                _ = explainer.permutation_importances_cats
        if shap_interaction:
            try:
                _ = explainer.shap_interaction_values
                if explainer.cats is not None:
                    _ = explainer.shap_interaction_values_cats
            except:
                print("Note: calculating shap interaction failed, so turning off interactions tab")
                self.shap_interaction=False
        if decision_trees:
            if hasattr(self.explainer, 'decision_trees'):
                _ = explainer.graphviz_available
                _ = explainer.decision_trees
            else:
                self.decision_trees = False
            
        self.app = dash.Dash(__name__)
        self.app.config['suppress_callback_exceptions']=True
        self.app.css.config.serve_locally = True
        self.app.scripts.config.serve_locally = True
        self.app.title = title
        
        pio.templates.default = self.plotly_template

        # layout
        self.title_and_label_selector = TitleAndLabelSelector(explainer, title=title)
        self.tabs = [] if tabs is None else tabs
        self._insert_tabs()
        assert len(self.tabs) > 0, 'need to pass at least one tab! e.g. model_summary=True'
        
        self.tab_layouts = [
            dcc.Tab(children=tab.layout(), label=tab.title, id=tab.tab_id, value=tab.tab_id) 
                for tab in self.tabs]

        self.app.layout = dbc.Container([
            self.title_and_label_selector.layout(),
            dcc.Tabs(id="tabs", value=self.tabs[0].tab_id, children=self.tab_layouts),
        ], fluid=True)

        #register callbacks
        self.title_and_label_selector.register_callbacks(self.app)
        
        for tab in self.tabs:
            tab.register_callbacks(self.app)

    def _insert_tabs(self):
        if self.model_summary:
            self.tabs.append(ModelSummaryTab(self.explainer, **self.kwargs))
        if self.contributions:
            self.tabs.append(ContributionsTab(self.explainer, **self.kwargs))
        if self.shap_dependence:
            self.tabs.append(ShapDependenceTab(self.explainer, **self.kwargs))
        if self.shap_interaction:
            self.tabs.append(ShapInteractionsTab(self.explainer, **self.kwargs))
        if self.decision_trees:
            assert hasattr(self.explainer, 'decision_trees'), \
                """the explainer object has no shadow_trees property. This tab 
                only works with a RandomForestClassifierBunch or RandomForestRegressionBunch""" 
            self.tabs.append(DecisionTreesTab(self.explainer, **self.kwargs))
        
    def run(self, port=8050, **kwargs):
        """Starts the dashboard using the built-in Flask server on localhost:port
        
        :param port: the port to run the dashboard on, defaults to 8050
        :type port: int, optional
        """
        print(f"Running {self.title} on http://localhost:{port}")
        pio.templates.default = self.plotly_template
        self.app.run_server(port=port, **kwargs)


class ExplainerDashboardStandaloneTab:
    """Constructs a dashboard out of an ExplainerBunch object. You can indicate
    which tabs to include, and pass kwargs to individual tabs.
    """
    def __init__(self, explainer, tab, title='Model Explainer', 
                    plotly_template="none", **kwargs):
        """Constructs an ExplainerDashboard.
        
        :param explainer: an ExplainerBunch object
        :param title: Title of the dashboard, defaults to 'Model Explainer'
        :type title: str, optional
        :param tab: single tab to be run as dashboard
        """
        self.explainer = explainer
        self.title = title

        self.plotly_template = plotly_template
        self.kwargs = kwargs

        self.tab = tab(self.explainer, standalone=True, **self.kwargs)

        self.app = dash.Dash(__name__)
        self.app.config['suppress_callback_exceptions']=True
        self.app.css.config.serve_locally = True
        self.app.scripts.config.serve_locally = True
        self.app.title = title
        
        pio.templates.default = self.plotly_template

        self.app.layout = self.tab.layout()
        self.tab.register_callbacks(self.app)

    def run(self, port=8050, **kwargs):
        """Starts the dashboard using the built-in Flask server on localhost:port
        
        :param port: the port to run the dashboard on, defaults to 8050
        :type port: int, optional
        """
        print(f"Running {self.title} on http://localhost:{port}")
        pio.templates.default = self.plotly_template
        self.app.run_server(port=port, **kwargs)


