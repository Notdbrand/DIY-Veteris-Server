TARGET := iphone:clang:latest:7.0
export TARGET=iphone:clang:6.0
ARCHS= armv7

include $(THEOS)/makefiles/common.mk

BUNDLE_NAME = VeterisRedirectPref

VeterisRedirectPref_FILES = VeterisRPrefRootListController.m
VeterisRedirectPref_FRAMEWORKS = UIKit
VeterisRedirectPref_PRIVATE_FRAMEWORKS = Preferences
VeterisRedirectPref_INSTALL_PATH = /Library/PreferenceBundles
VeterisRedirectPref_CFLAGS = -fobjc-arc

include $(THEOS_MAKE_PATH)/bundle.mk
