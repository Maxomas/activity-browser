# -*- coding: utf-8 -*-
from .panel import Panel, ActivitiesPanel, MethodsPanel
from ..web.webutils import SimpleWebPageWidget
from .. import activity_cache
from ..tabs import CalculationSetupTab
from ...signals import signals
from .... import PACKAGE_DIRECTORY


class LeftPanel(Panel):
    side = "left"

    def __init__(self, *args):
        super(LeftPanel, self).__init__(*args)
        # Tabs
        self.welcome_tab = SimpleWebPageWidget(
            html_file=PACKAGE_DIRECTORY+r'/app/ui/web/startscreen/startscreen.html'
        )
        self.method_panel = MethodsPanel(self)
        self.cs_tab = CalculationSetupTab(self)
        self.act_panel = ActivitiesPanel(self)

        # add tabs
        self.addTab(self.welcome_tab, 'Welcome')
        self.addTab(self.cs_tab, 'LCA Calculations')

        # signals
        signals.activity_tabs_changed.connect(self.update_activity_panel)
        self.currentChanged.connect(self.remove_welcome_tab)
        signals.method_tabs_changed.connect(self.update_method_panel)

    def update_method_panel(self):
        if self.method_panel.tab_dict:
            if self.indexOf(self.method_panel) == -1:
                self.addTab(self.method_panel, 'LCIA CFs')
            self.select_tab(self.method_panel)
        else:
            self.removeTab(self.indexOf(self.method_panel))
            self.setCurrentIndex(0)

    def update_activity_panel(self):
        if len(activity_cache):
            self.addTab(self.act_panel, 'Activities')
            self.select_tab(self.act_panel)
        else:
            self.removeTab(self.indexOf(self.act_panel))
            self.setCurrentIndex(0)

    def remove_welcome_tab(self):
        if self.indexOf(self.welcome_tab) != -1:
            self.removeTab(self.indexOf(self.welcome_tab))
