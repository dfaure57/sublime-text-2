import sublime, sublime_plugin
import datetime
from package_control.console_write import console_write

# you may copy this file into your Package/User directory

class DafCopyCharAboveSimpleCommand(sublime_plugin.TextCommand):
    # daf_copy_char_above_simple
    def run(self, edit):
        (inirow,inicol) = self.view.rowcol(self.view.sel()[0].begin())
        punto_lectura = self.view.text_point(inirow-1,inicol)
        punto_escritura = self.view.text_point(inirow,inicol)
        char_a_copiar = self.view.substr(punto_lectura)
        ch_ord = ord(char_a_copiar)
        if ch_ord != 10 and ch_ord != 13 and ch_ord != 0:
            self.view.insert(edit, punto_escritura,self.view.substr(punto_lectura))
        else:
            sublime.message_dialog(str(ch_ord))

class DafCopyWordAboveSimpleCommand(sublime_plugin.TextCommand):
    # daf_copy_word_above_simple
    def run(self, edit):
        (inirow,inicol) = self.view.rowcol(self.view.sel()[0].begin())
        punto_escritura = self.view.text_point(inirow,inicol)
        punto_lectura = self.view.text_point(inirow-1,inicol)
        char_a_copiar = self.view.word(punto_lectura)
        self.view.insert(edit, punto_escritura,self.view.substr(char_a_copiar))
        return

class DafCopyCharAboveCommand(sublime_plugin.TextCommand):
    # daf_copy_char_above
    def run(self, edit):
        # salvo mis coor iniciales
        (inirow,inicol) = self.view.rowcol(self.view.sel()[0].begin())
        # punto_escritura es donde insertaremos un char o word
        punto_escritura = self.view.text_point(inirow,inicol)

        # comenzaremos a leer primero la linea anterior
        counter=1
        posible_linea = self.view.text_point(inirow-counter,0)
        posible_region = self.view.line(posible_linea)

        # skip empty lines
        while posible_region.empty():
            counter = counter + 1
            posible_linea = self.view.text_point(inirow-counter,0)
            posible_region = self.view.line(posible_linea)
            pass

        # perform copy
        punto_lectura = self.view.text_point(inirow-counter,inicol)
        char_a_copiar = self.view.substr(punto_lectura)
        ch_ord = ord(char_a_copiar)
        if ch_ord != 10 and ch_ord != 13 and ch_ord != 0:
            self.view.insert(edit, punto_escritura,self.view.substr(punto_lectura))

class DafCopyDownCharacterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('daf_move_down')
        self.view.run_command('daf_copy_char_above_simple')
        self.view.run_command('daf_move_left')

class DafCopyDownWordCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('daf_copy_word_above_simple')
        self.view.run_command('move',{"by": "words", "forward": False})
        self.view.run_command('daf_move_down')

class DafCharAtCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        (inirow,inicol) = self.view.rowcol(self.view.sel()[0].begin())
        char_offset = self.view.text_point(inirow,inicol)
        return self.view.substr(char_offset)

class DafMoveEndCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('daf_remove_trailing_spaces')
        (row,col) = self.view.rowcol(self.view.sel()[0].begin())
        for region in self.view.sel():
            line = self.view.line(region)
        if col==len(line):
            # sublime.message_dialog('finne')
            self.view.run_command('move', {'by': "subwords", 'forward': False})
            pass
        else:
            self.view.run_command('move_to', {"to": "eol", "extend": False})
            pass

class DafMoveLeftCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('move', {'by': "characters", 'forward': False})

class DafMoveRightCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # Me fijo donde estoy
        (row,col) = self.view.rowcol(self.view.sel()[0].begin())
        for region in self.view.sel():
            line = self.view.line(region)
        if col==len(line):
            # Si estoy en el final, agrego espacios a modo de avance
            self.view.run_command('insert', {'characters': ' '})
            pass
        else:
            # Caso contrario, avanzo normalmente
            self.view.run_command('move', {'by': "characters", 'forward': True})
            pass

class DafMoveDownCommand(sublime_plugin.TextCommand):
    def run(self, edit):
    # this will analise how to mode down

        # salvo mis coor iniciales
        (inirow,inicol) = self.view.rowcol(self.view.sel()[0].begin())

        # me muevo en sentido de mi comando
        self.view.run_command('move', {'by': "lines", 'forward': True})
        self.view.run_command('daf_remove_trailing_spaces')

        # calculo si estoy en el final de la linea destino
        (finrow,fincol) = self.view.rowcol(self.view.sel()[0].begin())
        for region in self.view.sel():
            line = self.view.line(region)
        if fincol==len(line):
            # tras moverme, estoy en el final. Capaz es necesario agregar espacios
            if fincol<inicol:
                self.view.run_command('move_to', {"to": "eol", "extend": False})
                for x in xrange(0,inicol-fincol):
                    self.view.run_command('insert', {'characters': ' '})
                    pass
                pass
            pass

class DafMoveUpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
    # this will analise how to mode down

        # salvo mis coor iniciales
        (inirow,inicol) = self.view.rowcol(self.view.sel()[0].begin())

        # me muevo en sentido de mi comando
        self.view.run_command('move', {'by': "lines", 'forward': False})
        self.view.run_command('daf_remove_trailing_spaces')

        # calculo si estoy en el final de la linea destino
        (finrow,fincol) = self.view.rowcol(self.view.sel()[0].begin())
        for region in self.view.sel():
            line = self.view.line(region)
        if fincol==len(line):
            # tras moverme, estoy en el final. Capaz es necesario agregar espacios
            if fincol<inicol:
                self.view.run_command('move_to', {"to": "eol", "extend": False})
                for x in xrange(0,inicol-fincol):
                    self.view.run_command('insert', {'characters': ' '})
                    pass
                pass
            pass

class DafRemoveTrailingSpaces(sublime_plugin.TextCommand):
    def run(self, edit):
            trailing_white_space = self.view.find_all("[\t ]+$")
            trailing_white_space.reverse()
            edit = self.view.begin_edit()
            for r in trailing_white_space:
                self.view.erase(edit, r)
            self.view.end_edit(edit)

