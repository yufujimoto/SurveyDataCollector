# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yufujimoto/git/SurveyDataCollector/ui/configuration.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_configurationDialog(object):
    def setupUi(self, configurationDialog):
        configurationDialog.setObjectName("configurationDialog")
        configurationDialog.resize(800, 600)
        configurationDialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.lay_v_entire = QtWidgets.QVBoxLayout(configurationDialog)
        self.lay_v_entire.setObjectName("lay_v_entire")
        self.frm_conf_main = QtWidgets.QFrame(configurationDialog)
        self.frm_conf_main.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frm_conf_main.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frm_conf_main.setLineWidth(0)
        self.frm_conf_main.setObjectName("frm_conf_main")
        self.lay_v_main = QtWidgets.QVBoxLayout(self.frm_conf_main)
        self.lay_v_main.setObjectName("lay_v_main")
        self.tab_conf_main = QtWidgets.QTabWidget(self.frm_conf_main)
        self.tab_conf_main.setObjectName("tab_conf_main")
        self.tab_general = QtWidgets.QWidget()
        self.tab_general.setObjectName("tab_general")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_general)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gbx_general = QtWidgets.QGroupBox(self.tab_general)
        self.gbx_general.setObjectName("gbx_general")
        self.lay_v_theme = QtWidgets.QVBoxLayout(self.gbx_general)
        self.lay_v_theme.setSpacing(10)
        self.lay_v_theme.setObjectName("lay_v_theme")
        self.lay_h_thm_lang = QtWidgets.QHBoxLayout()
        self.lay_h_thm_lang.setObjectName("lay_h_thm_lang")
        self.lbl_thm_lang = QtWidgets.QLabel(self.gbx_general)
        self.lbl_thm_lang.setMinimumSize(QtCore.QSize(150, 30))
        self.lbl_thm_lang.setMaximumSize(QtCore.QSize(150, 30))
        self.lbl_thm_lang.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_thm_lang.setObjectName("lbl_thm_lang")
        self.lay_h_thm_lang.addWidget(self.lbl_thm_lang)
        self.cbx_thm_lang = QtWidgets.QComboBox(self.gbx_general)
        self.cbx_thm_lang.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbx_thm_lang.setObjectName("cbx_thm_lang")
        self.cbx_thm_lang.addItem("")
        self.cbx_thm_lang.addItem("")
        self.lay_h_thm_lang.addWidget(self.cbx_thm_lang)
        self.lay_v_theme.addLayout(self.lay_h_thm_lang)
        self.lay_h_thm_skin = QtWidgets.QHBoxLayout()
        self.lay_h_thm_skin.setObjectName("lay_h_thm_skin")
        self.lbl_thm_skin = QtWidgets.QLabel(self.gbx_general)
        self.lbl_thm_skin.setMinimumSize(QtCore.QSize(150, 30))
        self.lbl_thm_skin.setMaximumSize(QtCore.QSize(150, 30))
        self.lbl_thm_skin.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_thm_skin.setObjectName("lbl_thm_skin")
        self.lay_h_thm_skin.addWidget(self.lbl_thm_skin)
        self.cbx_skin = QtWidgets.QComboBox(self.gbx_general)
        self.cbx_skin.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbx_skin.setObjectName("cbx_skin")
        self.cbx_skin.addItem("")
        self.cbx_skin.addItem("")
        self.lay_h_thm_skin.addWidget(self.cbx_skin)
        self.lay_v_theme.addLayout(self.lay_h_thm_skin)
        self.verticalLayout.addWidget(self.gbx_general)
        self.gbx_tool = QtWidgets.QGroupBox(self.tab_general)
        self.gbx_tool.setObjectName("gbx_tool")
        self.lay_v_tools = QtWidgets.QVBoxLayout(self.gbx_tool)
        self.lay_v_tools.setSpacing(10)
        self.lay_v_tools.setObjectName("lay_v_tools")
        self.lay_h_tool_awb = QtWidgets.QHBoxLayout()
        self.lay_h_tool_awb.setObjectName("lay_h_tool_awb")
        self.lbl_tool_awb = QtWidgets.QLabel(self.gbx_tool)
        self.lbl_tool_awb.setMinimumSize(QtCore.QSize(150, 30))
        self.lbl_tool_awb.setMaximumSize(QtCore.QSize(150, 30))
        self.lbl_tool_awb.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_tool_awb.setObjectName("lbl_tool_awb")
        self.lay_h_tool_awb.addWidget(self.lbl_tool_awb)
        self.cbx_tool_awb = QtWidgets.QComboBox(self.gbx_tool)
        self.cbx_tool_awb.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbx_tool_awb.setObjectName("cbx_tool_awb")
        self.cbx_tool_awb.addItem("")
        self.cbx_tool_awb.addItem("")
        self.cbx_tool_awb.addItem("")
        self.cbx_tool_awb.addItem("")
        self.cbx_tool_awb.addItem("")
        self.cbx_tool_awb.addItem("")
        self.cbx_tool_awb.addItem("")
        self.cbx_tool_awb.addItem("")
        self.cbx_tool_awb.addItem("")
        self.lay_h_tool_awb.addWidget(self.cbx_tool_awb)
        self.lay_v_tools.addLayout(self.lay_h_tool_awb)
        self.lay_h_tool_psp = QtWidgets.QHBoxLayout()
        self.lay_h_tool_psp.setObjectName("lay_h_tool_psp")
        self.lbl_tool_psp = QtWidgets.QLabel(self.gbx_tool)
        self.lbl_tool_psp.setMinimumSize(QtCore.QSize(150, 30))
        self.lbl_tool_psp.setMaximumSize(QtCore.QSize(150, 30))
        self.lbl_tool_psp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_tool_psp.setObjectName("lbl_tool_psp")
        self.lay_h_tool_psp.addWidget(self.lbl_tool_psp)
        self.cbx_tool_psp = QtWidgets.QComboBox(self.gbx_tool)
        self.cbx_tool_psp.setMaximumSize(QtCore.QSize(16777215, 30))
        self.cbx_tool_psp.setObjectName("cbx_tool_psp")
        self.cbx_tool_psp.addItem("")
        self.cbx_tool_psp.addItem("")
        self.cbx_tool_psp.addItem("")
        self.lay_h_tool_psp.addWidget(self.cbx_tool_psp)
        self.lay_v_tools.addLayout(self.lay_h_tool_psp)
        self.verticalLayout.addWidget(self.gbx_tool)
        self.grp_textedit = QtWidgets.QGroupBox(self.tab_general)
        self.grp_textedit.setObjectName("grp_textedit")
        self.lay_v_defapps = QtWidgets.QVBoxLayout(self.grp_textedit)
        self.lay_v_defapps.setSpacing(10)
        self.lay_v_defapps.setObjectName("lay_v_defapps")
        self.lay_h_textedit = QtWidgets.QHBoxLayout()
        self.lay_h_textedit.setObjectName("lay_h_textedit")
        self.lbl_exe_textedit = QtWidgets.QLabel(self.grp_textedit)
        self.lbl_exe_textedit.setMinimumSize(QtCore.QSize(150, 30))
        self.lbl_exe_textedit.setMaximumSize(QtCore.QSize(150, 30))
        self.lbl_exe_textedit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_exe_textedit.setObjectName("lbl_exe_textedit")
        self.lay_h_textedit.addWidget(self.lbl_exe_textedit)
        self.tbx_exe_textedit = QtWidgets.QLineEdit(self.grp_textedit)
        self.tbx_exe_textedit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tbx_exe_textedit.setObjectName("tbx_exe_textedit")
        self.lay_h_textedit.addWidget(self.tbx_exe_textedit)
        self.lay_v_defapps.addLayout(self.lay_h_textedit)
        self.verticalLayout.addWidget(self.grp_textedit)
        self.grp_net_proxy = QtWidgets.QGroupBox(self.tab_general)
        self.grp_net_proxy.setObjectName("grp_net_proxy")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.grp_net_proxy)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.rbtn_no_proxy = QtWidgets.QCheckBox(self.grp_net_proxy)
        self.rbtn_no_proxy.setObjectName("rbtn_no_proxy")
        self.horizontalLayout.addWidget(self.rbtn_no_proxy)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout()
        self.verticalLayout_13.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rbtn_proxy = QtWidgets.QCheckBox(self.grp_net_proxy)
        self.rbtn_proxy.setObjectName("rbtn_proxy")
        self.horizontalLayout_2.addWidget(self.rbtn_proxy)
        self.txt_proxy = QtWidgets.QLineEdit(self.grp_net_proxy)
        self.txt_proxy.setMaximumSize(QtCore.QSize(16777215, 30))
        self.txt_proxy.setObjectName("txt_proxy")
        self.horizontalLayout_2.addWidget(self.txt_proxy)
        self.verticalLayout_13.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout_13)
        self.verticalLayout.addWidget(self.grp_net_proxy)
        self.tab_conf_main.addTab(self.tab_general, "")
        self.tab_camera = QtWidgets.QWidget()
        self.tab_camera.setObjectName("tab_camera")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.tab_camera)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.frm_cam_list = QtWidgets.QFrame(self.tab_camera)
        self.frm_cam_list.setMinimumSize(QtCore.QSize(350, 0))
        self.frm_cam_list.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frm_cam_list.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_cam_list.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_cam_list.setObjectName("frm_cam_list")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frm_cam_list)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.lbl_cur_cam = QtWidgets.QLabel(self.frm_cam_list)
        self.lbl_cur_cam.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cur_cam.setMaximumSize(QtCore.QSize(16777214, 16777215))
        self.lbl_cur_cam.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lbl_cur_cam.setObjectName("lbl_cur_cam")
        self.verticalLayout_9.addWidget(self.lbl_cur_cam)
        self.lbl_cur_cam_nam = QtWidgets.QLabel(self.frm_cam_list)
        self.lbl_cur_cam_nam.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cur_cam_nam.setIndent(0)
        self.lbl_cur_cam_nam.setObjectName("lbl_cur_cam_nam")
        self.verticalLayout_9.addWidget(self.lbl_cur_cam_nam)
        self.tre_cam = QtWidgets.QTreeWidget(self.frm_cam_list)
        self.tre_cam.setObjectName("tre_cam")
        self.verticalLayout_9.addWidget(self.tre_cam)
        self.btn_cam_conn = QtWidgets.QPushButton(self.frm_cam_list)
        self.btn_cam_conn.setObjectName("btn_cam_conn")
        self.verticalLayout_9.addWidget(self.btn_cam_conn)
        self.horizontalLayout_8.addWidget(self.frm_cam_list)
        self.frm_cam_param = QtWidgets.QFrame(self.tab_camera)
        self.frm_cam_param.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_cam_param.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_cam_param.setObjectName("frm_cam_param")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frm_cam_param)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.lay_h_cam_size = QtWidgets.QHBoxLayout()
        self.lay_h_cam_size.setObjectName("lay_h_cam_size")
        self.lbl_cam_size = QtWidgets.QLabel(self.frm_cam_param)
        self.lbl_cam_size.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cam_size.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lbl_cam_size.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cam_size.setObjectName("lbl_cam_size")
        self.lay_h_cam_size.addWidget(self.lbl_cam_size)
        self.cbx_cam_size = QtWidgets.QComboBox(self.frm_cam_param)
        self.cbx_cam_size.setMaximumSize(QtCore.QSize(180, 16777215))
        self.cbx_cam_size.setObjectName("cbx_cam_size")
        self.lay_h_cam_size.addWidget(self.cbx_cam_size)
        self.verticalLayout_8.addLayout(self.lay_h_cam_size)
        self.lay_h_cam_iso = QtWidgets.QHBoxLayout()
        self.lay_h_cam_iso.setObjectName("lay_h_cam_iso")
        self.lbl_cam_iso = QtWidgets.QLabel(self.frm_cam_param)
        self.lbl_cam_iso.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cam_iso.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lbl_cam_iso.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cam_iso.setObjectName("lbl_cam_iso")
        self.lay_h_cam_iso.addWidget(self.lbl_cam_iso)
        self.cbx_cam_iso = QtWidgets.QComboBox(self.frm_cam_param)
        self.cbx_cam_iso.setMaximumSize(QtCore.QSize(180, 16777215))
        self.cbx_cam_iso.setObjectName("cbx_cam_iso")
        self.lay_h_cam_iso.addWidget(self.cbx_cam_iso)
        self.verticalLayout_8.addLayout(self.lay_h_cam_iso)
        self.lay_h_cam_wht = QtWidgets.QHBoxLayout()
        self.lay_h_cam_wht.setObjectName("lay_h_cam_wht")
        self.lbl_cam_wht = QtWidgets.QLabel(self.frm_cam_param)
        self.lbl_cam_wht.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cam_wht.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lbl_cam_wht.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cam_wht.setObjectName("lbl_cam_wht")
        self.lay_h_cam_wht.addWidget(self.lbl_cam_wht)
        self.cbx_cam_wht = QtWidgets.QComboBox(self.frm_cam_param)
        self.cbx_cam_wht.setMaximumSize(QtCore.QSize(180, 16777215))
        self.cbx_cam_wht.setObjectName("cbx_cam_wht")
        self.lay_h_cam_wht.addWidget(self.cbx_cam_wht)
        self.verticalLayout_8.addLayout(self.lay_h_cam_wht)
        self.lay_h_cam_exp = QtWidgets.QHBoxLayout()
        self.lay_h_cam_exp.setObjectName("lay_h_cam_exp")
        self.lbl_cam_exp = QtWidgets.QLabel(self.frm_cam_param)
        self.lbl_cam_exp.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cam_exp.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lbl_cam_exp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cam_exp.setObjectName("lbl_cam_exp")
        self.lay_h_cam_exp.addWidget(self.lbl_cam_exp)
        self.cbx_cam_exp = QtWidgets.QComboBox(self.frm_cam_param)
        self.cbx_cam_exp.setMaximumSize(QtCore.QSize(180, 16777215))
        self.cbx_cam_exp.setObjectName("cbx_cam_exp")
        self.lay_h_cam_exp.addWidget(self.cbx_cam_exp)
        self.verticalLayout_8.addLayout(self.lay_h_cam_exp)
        self.lay_h_cam_fnum = QtWidgets.QHBoxLayout()
        self.lay_h_cam_fnum.setObjectName("lay_h_cam_fnum")
        self.lbl_cam_fval = QtWidgets.QLabel(self.frm_cam_param)
        self.lbl_cam_fval.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cam_fval.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lbl_cam_fval.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cam_fval.setObjectName("lbl_cam_fval")
        self.lay_h_cam_fnum.addWidget(self.lbl_cam_fval)
        self.cbx_cam_fval = QtWidgets.QComboBox(self.frm_cam_param)
        self.cbx_cam_fval.setMaximumSize(QtCore.QSize(180, 16777215))
        self.cbx_cam_fval.setObjectName("cbx_cam_fval")
        self.lay_h_cam_fnum.addWidget(self.cbx_cam_fval)
        self.verticalLayout_8.addLayout(self.lay_h_cam_fnum)
        self.lay_h_cam_qoi = QtWidgets.QHBoxLayout()
        self.lay_h_cam_qoi.setObjectName("lay_h_cam_qoi")
        self.lbl_cam_qoi = QtWidgets.QLabel(self.frm_cam_param)
        self.lbl_cam_qoi.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cam_qoi.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lbl_cam_qoi.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cam_qoi.setObjectName("lbl_cam_qoi")
        self.lay_h_cam_qoi.addWidget(self.lbl_cam_qoi)
        self.cbx_cam_qoi = QtWidgets.QComboBox(self.frm_cam_param)
        self.cbx_cam_qoi.setMaximumSize(QtCore.QSize(180, 16777215))
        self.cbx_cam_qoi.setObjectName("cbx_cam_qoi")
        self.lay_h_cam_qoi.addWidget(self.cbx_cam_qoi)
        self.verticalLayout_8.addLayout(self.lay_h_cam_qoi)
        self.lay_h_cam_fmod = QtWidgets.QHBoxLayout()
        self.lay_h_cam_fmod.setObjectName("lay_h_cam_fmod")
        self.lbl_cam_fmod = QtWidgets.QLabel(self.frm_cam_param)
        self.lbl_cam_fmod.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cam_fmod.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lbl_cam_fmod.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cam_fmod.setObjectName("lbl_cam_fmod")
        self.lay_h_cam_fmod.addWidget(self.lbl_cam_fmod)
        self.cbx_cam_fmod = QtWidgets.QComboBox(self.frm_cam_param)
        self.cbx_cam_fmod.setMaximumSize(QtCore.QSize(180, 16777215))
        self.cbx_cam_fmod.setObjectName("cbx_cam_fmod")
        self.lay_h_cam_fmod.addWidget(self.cbx_cam_fmod)
        self.verticalLayout_8.addLayout(self.lay_h_cam_fmod)
        self.lay_h_cam_epg = QtWidgets.QHBoxLayout()
        self.lay_h_cam_epg.setObjectName("lay_h_cam_epg")
        self.lbl_cam_epg = QtWidgets.QLabel(self.frm_cam_param)
        self.lbl_cam_epg.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cam_epg.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lbl_cam_epg.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cam_epg.setObjectName("lbl_cam_epg")
        self.lay_h_cam_epg.addWidget(self.lbl_cam_epg)
        self.cbx_cam_epg = QtWidgets.QComboBox(self.frm_cam_param)
        self.cbx_cam_epg.setMaximumSize(QtCore.QSize(180, 16777215))
        self.cbx_cam_epg.setObjectName("cbx_cam_epg")
        self.lay_h_cam_epg.addWidget(self.cbx_cam_epg)
        self.verticalLayout_8.addLayout(self.lay_h_cam_epg)
        self.lay_h_cam_cpt = QtWidgets.QHBoxLayout()
        self.lay_h_cam_cpt.setObjectName("lay_h_cam_cpt")
        self.lbl_cam_cpt = QtWidgets.QLabel(self.frm_cam_param)
        self.lbl_cam_cpt.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cam_cpt.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lbl_cam_cpt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cam_cpt.setObjectName("lbl_cam_cpt")
        self.lay_h_cam_cpt.addWidget(self.lbl_cam_cpt)
        self.cbx_cam_cpt = QtWidgets.QComboBox(self.frm_cam_param)
        self.cbx_cam_cpt.setMaximumSize(QtCore.QSize(180, 16777215))
        self.cbx_cam_cpt.setObjectName("cbx_cam_cpt")
        self.lay_h_cam_cpt.addWidget(self.cbx_cam_cpt)
        self.verticalLayout_8.addLayout(self.lay_h_cam_cpt)
        self.lay_h_cam_met = QtWidgets.QHBoxLayout()
        self.lay_h_cam_met.setObjectName("lay_h_cam_met")
        self.lbl_cam_met = QtWidgets.QLabel(self.frm_cam_param)
        self.lbl_cam_met.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_cam_met.setMaximumSize(QtCore.QSize(180, 16777215))
        self.lbl_cam_met.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_cam_met.setObjectName("lbl_cam_met")
        self.lay_h_cam_met.addWidget(self.lbl_cam_met)
        self.cbx_cam_met = QtWidgets.QComboBox(self.frm_cam_param)
        self.cbx_cam_met.setMaximumSize(QtCore.QSize(180, 16777215))
        self.cbx_cam_met.setObjectName("cbx_cam_met")
        self.lay_h_cam_met.addWidget(self.cbx_cam_met)
        self.verticalLayout_8.addLayout(self.lay_h_cam_met)
        self.horizontalLayout_8.addWidget(self.frm_cam_param)
        self.tab_conf_main.addTab(self.tab_camera, "")
        self.tab_applications = QtWidgets.QWidget()
        self.tab_applications.setObjectName("tab_applications")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.tab_applications)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.grp_ocr = QtWidgets.QGroupBox(self.tab_applications)
        self.grp_ocr.setObjectName("grp_ocr")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.grp_ocr)
        self.verticalLayout_17.setContentsMargins(-1, 20, -1, -1)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.lbl_ocr_psm = QtWidgets.QLabel(self.grp_ocr)
        self.lbl_ocr_psm.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_ocr_psm.setObjectName("lbl_ocr_psm")
        self.verticalLayout_15.addWidget(self.lbl_ocr_psm)
        self.cbx_psm = QtWidgets.QComboBox(self.grp_ocr)
        self.cbx_psm.setObjectName("cbx_psm")
        self.verticalLayout_15.addWidget(self.cbx_psm)
        self.verticalLayout_17.addLayout(self.verticalLayout_15)
        self.verticalLayout_14.addWidget(self.grp_ocr)
        self.grp_ocr_lang = QtWidgets.QGroupBox(self.tab_applications)
        self.grp_ocr_lang.setObjectName("grp_ocr_lang")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.grp_ocr_lang)
        self.horizontalLayout_3.setContentsMargins(-1, 20, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lay_v_available = QtWidgets.QVBoxLayout()
        self.lay_v_available.setContentsMargins(-1, 0, -1, -1)
        self.lay_v_available.setObjectName("lay_v_available")
        self.lbl_ocr_lang_available = QtWidgets.QLabel(self.grp_ocr_lang)
        self.lbl_ocr_lang_available.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_ocr_lang_available.setObjectName("lbl_ocr_lang_available")
        self.lay_v_available.addWidget(self.lbl_ocr_lang_available)
        self.lst_lang_available = QtWidgets.QListWidget(self.grp_ocr_lang)
        self.lst_lang_available.setObjectName("lst_lang_available")
        self.lay_v_available.addWidget(self.lst_lang_available)
        self.horizontalLayout_3.addLayout(self.lay_v_available)
        self.lay_v_sel_lang = QtWidgets.QVBoxLayout()
        self.lay_v_sel_lang.setContentsMargins(-1, -1, 0, -1)
        self.lay_v_sel_lang.setObjectName("lay_v_sel_lang")
        self.btn_ocr_lang_on = QtWidgets.QPushButton(self.grp_ocr_lang)
        self.btn_ocr_lang_on.setMinimumSize(QtCore.QSize(20, 0))
        self.btn_ocr_lang_on.setMaximumSize(QtCore.QSize(20, 16777215))
        self.btn_ocr_lang_on.setText("")
        self.btn_ocr_lang_on.setFlat(True)
        self.btn_ocr_lang_on.setObjectName("btn_ocr_lang_on")
        self.lay_v_sel_lang.addWidget(self.btn_ocr_lang_on)
        self.btn_ocr_lang_off = QtWidgets.QPushButton(self.grp_ocr_lang)
        self.btn_ocr_lang_off.setMinimumSize(QtCore.QSize(20, 0))
        self.btn_ocr_lang_off.setMaximumSize(QtCore.QSize(20, 16777215))
        self.btn_ocr_lang_off.setText("")
        self.btn_ocr_lang_off.setFlat(True)
        self.btn_ocr_lang_off.setObjectName("btn_ocr_lang_off")
        self.lay_v_sel_lang.addWidget(self.btn_ocr_lang_off)
        self.horizontalLayout_3.addLayout(self.lay_v_sel_lang)
        self.lay_v_use = QtWidgets.QVBoxLayout()
        self.lay_v_use.setContentsMargins(-1, 0, -1, -1)
        self.lay_v_use.setObjectName("lay_v_use")
        self.lbl_ocr_lang_use = QtWidgets.QLabel(self.grp_ocr_lang)
        self.lbl_ocr_lang_use.setMinimumSize(QtCore.QSize(0, 30))
        self.lbl_ocr_lang_use.setObjectName("lbl_ocr_lang_use")
        self.lay_v_use.addWidget(self.lbl_ocr_lang_use)
        self.lst_lang_selected = QtWidgets.QListWidget(self.grp_ocr_lang)
        self.lst_lang_selected.setObjectName("lst_lang_selected")
        self.lay_v_use.addWidget(self.lst_lang_selected)
        self.horizontalLayout_3.addLayout(self.lay_v_use)
        self.verticalLayout_14.addWidget(self.grp_ocr_lang)
        self.grp_ocr_lang.raise_()
        self.grp_ocr.raise_()
        self.tab_conf_main.addTab(self.tab_applications, "")
        self.tab_thirdparty = QtWidgets.QWidget()
        self.tab_thirdparty.setObjectName("tab_thirdparty")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.tab_thirdparty)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.gbx_geospatial = QtWidgets.QGroupBox(self.tab_thirdparty)
        self.gbx_geospatial.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.gbx_geospatial.setObjectName("gbx_geospatial")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.gbx_geospatial)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lay_h_map = QtWidgets.QHBoxLayout()
        self.lay_h_map.setObjectName("lay_h_map")
        self.lbl_map_tile = QtWidgets.QLabel(self.gbx_geospatial)
        self.lbl_map_tile.setMinimumSize(QtCore.QSize(150, 30))
        self.lbl_map_tile.setMaximumSize(QtCore.QSize(150, 30))
        self.lbl_map_tile.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_map_tile.setObjectName("lbl_map_tile")
        self.lay_h_map.addWidget(self.lbl_map_tile)
        self.cbx_map_tile = QtWidgets.QComboBox(self.gbx_geospatial)
        self.cbx_map_tile.setObjectName("cbx_map_tile")
        self.cbx_map_tile.addItem("")
        self.cbx_map_tile.addItem("")
        self.cbx_map_tile.addItem("")
        self.cbx_map_tile.addItem("")
        self.cbx_map_tile.addItem("")
        self.cbx_map_tile.addItem("")
        self.lay_h_map.addWidget(self.cbx_map_tile)
        self.verticalLayout_2.addLayout(self.lay_h_map)
        self.verticalLayout_11.addWidget(self.gbx_geospatial)
        self.gbx_flickr = QtWidgets.QGroupBox(self.tab_thirdparty)
        self.gbx_flickr.setObjectName("gbx_flickr")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.gbx_flickr)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lay_h_flc_api = QtWidgets.QHBoxLayout()
        self.lay_h_flc_api.setObjectName("lay_h_flc_api")
        self.lbl_flc_api = QtWidgets.QLabel(self.gbx_flickr)
        self.lbl_flc_api.setMinimumSize(QtCore.QSize(150, 30))
        self.lbl_flc_api.setMaximumSize(QtCore.QSize(150, 30))
        self.lbl_flc_api.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_flc_api.setObjectName("lbl_flc_api")
        self.lay_h_flc_api.addWidget(self.lbl_flc_api)
        self.txt_flc_api = QtWidgets.QLineEdit(self.gbx_flickr)
        self.txt_flc_api.setObjectName("txt_flc_api")
        self.lay_h_flc_api.addWidget(self.txt_flc_api)
        self.verticalLayout_4.addLayout(self.lay_h_flc_api)
        self.lay_h_flc_sec = QtWidgets.QHBoxLayout()
        self.lay_h_flc_sec.setObjectName("lay_h_flc_sec")
        self.lbl_flc_sec = QtWidgets.QLabel(self.gbx_flickr)
        self.lbl_flc_sec.setMinimumSize(QtCore.QSize(150, 30))
        self.lbl_flc_sec.setMaximumSize(QtCore.QSize(150, 30))
        self.lbl_flc_sec.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lbl_flc_sec.setObjectName("lbl_flc_sec")
        self.lay_h_flc_sec.addWidget(self.lbl_flc_sec)
        self.txt_flc_sec = QtWidgets.QLineEdit(self.gbx_flickr)
        self.txt_flc_sec.setObjectName("txt_flc_sec")
        self.lay_h_flc_sec.addWidget(self.txt_flc_sec)
        self.verticalLayout_4.addLayout(self.lay_h_flc_sec)
        self.verticalLayout_11.addWidget(self.gbx_flickr)
        self.dummy_0001 = QtWidgets.QFrame(self.tab_thirdparty)
        self.dummy_0001.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dummy_0001.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dummy_0001.setObjectName("dummy_0001")
        self.verticalLayout_11.addWidget(self.dummy_0001)
        self.tab_conf_main.addTab(self.tab_thirdparty, "")
        self.lay_v_main.addWidget(self.tab_conf_main)
        self.lay_v_entire.addWidget(self.frm_conf_main)
        self.frm_conf_btns = QtWidgets.QFrame(configurationDialog)
        self.frm_conf_btns.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frm_conf_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frm_conf_btns.setObjectName("frm_conf_btns")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frm_conf_btns)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.bbx_conf_res = QtWidgets.QDialogButtonBox(self.frm_conf_btns)
        self.bbx_conf_res.setOrientation(QtCore.Qt.Horizontal)
        self.bbx_conf_res.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bbx_conf_res.setObjectName("bbx_conf_res")
        self.verticalLayout_7.addWidget(self.bbx_conf_res)
        self.lay_v_entire.addWidget(self.frm_conf_btns)

        self.retranslateUi(configurationDialog)
        self.tab_conf_main.setCurrentIndex(0)
        self.cbx_psm.setCurrentIndex(-1)
        self.bbx_conf_res.accepted.connect(configurationDialog.accept) # type: ignore
        self.bbx_conf_res.rejected.connect(configurationDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(configurationDialog)

    def retranslateUi(self, configurationDialog):
        _translate = QtCore.QCoreApplication.translate
        configurationDialog.setWindowTitle(_translate("configurationDialog", "Preference"))
        self.gbx_general.setTitle(_translate("configurationDialog", "テーマの設定"))
        self.lbl_thm_lang.setText(_translate("configurationDialog", "言語の設定 : "))
        self.cbx_thm_lang.setItemText(0, _translate("configurationDialog", "日本語"))
        self.cbx_thm_lang.setItemText(1, _translate("configurationDialog", "English"))
        self.lbl_thm_skin.setText(_translate("configurationDialog", "色の設定 : "))
        self.cbx_skin.setItemText(0, _translate("configurationDialog", "Grey"))
        self.cbx_skin.setItemText(1, _translate("configurationDialog", "White"))
        self.gbx_tool.setTitle(_translate("configurationDialog", "ツールの設定"))
        self.lbl_tool_awb.setText(_translate("configurationDialog", "ホワイトバランス : "))
        self.cbx_tool_awb.setItemText(0, _translate("configurationDialog", "retinex_adjusted"))
        self.cbx_tool_awb.setItemText(1, _translate("configurationDialog", "stretch"))
        self.cbx_tool_awb.setItemText(2, _translate("configurationDialog", "gray_world"))
        self.cbx_tool_awb.setItemText(3, _translate("configurationDialog", "max_white"))
        self.cbx_tool_awb.setItemText(4, _translate("configurationDialog", "retinex"))
        self.cbx_tool_awb.setItemText(5, _translate("configurationDialog", "stdev_luminance"))
        self.cbx_tool_awb.setItemText(6, _translate("configurationDialog", "stdev_grey_world"))
        self.cbx_tool_awb.setItemText(7, _translate("configurationDialog", "luminance_weighted"))
        self.cbx_tool_awb.setItemText(8, _translate("configurationDialog", "automatic"))
        self.lbl_tool_psp.setText(_translate("configurationDialog", "パンシャープン : "))
        self.cbx_tool_psp.setItemText(0, _translate("configurationDialog", "ihsConvert"))
        self.cbx_tool_psp.setItemText(1, _translate("configurationDialog", "simpleMeanConvert"))
        self.cbx_tool_psp.setItemText(2, _translate("configurationDialog", "broveyConvert"))
        self.grp_textedit.setTitle(_translate("configurationDialog", "既定のアプリ"))
        self.lbl_exe_textedit.setText(_translate("configurationDialog", "テキストエディタ"))
        self.tbx_exe_textedit.setText(_translate("configurationDialog", "gedit"))
        self.grp_net_proxy.setTitle(_translate("configurationDialog", "プロキシの設定"))
        self.rbtn_no_proxy.setText(_translate("configurationDialog", "NO PROXY"))
        self.rbtn_proxy.setText(_translate("configurationDialog", "HTT_PROXY"))
        self.tab_conf_main.setTabText(self.tab_conf_main.indexOf(self.tab_general), _translate("configurationDialog", "一般"))
        self.lbl_cur_cam.setText(_translate("configurationDialog", "Current Camera:"))
        self.lbl_cur_cam_nam.setText(_translate("configurationDialog", "No Camera"))
        self.tre_cam.headerItem().setText(0, _translate("configurationDialog", "port"))
        self.tre_cam.headerItem().setText(1, _translate("configurationDialog", "name"))
        self.btn_cam_conn.setText(_translate("configurationDialog", "接続"))
        self.lbl_cam_size.setText(_translate("configurationDialog", "<html><head/><body><p>Image Size</p></body></html>"))
        self.lbl_cam_iso.setText(_translate("configurationDialog", "ISO Speed Rating"))
        self.lbl_cam_wht.setText(_translate("configurationDialog", "White Balance"))
        self.lbl_cam_exp.setText(_translate("configurationDialog", "Exposure Compensation"))
        self.lbl_cam_fval.setText(_translate("configurationDialog", "F-Number"))
        self.lbl_cam_qoi.setText(_translate("configurationDialog", "Image Quality"))
        self.lbl_cam_fmod.setText(_translate("configurationDialog", "Focus Mode"))
        self.lbl_cam_epg.setText(_translate("configurationDialog", "Exposure Program"))
        self.lbl_cam_cpt.setText(_translate("configurationDialog", "Capture Mode"))
        self.lbl_cam_met.setText(_translate("configurationDialog", "Metering Mode"))
        self.tab_conf_main.setTabText(self.tab_conf_main.indexOf(self.tab_camera), _translate("configurationDialog", "カメラ接続"))
        self.grp_ocr.setTitle(_translate("configurationDialog", "Tesseract OCR"))
        self.lbl_ocr_psm.setText(_translate("configurationDialog", "Page Segmentation Modes"))
        self.grp_ocr_lang.setTitle(_translate("configurationDialog", "使用言語"))
        self.lbl_ocr_lang_available.setText(_translate("configurationDialog", "Available Languages"))
        self.lbl_ocr_lang_use.setText(_translate("configurationDialog", "Selected Languages"))
        self.tab_conf_main.setTabText(self.tab_conf_main.indexOf(self.tab_applications), _translate("configurationDialog", "ツール"))
        self.gbx_geospatial.setTitle(_translate("configurationDialog", "地理情報"))
        self.lbl_map_tile.setText(_translate("configurationDialog", "マップタイル："))
        self.cbx_map_tile.setItemText(0, _translate("configurationDialog", "OpenStreetMap"))
        self.cbx_map_tile.setItemText(1, _translate("configurationDialog", "Google Streets"))
        self.cbx_map_tile.setItemText(2, _translate("configurationDialog", "Google Hybrid"))
        self.cbx_map_tile.setItemText(3, _translate("configurationDialog", "Google Satellite"))
        self.cbx_map_tile.setItemText(4, _translate("configurationDialog", "Google Terrain"))
        self.cbx_map_tile.setItemText(5, _translate("configurationDialog", "地理院タイル"))
        self.gbx_flickr.setTitle(_translate("configurationDialog", "flickrの設定"))
        self.lbl_flc_api.setText(_translate("configurationDialog", "API KEY : "))
        self.lbl_flc_sec.setText(_translate("configurationDialog", "Secret : "))
        self.tab_conf_main.setTabText(self.tab_conf_main.indexOf(self.tab_thirdparty), _translate("configurationDialog", "外部サービス"))
