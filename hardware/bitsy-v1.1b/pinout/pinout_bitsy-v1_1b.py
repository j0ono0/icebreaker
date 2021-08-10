import csv
from urllib.request import urlopen

from pinout import config
from pinout.core import Group, Image
from pinout.components.layout import Diagram, Panel
from pinout.components.pinlabel import PinLabelGroup
from pinout.components.annotation import AnnotationLabel
from pinout.components.text import TextBlock
from pinout.components import leaderline as lline
from pinout.components.legend import Legend


# Load pin data from a web resource
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE89BpMAF3PvleygKz7c3khpRu-OMNDxSsPL_APcMQ4q1rY2-bD7uYWXYyUwfEbpO6l143bj-qVhWU/pub?output=csv"
response = urlopen(url)
lines = [l.decode("utf-8") for l in response.readlines()]
cr = csv.reader(lines)

################################################################
# Manage data importing and parsing

# label configs
lbl_conf = None
sm_lbl = {"body": {"width": 45}}
xs_lbl = {"body": {"width": 35}}
xl_lbl = {"body": {"width": 182}}

# Parse data for use as pinlabels (blank labels are dropped here)
labeldata = []
for (a, b, c) in cr:
    # Conditionally assign values where needed
    lbl_conf = sm_lbl
    if a == "GND":
        tag = "gnd"
    elif a.startswith("Vin") or a.startswith("3.3V"):
        tag = "pwr"
        lbl_conf = xl_lbl
    else:
        tag = "pin_id"

    lbl_a = [(str(a), tag, lbl_conf)] if a else []
    lbl_b = [(str(b), "fpga_id", sm_lbl)] if b else []
    lbl_c = [(str(c), "fpga_name")] if c else []
    labeldata += [lbl_a + lbl_b + lbl_c]


################################################################
# Create a new diagram, add styles and a base panel
diagram = Diagram(1012, 1012, "pinout")
diagram.add_stylesheet("styles.css")
content = diagram.add(Panel(width=1012, height=1012, tag="panel__content"))

################################################################
# Create a group to hold the actual diagram components.
# x value centres the hardware
front = content.add(Group(406, 10))

# Add and embed an image
front.add(
    Image(
        "bitsy-v1.1b_front_resized.png",
        width=200,
        height=411,
        embed=True,
    )
)

front.add(
    PinLabelGroup(
        x=2,
        y=28,
        pin_pitch=(0, 28.25),
        label_start=(30, 0),
        label_pitch=(0, 28.25),
        scale=(-1, 1),
        labels=labeldata[1:15],
    )
)

front.add(
    PinLabelGroup(
        x=198,
        y=28,
        pin_pitch=(0, 28.25),
        label_start=(30, 0),
        label_pitch=(0, 28.25),
        scale=(1, 1),
        labels=labeldata[29:14:-1],
    )
)


################################################################
# Back view
back = content.add(Group(406, 500))
back.add(
    Image(
        "bitsy-v1.1b_back_resized.png",
        width=200,
        height=411,
        embed=True,
    )
)
back.add(
    PinLabelGroup(
        x=90,
        y=86,
        pin_pitch=(0, 0),
        label_start=(140, 0),
        label_pitch=(0, 0),
        labels=labeldata[30:31],
        scale=(1, 1),
        leaderline=lline.Curved(direction="vh"),
    )
)
back.add(
    PinLabelGroup(
        x=50,
        y=170,
        pin_pitch=(0, 0),
        label_start=(180, 56),
        label_pitch=(0, 0),
        labels=labeldata[31:32],
        scale=(1, -1),
        leaderline=lline.Curved(direction="vh"),
    )
)
back.add(
    PinLabelGroup(
        x=150,
        y=170,
        pin_pitch=(0, 0),
        label_start=(80, 28),
        label_pitch=(0, 0),
        labels=labeldata[32:33],
        scale=(1, -1),
        leaderline=lline.Curved(direction="vh"),
    )
)
back.add(
    PinLabelGroup(
        x=50,
        y=287,
        pin_pitch=(0, 0),
        label_start=(180, 90),
        label_pitch=(0, 0),
        labels=labeldata[33:34],
        scale=(1, -1),
        leaderline=lline.Curved(direction="vh"),
    )
)
back.add(
    PinLabelGroup(
        x=122,
        y=292,
        pin_pitch=(0, 0),
        label_start=(108, 60),
        label_pitch=(0, 0),
        labels=labeldata[34:35],
        scale=(1, -1),
        leaderline=lline.Curved(direction="vh"),
    )
)
back.add(
    PinLabelGroup(
        x=150,
        y=292,
        pin_pitch=(0, 0),
        label_start=(80, 30),
        label_pitch=(0, 0),
        labels=labeldata[35:36],
        scale=(1, -1),
        leaderline=lline.Curved(direction="vh"),
    )
)

# Output from command-line:
# >>> py -m pinout.manager -e pinout_bitsy-v1_1b pinout_wip_bitsy-v1.1b.svg -o
