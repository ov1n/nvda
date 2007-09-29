#IAccessibleHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import comtypesClient
import ctypes
import api
import eventHandler
import IAccessibleHandler
import speech
import NVDAObjects.IAccessible

IServiceProvider=comtypesClient.GetModule('lib/ServProv.tlb').IServiceProvider
IA2Lib=comtypesClient.GetModule('lib/ia2.tlb')

TEXT_BOUNDARY_CHAR=0
TEXT_BOUNDARY_WORD=1
TEXT_BOUNDARY_SENTENCE=2
TEXT_BOUNDARY_PARAGRAPH=3
TEXT_BOUNDARY_LINE=4
TEXT_BOUNDARY_ALL=5

ROLE_UNKNOWN=0
(ROLE_CANVAS,
ROLE_CAPTION,
ROLE_CHECK_MENU_ITEM,
ROLE_COLOR_CHOOSER,
ROLE_DATE_EDITOR,
ROLE_DESKTOP_ICON,
ROLE_DESKTOP_PANE,
ROLE_DIRECTORY_PANE,
ROLE_EDITBAR,
ROLE_EMBEDDED_OBJECT,
ROLE_ENDNOTE,
ROLE_FILE_CHOOSER,
ROLE_FONT_CHOOSER,
ROLE_FOOTER,
ROLE_FOOTNOTE,
ROLE_FORM,
ROLE_FRAME,
ROLE_GLASS_PANE,
ROLE_HEADER,
ROLE_HEADING,
ROLE_ICON,
ROLE_IMAGE_MAP,
ROLE_INPUT_METHOD_WINDOW,
ROLE_INTERNAL_FRAME,
ROLE_LABEL,
ROLE_LAYERED_PANE,
ROLE_NOTE,
ROLE_OPTION_PANE,
ROLE_PAGE,
ROLE_PARAGRAPH,
ROLE_RADIO_MENU_ITEM,
ROLE_REDUNDANT_OBJECT,
ROLE_ROOT_PANE,
ROLE_RULER,
ROLE_SCROLL_PANE,
ROLE_SECTION,
ROLE_SHAPE,
ROLE_SPLIT_PANE,
ROLE_TEAR_OFF_MENU,
ROLE_TERMINAL,
ROLE_TEXT_FRAME,
ROLE_TOGGLE_BUTTON,
ROLE_VIEW_PORT,
)=range(0x401,0x401+43)

(EVENT_ACTION_CHANGED,
EVENT_ACTIVE_DECENDENT_CHANGED,
EVENT_DOCUMENT_ATTRIBUTE_CHANGED,
EVENT_DOCUMENT_CONTENT_CHANGED,
EVENT_DOCUMENT_LOAD_COMPLETE,
EVENT_DOCUMENT_LOAD_STOPPED,
EVENT_DOCUMENT_RELOAD,
EVENT_HYPERLINK_END_INDEX_CHANGED,
EVENT_HYPERLINK_NUMBER_OF_ANCHORS_CHANGED,
EVENT_HYPERLINK_SELECTED_LINK_CHANGED,
EVENT_HYPERTEXT_LINK_ACTIVATED,
EVENT_HYPERTEXT_LINK_SELECTED,
EVENT_HYPERLINK_START_INDEX_CHANGED,
EVENT_HYPERTEXT_CHANGED,
EVENT_HYPERTEXT_NLINKS_CHANGED,
EVENT_OBJECT_ATTRIBUTE_CHANGED,
EVENT_PAGE_CHANGED,  
EVENT_ROLE_CHANGED,
EVENT_TABLE_CAPTION_CHANGED,
EVENT_TABLE_COLUMN_DESCRIPTION_CHANGED,
EVENT_TABLE_COLUMN_HEADER_CHANGED,
EVENT_TABLE_MODEL_CHANGED,
EVENT_TABLE_ROW_DESCRIPTION_CHANGED,
EVENT_TABLE_ROW_HEADER_CHANGED,
EVENT_TABLE_SUMMARY_CHANGED,
EVENT_TEXT_ATTRIBUTE_CHANGED,
EVENT_TEXT_CARET_MOVED,
EVENT_TEXT_CHANGED,
EVENT_TEXT_INSERTED,
EVENT_TEXT_REMOVED,
EVENT_TEXT_UPDATED,
EVENT_TEXT_SELECTION_CHANGED,
EVENT_VISIBLE_DATA_CHANGED,
EVENT_COLUMN_CHANGED,
EVENT_SECTION_CHANGED,
)=range(0x101,0x101+35)

def IA2FromMSAA(pacc):
	if isinstance(pacc,IA2Lib.IAccessible2):
		return pacc
	try:
		try:
			return pacc.QueryInterface(IA2Lib.IAccessible2) 
		except:
			pass
		s=pacc.QueryInterface(IServiceProvider)
		i=s.QueryService(ctypes.byref(IAccessibleHandler.IAccessible._iid_),ctypes.byref(IA2Lib.IAccessible2._iid_))
		newPacc=ctypes.POINTER(IA2Lib.IAccessible2)(i)
		return newPacc
	except:
		return None

def handleActiveDescendantEvent(window,objectID,childID):
	speech.speakMessage("active")
	obj=NVDAObjects.IAccessible.getNVDAObjectFromEvent(window,objectID,childID)
	if not obj:
		return
	obj=obj.activeChild
	if not obj:
		return
	api.setFocusObject(obj)
	eventHandler.manageEvent("gainFocus",obj)
