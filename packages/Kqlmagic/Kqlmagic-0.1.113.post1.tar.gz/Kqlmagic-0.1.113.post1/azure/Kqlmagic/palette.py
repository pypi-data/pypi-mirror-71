# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import six
import warnings

# to suppress 'pandas.util.testing is depreciated' warnig for some combinations of pandas with seaborn
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import seaborn as sns


class Color(object):

    def __init__(self, rgb_color, name=None, **kwargs):
        self.color = rgb_color
        self.name = name or rgb_color


    def _repr_html_(self):
        return self._to_html()


    def _to_html(self):
        c = f'<div style="background-color:{self.color};height:20px;width:20px;display:inline-block;"></div>'
        return f'<div style="display:inline-block;padding:10px;"><div>{self.name}</div>{c}</div>'


    def __repr__(self):
        return self.color


class Palette(list):

    def __init__(self, palette_name=None, n_colors=None, desaturation=None, rgb_palette=None, range_start=None, to_reverse=False, **kwargs):
        self.name = palette_name or Palettes.DEFAULT_NAME
        self.n_colors = (n_colors or Palettes.DEFAULT_N_COLORS) if rgb_palette is None else len(rgb_palette)
        self.desaturation = desaturation or Palettes.DEFAULT_DESATURATION
        self.kwargs = kwargs
        self.range_start = range_start

        parsed = self.parse(self.name)
        self.name = parsed.get("name") or self.name

        if rgb_palette is None:
            rgb_palette = parsed.get("rgb_palette")
            if rgb_palette is None:
                sns_pallete = sns.color_palette(palette=parsed.get("base_name"), n_colors=self.n_colors, desat=self.desaturation)
                rgb_palette = ["rgb" + str((int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255))) for rgb in sns_pallete]
            if parsed.get("slice"):
                rgb_palette = rgb_palette.__getitem__(parsed.get("slice"))
            if parsed.get("reversed") is not None and parsed.get("reversed"):
                rgb_palette = list(reversed(rgb_palette))
            if to_reverse:
                rgb_palette = list(reversed(rgb_palette))
        super(Palette, self).__init__()
        self.extend(rgb_palette)


    def _to_html(self, add_details_to_name=True):
        name = self.name
        if self.range_start is not None:
            name = f"{name}[{self.range_start}:{self.range_start + len(self)}]"
        if add_details_to_name:
            desaturation_details = ""
            if self.desaturation is not None and self.desaturation > 0 and self.desaturation < 1.0:
                desaturation_details = f", desaturation {self.desaturation}"
            name = f"{name} ({self.n_colors} colors{desaturation_details})"
        s_s = ""
        for color in self:
            s_s = f'{s_s}<div style="background-color:{color};height:20px;width:20px;display:inline-block;"></div>'
            
        return f'<div style="display:inline-block;padding:10px;"><div>{name}</div>{s_s}</div>'


    def __getitem__(self, key):
        item = super(Palette, self).__getitem__(key)
        if isinstance(key, slice):
            range_start = min((key.start or 0), len(self)) + (self.range_start or 0)
            return Palette(palette_name=self.name, desaturation=self.desaturation, rgb_palette=item, range_start=range_start, **self.kwargs)
        else:
            return Color(item, name=f"{self.name}[{(self.range_start or 0) + key}]")


    def _repr_html_(self):
        return self._to_html()


    @classmethod
    def parse(cls, name):
        name = name.strip()
        reverse = name.endswith("_r")
        base_name = name[:-2] if reverse else name

        rgb_palette = None
        range = None

        if base_name.endswith("]"):
            start = base_name.rfind("[")
            # slice
            if start > 0:
                se_parts = [value.strip() for value in base_name[start + 1 : -1].split(":")]
                if len(se_parts) == 2:
                    try:
                        range = slice(*[int(value) if value else None for value in se_parts])
                        base_name = base_name[:start]
                    except:
                        pass

        # custom
        if base_name.startswith("[") and base_name.endswith("]"):
            rgb_palette = eval(base_name.lower().replace("-", "").replace("_", ""))
            if not isinstance(rgb_palette, list) or len(rgb_palette) == 0:
                raise ValueError("invlaid custom palette syntax, should be a comma separate list.'[\"rgb(r,g,b)\",...]'")

            for rgb in rgb_palette:
                if not isinstance(rgb, str) or not rgb.startswith("rgb"):
                    raise ValueError("invlaid custom palette syntax, each item must have a 'rgb' prefix.'[\"rgb(r,g,b)\",\"rgb(...)\",...]'")
                color_list = eval(rgb[3:])
                if len(color_list) != 3:
                    raise ValueError("invlaid custom palette syntax, each color must be composed of a list of 3 number: \"rgb(r,g,b)\"")

                for color in color_list:
                    if not isinstance(color, six.integer_types) or color < 0 or color > 255:
                        raise ValueError("invlaid custom palette syntax, each basic color (r,g,b) must between 0 to 255")
            name = name.lower().replace("-", "").replace("_", "").replace(" ", "")
            base_name = None

        return {"name": name, "base_name": base_name, "rgb_palette": rgb_palette, "reversed": reverse, "slice": range}


    @classmethod
    def validate_palette_name(cls, name):
        parsed = cls.parse(name)
        if parsed.get("rgb_palette") is None and parsed.get("base_name") not in Palettes.BASE_PALETTE_NAMES:
            raise ValueError(
                f"must be a known palette name or custom palette (see option -popup_palettes) , but a value of {name} was specified."
            )


    @classmethod
    def validate_palette_desaturation(cls, desaturation):
        if desaturation > 1 or desaturation < 0:
            raise ValueError(f"must be between 0 and 1, but a value of {str(desaturation)} was specified.")


    @classmethod
    def validate_palette_colors(cls, n_colors):
        if n_colors < 1:
            raise ValueError(f"must be greater or equal than 1, but a value of {str(n_colors)} was specified.")


class Palettes(list):

    DEFAULT_DESATURATION = 1.0
    DEFAULT_N_COLORS = 10
    DEFAULT_NAME = "tab10"


    BASE_PALETTE_NAMES = [
        "deep",
        "muted",
        "bright",
        "pastel",
        "dark",
        "colorblind",
        "Accent",
        "Blues",
        "BrBG",
        "BuGn",
        "BuPu",
        "CMRmap",
        "Dark2",
        "GnBu",
        "Greens",
        "Greys",
        "OrRd",
        "Oranges",
        "PRGn",
        "Paired",
        "Pastel1",
        "Pastel2",
        "PiYG",
        "PuBu",
        "PuBuGn",
        "PuOr",
        "PuRd",
        "Purples",
        "RdBu",
        "RdGy",
        "RdPu",
        "RdYlBu",
        "RdYlGn",
        "Reds",
        "Set1",
        "Set2",
        "Set3",
        "Spectral",
        "Wistia",
        "YlGn",
        "YlGnBu",
        "YlOrBr",
        "YlOrRd",
        "afmhot",
        "autumn",
        "binary",
        "bone",
        "brg",
        "bwr",
        "cividis",
        "cool",
        "coolwarm",
        "copper",
        "cubehelix",
        "flag",
        "gist_earth",
        "gist_gray",
        "gist_heat",
        "gist_ncar",
        "gist_rainbow",
        "gist_stern",
        "gist_yarg",
        "gnuplot",
        "gnuplot2",
        "gray",
        "hot",
        "hsv",
        "icefire",
        "inferno",
        "magma",
        "mako",
        "nipy_spectral",
        "ocean",
        "pink",
        "plasma",
        "prism",
        "rainbow",
        "rocket",
        "seismic",
        "spring",
        "summer",
        "tab10",
        "tab20",
        "tab20b",
        "tab20c",
        "terrain",
        "viridis",
        "vlag",
        "winter",
    ]


    def __init__(self, n_colors=None, desaturation=None, palette_list=None, to_reverse=False, **kwargs):
        self.n_colors = n_colors or self.DEFAULT_N_COLORS
        self.desaturation = desaturation or self.DEFAULT_DESATURATION
        self.to_reverse = to_reverse
        self.kwargs = kwargs
        super(Palettes, self).__init__()
        self.extend(palette_list or self.BASE_PALETTE_NAMES)


    def __getitem__(self, key):
        if isinstance(key, str):
            key = self.index(key)
        item = super(Palettes, self).__getitem__(key)
        if isinstance(key, slice):
            return Palettes(palette_list=item, desaturation=self.desaturation, n_colors=self.n_colors, to_reverse=self.to_reverse, **self.kwargs)
        else:
            return Palette(palette_name=item, desaturation=self.desaturation, n_colors=self.n_colors, to_reverse=self.to_reverse, **self.kwargs)


    def _to_html(self):
        n_colors = self.n_colors
        desaturation = self.desaturation
        suffix = f" (desaturation {str(desaturation)})" if desaturation is not None and desaturation != 1.0 and desaturation != 0 else ""
        html_str = f'<div style="text-align:center"><h1>{n_colors} colors palettes{suffix}</h1></div>'
        for name in self:
            for suffix in [""]:  # ['', '_r']:
                s = Palette(palette_name=name + suffix, n_colors=n_colors, desaturation=desaturation, **self.kwargs)
                html_str += s._to_html(add_details_to_name=False)
        return html_str


    def _repr_html_(self):
        return self._to_html()

    # plotly support this css colors:


"""       - A named CSS color:
            aliceblue, antiquewhite, aqua, aquamarine, azure,
            beige, bisque, black, blanchedalmond, blue,
            blueviolet, brown, burlywood, cadetblue,
            chartreuse, chocolate, coral, cornflowerblue,
            cornsilk, crimson, cyan, darkblue, darkcyan,
            darkgoldenrod, darkgray, darkgrey, darkgreen,
            darkkhaki, darkmagenta, darkolivegreen, darkorange,
            darkorchid, darkred, darksalmon, darkseagreen,
            darkslateblue, darkslategray, darkslategrey,
            darkturquoise, darkviolet, deeppink, deepskyblue,
            dimgray, dimgrey, dodgerblue, firebrick,
            floralwhite, forestgreen, fuchsia, gainsboro,
            ghostwhite, gold, goldenrod, gray, grey, green,
            greenyellow, honeydew, hotpink, indianred, indigo,
            ivory, khaki, lavender, lavenderblush, lawngreen,
            lemonchiffon, lightblue, lightcoral, lightcyan,
            lightgoldenrodyellow, lightgray, lightgrey,
            lightgreen, lightpink, lightsalmon, lightseagreen,
            lightskyblue, lightslategray, lightslategrey,
            lightsteelblue, lightyellow, lime, limegreen,
            linen, magenta, maroon, mediumaquamarine,
            mediumblue, mediumorchid, mediumpurple,
            mediumseagreen, mediumslateblue, mediumspringgreen,
            mediumturquoise, mediumvioletred, midnightblue,
            mintcream, mistyrose, moccasin, navajowhite, navy,
            oldlace, olive, olivedrab, orange, orangered,
            orchid, palegoldenrod, palegreen, paleturquoise,
            palevioletred, papayawhip, peachpuff, peru, pink,
            plum, powderblue, purple, red, rosybrown,
            royalblue, saddlebrown, salmon, sandybrown,
            seagreen, seashell, sienna, silver, skyblue,
            slateblue, slategray, slategrey, snow, springgreen,
            steelblue, tan, teal, thistle, tomato, turquoise,
            violet, wheat, white, whitesmoke, yellow,
            yellowgreen
            """

