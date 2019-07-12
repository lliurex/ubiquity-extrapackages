# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-

from ubiquity import misc, plugin, validation
import os
import inspect
import gettext


NAME = 'lliurexExtrapackages'
AFTER = 'console_setup'
BEFORE = 'usersetup'
WEIGHT = 20

gettext.textdomain('ubilliurexextrapackages')
_ = gettext.gettext

class PageKde(plugin.PluginUI):
    plugin_title = 'lliurex/text/breadcrumb_extrapackages'
    plugin_breadcrumb = 'lliurex/text/breadcrumb_extrapackages'
    plugin_prefix = 'lliurex/text'

    def __init__(self, controller, *args, **kwargs):

        import yaml

        config = yaml.load(open('/etc/lliurexinstaller/extrapackages.yaml')) if os.path.exists('/etc/lliurexinstaller/extrapackages.yaml') else {'packages':[]}

        from PyQt5.QtGui import QPixmap, QIcon, QFont
        from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QScrollArea, QGridLayout, QHBoxLayout, QLabel, QSizePolicy, QRadioButton
        from PyQt5.QtCore import Qt
        self.packages_install = []
        self.controller = controller
        self.main_widget = QFrame()
        self.main_widget.setLayout(QVBoxLayout())
        qsa = QScrollArea()
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        widget.layout().setAlignment(Qt.AlignCenter | Qt.AlignTop)
        qsa.setWidget(widget)
        qsa.setWidgetResizable(True)

        label = QLabel()
        self.main_widget.layout().addWidget(label)
        self.main_widget.layout().addWidget(qsa)

        label.text = _("Select extra packages to install")
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        fontlabel = QFont()
        fontlabel.setBold(True)
        fontlabel.setWeight(75)
        fontlabel.setPixelSize(20)
        label.setFont(fontlabel)
        label.setStyleSheet("QLabel{ margin:0px 0px 10px 0px}")

        count = 0
        for app in config['packages']:
            appConfig = config['packages'][app]
            last = False
            if count+1 == len(config['packages']):
                last = True
            widget.layout().addLayout(self.newPackageUI(appConfig), last)
            count+=1

        self.page = qsa
        self.plugin_widgets = self.page


    def createImagePackage(self,config):
        from PyQt5.QtWidgets import QLabel, QSizePolicy
        from PyQt5.QtGui import QIcon
        from PyQt5.QtCore import QSize

        label = QLabel()
        label.setText("")
        label.setScaledContents(True)
        label.setPixmap(QIcon.fromTheme(config['image']).pixmap(40,40))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label.setSizePolicy(sizePolicy)
        label.setMaximumSize(QSize(40, 40))
        label.setObjectName("imagePackage")
        return label


    def createNamePackage(self,config):
        from PyQt5.QtWidgets import QLabel, QSizePolicy
        from PyQt5.QtGui import QFont

        label_3 = QLabel()
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label_3.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        label_3.setFont(font)
        label_3.setObjectName("label_3")
        label_3.setStyleSheet("QLabel{margin-left:5px; }")
        label_3.setText(_(config['name']))
        return label_3


    def createDescriptionPackage(self,config):
        from PyQt5.QtWidgets import QLabel, QSizePolicy

        label_2 = QLabel()
        label_2.setWordWrap(True)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label_2.setSizePolicy(sizePolicy)
        label_2.setObjectName("label_2")
        label_2.setStyleSheet("QLabel{margin-left:5px ; color: #666 }")
        label_2.setText(_(config['description']))
        return label_2

    def createCheckInstallPackage(self,config):
        from PyQt5.QtWidgets import QCheckBox, QSizePolicy
        checkBox = QCheckBox()
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        checkBox.setSizePolicy(sizePolicy)
        checkBox.setObjectName("checkBox")
        checkBox.setChecked(config['checked'])
        checkBox.clicked.connect(lambda: self.modify_package(config['package'],checkBox))
        if config['checked']:
            self.modify_package(config['package'],checkBox)
        checkBox.setText(_("Install"))
        return checkBox

    def newPackageUI(self, config, last=False):
        from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
        vLayout = QVBoxLayout()
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setObjectName("horizontalLayout")
        verticalLayout_3 = QVBoxLayout()
        verticalLayout_3.setObjectName("verticalLayout_3")
        horizontalLayout_2 = QHBoxLayout()
        horizontalLayout_2.setObjectName("horizontalLayout_2")
        verticalLayout_4 = QVBoxLayout()
        verticalLayout_4.setObjectName("verticalLayout_4")
        horizontalLayout_2.addLayout(verticalLayout_4)
        
        image_package = self.createImagePackage(config)
        name_package = self.createNamePackage(config)
        description_package = self.createDescriptionPackage(config)
        install_package = self.createCheckInstallPackage(config)

        horizontalLayout.addWidget(image_package)
        verticalLayout_4.addWidget(name_package)
        verticalLayout_4.addWidget(description_package)
        horizontalLayout_2.addWidget(install_package)

        verticalLayout_3.addLayout(horizontalLayout_2)
        horizontalLayout.addLayout(verticalLayout_3)
        vLayout.addLayout(horizontalLayout)
        if not last:
            verticalLayout_3.addWidget(self.add_line())
        return vLayout

    def add_line(self):
        from PyQt5.QtWidgets import QWidget, QSizePolicy
        line = QWidget()
        line.setFixedHeight(1)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        line.setSizePolicy(sizePolicy)
        line.setStyleSheet("QWidget{background-color: #ccc}")
        line.setObjectName("line")
        return line
    
    def modify_package(self, package_name, checkbox):
        if checkbox.isChecked():
            self.packages_install.append(package_name)
        else:
            self.packages_install.remove(package_name)

class Page(plugin.Plugin):
    @misc.raise_privileges
    def ok_handler(self):
        os.system("mkdir -p /var/lib/ubiquity")
        with open('/var/lib/ubiquity/lliurex-extra-packages','w') as fd:
            for package in self.ui.packages_install:
                fd.write('{package}\n'.format(package=package))
        plugin.Plugin.ok_handler(self)

