# ST-PrivateClipboardManager

![Main](https://github.com/jfcherng-sublime/ST-PrivateClipboardManager/workflows/Main/badge.svg?branch=master)
[![Required ST Build](https://img.shields.io/badge/ST-4085+-orange.svg?style=flat-square&logo=sublime-text)](https://www.sublimetext.com)
[![Package Control](https://img.shields.io/packagecontrol/dt/PrivateClipboardManager?style=flat-square)](https://packagecontrol.io/packages/PrivateClipboardManager)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/tag/jfcherng-sublime/ST-PrivateClipboardManager?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-PrivateClipboardManager/tags)
[![Project license](https://img.shields.io/github/license/jfcherng-sublime/ST-PrivateClipboardManager?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-PrivateClipboardManager/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/jfcherng-sublime/ST-PrivateClipboardManager?style=flat-square&logo=github)](https://github.com/jfcherng-sublime/ST-PrivateClipboardManager/stargazers)
[![Donate to this project using Paypal](https://img.shields.io/badge/paypal-donate-blue.svg?style=flat-square&logo=paypal)](https://www.paypal.me/jfcherng/5usd)

Provides a private text-only clipboard which won't pollute the system one.

Note that this plugin only works on Sublime Text >= 4085.

## Why

- This plugin won't pollute the system clipboard.
- ST has some problems when pasting multi-line content with multi-cursor.

  For example,

  1. Copy with two carets. Each cursor selects two lines.
  1. Directly paste the just copied content by <kbd>Ctrl + v</kbd>.
  1. BOOM!!!

- Plugin commands can be handy in chained commands or macros.

## Features

- It provides a private clipboard, which won't modify the system clipboard, in ST.
- It pastes what it copied as-is, if the caret counts matches.
- It keeps a certain numbers of newest clipboard histories.

## Install

1. This plugin is not published on the official Package Control.
   To install, add a custom repository for Package Control with steps described
   [here](https://github.com/jfcherng-sublime/ST-my-package-control/blob/master/README.md#usage).
1. Install `PrivateClipboardManager` via Package Control.

## Settings

To edit settings, go to `Preferences` » `Package Settings` » `PrivateClipboardManager` » `Settings`.

I try to make the [settings file](https://github.com/jfcherng-sublime/ST-PrivateClipboardManager/blob/master/PrivateClipboardManager.sublime-settings)
self-explanatory. But if you still have questions, feel free to open an issue.

## Key Bindings

- <kbd>Alt + p</kbd>, <kbd>Alt + c</kbd>:
  Copy texts from selected regions into the clipboard.

- <kbd>Alt + p</kbd>, <kbd>Alt + x</kbd>:
  Cut texts from selected regions into the clipboard.

- <kbd>Alt + p</kbd>, <kbd>Alt + v</kbd>:
  Directly paste the newest item in the clipboard without asking.

- <kbd>Alt + p</kbd>, <kbd>Alt + p</kbd>:
  Open a quick panel to let you choose which item to be pasted.

- <kbd>Alt + p</kbd>, <kbd>Alt + Delete</kbd>:
  Remove all items from the clipboard.
