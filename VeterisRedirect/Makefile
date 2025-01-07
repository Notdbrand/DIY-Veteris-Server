TARGET := iphone:clang:latest:7.0
export TARGET=iphone:clang:6.0
ARCHS= armv7

include $(THEOS)/makefiles/common.mk

TWEAK_NAME = VeterisRedirect

VeterisRedirect_FILES = Tweak.x
VeterisRedirect_CFLAGS = -fobjc-arc

include $(THEOS_MAKE_PATH)/tweak.mk
SUBPROJECTS += VeterisRedirectPref
include $(THEOS_MAKE_PATH)/aggregate.mk
