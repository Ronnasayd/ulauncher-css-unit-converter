from email.mime import base
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.event import (
    KeywordQueryEvent,
    PreferencesEvent,
    PreferencesUpdateEvent,
)

import logging

logger = logging.getLogger(__name__)

base_value = 16
width_value = 1366
height_value = 768


def vh2px(value):
    return str(float(value) * height_value / 100)


def px2vh(value):
    return str(float(value) * 100 / height_value)


def vw2px(value):
    return str(float(value) * width_value / 100)


def px2vw(value):
    return str(float(value) * 100 / width_value)


def in2px(value):
    return str(float(value) * 96)


def px2in(value):
    return str(float(value) / 96)


def cm2px(value):
    return str(float(value) * 96 / 2.54)


def px2cm(value):
    return str(float(value) * 2.54 / 96)


def mm2px(value):
    return str(float(value) * 96 / 25.4)


def px2mm(value):
    return str(float(value) * 25.4 / 96)


def pt2px(value):
    return str(float(value) * 96 / 72)


def px2pt(value):
    return str(float(value) * 72 / 96)


def pc2px(value):
    return str(float(value) * 96 / 6)


def px2pc(value):
    return str(float(value) * 6 / 96)


def rem2px(value):
    return str(float(value) * base_value)


def px2rem(value):
    return str(float(value) / base_value)


def em2px(value):
    return str(float(value) * base_value)


def px2em(value):
    return str(float(value) / base_value)


maps = {
    "rem": rem2px,
    "em": em2px,
    "in": in2px,
    "cm": cm2px,
    "mm": mm2px,
    "pt": pt2px,
    "pc": pc2px,
    "rem": rem2px,
    "em": em2px,
    "vh": vh2px,
    "vw": vw2px,
}

fns = [
    [
        "rem",
        px2rem,
    ],
    [
        "em",
        px2em,
    ],
    ["vh", px2vh],
    ["vw", px2vw],
    [
        "in",
        px2in,
    ],
    [
        "pt",
        px2pt,
    ],
    [
        "cm",
        px2cm,
    ],
    [
        "mm",
        px2mm,
    ],
    [
        "pc",
        px2pc,
    ],
]


class CSSUnitConverter(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesEvent, PreferencesLoadListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateListener())


class PreferencesLoadListener(EventListener):
    def on_event(self, event, extension):
        global base_value, width_value, height_value
        base_value = float(event.preferences["base"])
        width_value = float(event.preferences["width"])
        height_value = float(event.preferences["height"])


class PreferencesUpdateListener(EventListener):
    def on_event(self, event, extension):
        global base_value, width_value, height_value
        base_value = float(event.preferences["base"])
        width_value = float(event.preferences["width"])
        height_value = float(event.preferences["height"])


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        inps = event.get_query().split()
        if len(inps) != 2:
            return

        if inps[0] in "px":
            results = [f"{v(float(inps[1]))} {k}" for k, v in fns]
        else:
            result = maps[inps[0]](float(inps[1]))
            results = [f"{v(float(result))} {k}" for k, v in fns if k != inps[0]]
            results = [f"{result} px"] + results

        for result in results:
            items.append(
                ExtensionResultItem(
                    icon="images/icon.png",
                    name=result,
                    description=result,
                    on_enter=CopyToClipboardAction(result.replace(" ", "")),
                )
            )

        return RenderResultListAction(items)


if __name__ == "__main__":
    CSSUnitConverter().run()
