import os
import pygame as pg

from .settings import list_guides_menu
from paths import *
from app.functiontools import Obj, draw_texts, save_log_and_exit

VERSION = os.environ.get('VERSION')
GAME_NAME = os.environ.get('GAME_NAME')
DISPLAY_NONE = int(os.environ.get('DISPLAY_NONE'))


class Menu:

    is_active = True
    block = False
    check = ''

    def __init__(self, main_screen, *groups):
        
        self.main_screen = main_screen
        
        self._background = Obj(IMG_MENU['bg'], 0, 0, *groups)

        self._guides = []

        self._objects = {
            'select': Obj(IMG_MENU['select'], 0, DISPLAY_NONE, *groups),
            'info_credit': Obj(IMG_MENU['info_c'], 0, DISPLAY_NONE, *groups),
            'return': Obj(IMG_MENU['return'], 206, DISPLAY_NONE, *groups)
        }
        self._draw_guides()


    def _draw_guides(self):

        pos_x, pos_y = 195, 317

        for item in list_guides_menu:

            draw_texts(
                screen=self.main_screen,
                text='{:^45}'.format(item.title().replace('_', ' ')),
                pos_x=pos_x,
                pos_y=pos_y + 15,
                size=25
                )
            self._guides.append(pg.rect.Rect(pos_x, pos_y, 356, 65))

            pos_y += 90


    def _guide_new_game(self, pos_mouse):

        if self._guides[0].collidepoint(pos_mouse):

            self.check = 'new'
            self.is_active = False
           

    def _guide_load(self, pos_mouse):

        if self._guides[1].collidepoint(pos_mouse):

            self.check = 'load'
            self.is_active = False
          

    def _guide_options(self, pos_mouse):

        if self._guides[3].collidepoint(pos_mouse):

            self.check = 'options'
            self.is_active = False
           

    def _guide_credit(self, pos_mouse):

        if self._guides[2].collidepoint(pos_mouse):

            y, y_ = 0, 942
            self.block = True

        elif self._objects['return'].rect.collidepoint(pos_mouse):

            y, y_ = DISPLAY_NONE, DISPLAY_NONE
            self.block = False

        else:
            return 0

        self._objects['info_credit'].rect.y = y
        self._objects['return'].rect.y = y_
       

    def _guide_quit(self, pos_mouse):

        if self._guides[4].collidepoint(pos_mouse):

            save_log_and_exit()


    def _get_mouse_events_to_show_interactive(self, pos_mouse):

        img_return = 'return'

        if self._objects['return'].rect.collidepoint(pos_mouse):
            img_return = 'select_return'

        self._objects['return'].image = pg.image.load(IMG_MENU[img_return])


    def _select_guides(self, pos_mouse):

        topleft = -1080, - 1080

        for object in self._guides:

            if object.collidepoint(pos_mouse):

                topleft = object.topleft

        self._objects['select'].rect.topleft = topleft


    def events_menu(self, event):

        pos_mouse = pg.mouse.get_pos()

        if event.type == pg.MOUSEBUTTONDOWN:

            self._guide_credit(pos_mouse)

            if not self.block:

                self._guide_new_game(pos_mouse)
                self._guide_load(pos_mouse)
                self._guide_options(pos_mouse)
                self._guide_quit(pos_mouse)

        if not self.block:

            self._select_guides(pos_mouse)

        self._get_mouse_events_to_show_interactive(pos_mouse)


    def update(self) -> None:
               
        draw_texts(
            screen=self.main_screen,
            text=GAME_NAME,
            pos_x=self.main_screen.get_width() / 2 - len(GAME_NAME) * 6.5,
            pos_y=100,
            size=25
            )
        draw_texts(
            screen=self.main_screen,
            text=VERSION,
            pos_x=self.main_screen.get_width() / 2 - len(VERSION),
            pos_y=980
            )

        if not self.block:

            self._draw_guides()
