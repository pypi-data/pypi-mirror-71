# Pyromenu [![Build Status](https://travis-ci.com/IlhomBahoraliev/pyromenu.svg?branch=master)](https://travis-ci.com/IlhomBahoraliev/pyromenu)

**Pyromenu** is an easy-to-extend object-oriented library for building keyboard menus for telegram bots on the [Pyrogram](https://github.com/pyrogram/pyrogram)

## Base usage case

```python
from pyrogram import Client, Filters, ReplyKeyboardRemove
from pyromenu import KButton, KRow, KMenu


app = Client("app")
# it's menu declaration style
menu = KMenu(
  KRow(
    KButton("English"), KButton("Russian"), KButton("Portugues")
  ),
  KRow(
    KButton("exit")
  )
)


@app.on_message(Filters.command("start"))
def send_keyboard(clt, msg):
  msg.reply("Hi / Привет / Oi", reply_markup=menu.keyboard)

# use KButton update_filter property for creating Filter for Handler's
@app.on_message(KButon("exit").update_filter)
def remove_keyboard(clt, msg):
  msg.reply("Bye / Пока / Adeus", reply_markup=ReplyKeyboardRemove)
```

## ABC's

Pyromenu define 3 abstract classes: [Button](https://github.com/IlhomBahoraliev/pyromenu/tree/master/pyromenu/abc/button.py), [Row](https://github.com/IlhomBahoraliev/pyromenu/tree/master/pyromenu/abc/row.py), [Menu](https://github.com/IlhomBahoraliev/pyromenu/tree/master/pyromenu/abc/menu.py)

- Button
  - `__hash__`
  - `__eq__`
  - `keyboard_button`(properrty) - return KeyboardButton
  - `update_filter`(property) - return Filter
- Row
  - `keyboard_row`(property) - return list of KeyboardButton's
  - `buttons`(property) - return list of Button's
- Menu
  - `keyboard`(property) - return ReplyKeyboardButton
  - `one_time_keyboard`(property) - same as `keyboard`, but with one_time_keyboard flag on
  - `filter`(property) - return composite Filter of all button
  - `matched_button` - take message and return first matched button

## Built-in's

Pyromenu provides simple built-in implementations of each abstract classes: [KButton](https://github.com/IlhomBahoraliev/pyromenu/tree/master/pyromenu/kbutton.py), [KRow](https://github.com/IlhomBahoraliev/pyromenu/tree/master/pyromenu/krow.py), [KMenu](https://github.com/IlhomBahoraliev/pyromenu/tree/master/pyromenu/kmenu.py)

## Usage

Pyromenu has a distinctive menu declaration style inspired by the principles of Elegant Objects.

```python
from pyrogram import Client
from pyromenu import KButton, KRow, KMenu


app = Client("app")
menu = KMenu(
  KRow(
    KButton("English"), KButton("Russian"), KButton("Portugues")
  ),
  KRow(
    KButton("exit")
  )
)
```

### Sending

```python
app.send_message(chat_id, text, reply_markup=menu.keyboard)
# or
# send one time keyboard
app.send_message(chat_id, text, reply_markup=menu.one_time_keyboard)
```

### Handling

```python
@app.on_message(KButton("exit").update_filter)
def exit(clt, msg):
    msg.reply("Bye / Пока / Adeus" reply_markup=ReplyKeyboardRemove)
# or
# if you have more complex menu
@app.on_message(menu.filter)
def handle_menu(clt, msg):
    matched_button = menu.matched_button(msg)
    if matched_button == KButton("exit"):
        msg.reply("Bye / Пока / Adeus" reply_markup=ReplyKeyboardRemove)
    ...
```

### Expanding

All built-in classes have minimal dependency on others. All you need to do is implement abstract class. For example if you need to create button, which send location request you can create that:

```python
from pyrogram import KeyboardButton, Filters
from pyromenu.abc import Button


class LocationButton(Button):
    def __init__(self, text):
        self._text = text

    def __hash__(self):
        return hash(self._text)

    def __eq__(self, other_button):
        return hash(self) == hash(other_button)

    @property
    def keyboard_button(self):
        return KeyboardButton(self._text, request_location=True)

    @property
    def update_filter(self):
        return Filters.create(
            name=f"{self._text}ButtonFilter",
            func=lambda flt, msg: flt.btn_txt == msg.text,
            btn_txt=self._text,
        )
```

or that:

```python
from pyrogram import KeyboardButton
from pyromenu import KButton

class LocationButton(KButton):
    @property
    def keyboard_button(self):
        btn = super().keyboard_button
        btn.request_location = True
        return btn
```

and it's will be works well with any built-in classes

### Installing

```bash
pip3 install pyromenu
```
