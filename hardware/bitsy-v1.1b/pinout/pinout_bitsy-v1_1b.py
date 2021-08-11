import csv
from urllib.request import urlopen

from pinout.core import Group, Image
from pinout.components.layout import Diagram, Panel
from pinout.components.pinlabel import PinLabelGroup
from pinout.components import leaderline as lline


# Load pin data from a web resource
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQE89BpMAF3PvleygKz7c3khpRu-OMNDxSsPL_APcMQ4q1rY2-bD7uYWXYyUwfEbpO6l143bj-qVhWU/pub?output=csv"
response = urlopen(url)
lines = [l.decode("utf-8") for l in response.readlines()]
cr = csv.reader(lines)

################################################################
# Manage data importing and parsing


tags = next(cr)
# Parse data for use as pinlabels (blank labels are dropped here)
# padding labeldata with tag row so row index matches spreadsheet
labeldata = [tags]
for row in cr:
    label_row = []
    for name, tag in zip(row, tags):
        # Omit labels with no name
        if name:
            # Conditionally apply config
            if tag == "notes":
                cfg = {"body": {"width": 140, "x": 0}}
            elif tag.endswith("_id"):
                cfg = {"body": {"width": 45}}
            else:
                cfg = {}
            if tag == tags[1] and len(label_row) == 0:
                cfg["body"]["x"] = 57
            label_row.append((name, tag, cfg))

    labeldata.append(label_row)


################################################################
# Create a new diagram, add styles and a base panel
diagram = Diagram(1012, 1600, "pinout")
diagram.add_stylesheet("styles.css")
content = diagram.add(Panel(width=1012, height=1600, tag="panel__content"))

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
# Front left edge
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
# Front right edge
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
# USB plug detail
usb_pins = content.add(Group(506, 500))
usb_pins.add(
    Image(
        "bitsy-v1.1b_back_detail_1.png",
        width=100,
        height=200,
        embed=True,
    )
)
usb_pins.add(
    PinLabelGroup(
        x=80,
        y=66.5,
        pin_pitch=(0, 22.5),
        label_start=(30, -8.25),
        label_pitch=(0, 28),
        scale=(1, 1),
        labels=labeldata[49:53],
    )
)

################################################################
# Back view
back = content.add(Group(406, 800))
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
        label_start=(180, 81),
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
        label_start=(108, 58),
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

################################################################
# 2 row pin detail
doublerow = content.add(Group(406, 1300))
doublerow.add(
    Image(
        "bitsy-v1.1b_back_detail_2.png",
        width=100,
        height=200,
        embed=True,
    )
)
# inboard double row
doublerow.add(
    PinLabelGroup(
        x=44,
        y=44,
        pin_pitch=(0, 28.25),
        label_start=(80, 0),
        label_pitch=(0, 28.25),
        labels=labeldata[37:42],
        scale=(1, 1),
    )
)
# IO2
doublerow.add(
    PinLabelGroup(
        x=15,
        y=44 + 28.25 * 4,
        pin_pitch=(0, 28.25),
        label_start=(109, 28.25),
        label_pitch=(0, 28.25),
        labels=labeldata[42:43],
        scale=(1, 1),
        leaderline=lline.Curved(direction="vh"),
    )
)
# Edge double row
doublerow.add(
    PinLabelGroup(
        x=15,
        y=44,
        pin_pitch=(0, 28.25),
        label_start=(80, 0),
        label_pitch=(0, 28.25),
        labels=labeldata[44:48],
        scale=(-1, 1),
    )
)

# Output from command-line:
# >>> py -m pinout.manager -e pinout_bitsy-v1_1b pinout_wip_bitsy-v1.1b.svg -o
