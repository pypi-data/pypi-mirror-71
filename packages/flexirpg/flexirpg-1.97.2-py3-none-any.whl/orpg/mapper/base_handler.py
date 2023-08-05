# Copyright (C) 2000-2001 The OpenRPG Project
#
#    openrpg-dev@lists.sourceforge.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# --
#
# File: mapper/whiteboard_hander.py
# Author: OpenRPG Team
# Maintainer:
# Version:
#   $Id: base_handler.py,v 1.20 2007/11/04 17:32:25 digitalxero Exp $
#
# Description: base layer handler.
#   layer handlers are responsible for the GUI elements of the layer
#
__version__ = "$Id: base_handler.py,v 1.20 2007/11/04 17:32:25 digitalxero Exp $"


from orpg.orpg_windows import *
from orpg.orpgCore import open_rpg


class base_layer_handler(wx.Panel):

    def __init__(self, parent, id, canvas):
        wx.Panel.__init__(self, parent, id)
        self.canvas = canvas
        self.map_frame = self.canvas.frame
        self.top_frame = self.canvas.frame.top_frame
        self.chat = open_rpg.get_component("chat")
        self.build_ctrls()
        self.build_menu()
        self.Bind(wx.EVT_LEFT_DCLICK, self.on_left_dclick)

    def build_ctrls(self):
        self.basesizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonsizer = wx.BoxSizer(wx.HORIZONTAL)

        mapopen = createMaskedButton( self, orpg.dirpath.dir_struct["icon"]+'open.bmp', 'Load a map', wx.ID_ANY, '#c0c0c0', wx.BITMAP_TYPE_BMP )
        mapsave = createMaskedButton( self, orpg.dirpath.dir_struct["icon"]+'save.bmp', 'Save the map', wx.ID_ANY, '#c0c0c0', wx.BITMAP_TYPE_BMP )
        self.buttonsizer.Add(mapopen, 0, wx.ALIGN_CENTER )
        self.buttonsizer.Add(mapsave, 0, wx.ALIGN_CENTER )

        self.basesizer.Add((3, 0))
        self.basesizer.Add( self.sizer, 1, wx.EXPAND)
        self.basesizer.Add((12, 0))
        self.basesizer.Add( self.buttonsizer, 0, wx.EXPAND)
        self.basesizer.Add((3, 0))
        self.Bind(wx.EVT_BUTTON, self.map_frame.on_open, mapopen)
        self.Bind(wx.EVT_BUTTON, self.map_frame.on_save, mapsave)

        self.SetSizer(self.basesizer)

    def build_menu(self):
        main_menu = wx.Menu()

        item = wx.MenuItem(main_menu, wx.ID_ANY, "&Load Map", "Load Map")
        self.canvas.Bind(wx.EVT_MENU, self.map_frame.on_open, item)
        main_menu.Append(item)

        item = wx.MenuItem(main_menu, wx.ID_ANY, "&Save Map", "Save Map")
        self.canvas.Bind(wx.EVT_MENU, self.map_frame.on_save, item)
        main_menu.Append(item)

        item = wx.MenuItem(main_menu, wx.ID_ANY, "Save as JPG", "Save as JPG")
        self.canvas.Bind(wx.EVT_MENU, self.on_save_map_jpg, item)
        main_menu.Append(item)

        main_menu.AppendSeparator()

        item = wx.MenuItem(main_menu, wx.ID_ANY, "&Properties", "Properties")
        self.canvas.Bind(wx.EVT_MENU, self.canvas.on_prop, item)
        main_menu.Append(item)

        self.main_menu = main_menu

    def on_save_map_jpg(self, evt):
        directory = orpg.dirpath.dir_struct["user"]
        if directory == None:
            directory = ""
        d = wx.FileDialog(self.GetParent(), "Save map as a jpg", directory, "", "*.jpg", wx.FD_SAVE)
        if d.ShowModal() != wx.ID_OK:
            return
        filename = d.GetPath()
        width = self.canvas.size[0]
        height = self.canvas.size[1]
        dc = wx.MemoryDC()
        bitmap = wx.EmptyBitmap(width+1, height+1)
        dc.SelectObject(bitmap)
        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetBrush(wx.Brush(self.canvas.GetBackgroundColour(), wx.SOLID))
        dc.DrawRectangle(0,0,width+1, height+1)
        self.canvas.layers['bg'].layerDraw(dc, 1, [0,0], self.canvas.size)
        self.canvas.layers['grid'].layerDraw(dc, [0,0], self.canvas.size)
        self.canvas.layers['miniatures'].layerDraw(dc, [0,0], self.canvas.size)
        self.canvas.layers['whiteboard'].layerDraw(dc)
        self.canvas.layers['fog'].layerDraw(dc, [0,0], self.canvas.size)
        image = bitmap.ConvertToImage()
        image.SaveFile(filename, wx.BITMAP_TYPE_JPEG)

    def do_map_board_menu(self,pos):
        self.canvas.PopupMenu(self.main_menu,pos)

    def on_right_down(self,evt):
        self.do_map_board_menu(evt.GetPosition())

    def on_left_down(self,evt):
        pass

    def on_left_up(self,evt):
        pass

    #added to base layer by Snowdog 5/03
    def on_left_dclick(self,evt):
        pass

    def on_motion(self,evt):
        pass

    def update_info(self):
        pass
