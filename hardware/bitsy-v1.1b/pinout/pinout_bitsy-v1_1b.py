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
diagram = Diagram(1012, 800, "pinout")
diagram.add_stylesheet("styles.css")
content = diagram.add(Panel(width=1012, height=800, tag="panel__content"))

# Create a group to hold the actual diagram components.
graphic = content.add(Group(506, 10))

# Add and embed an image
graphic.add(Image("bitsy-v1.1b_front_resized.png", width=200, height=411, embed=True))

graphic.add(
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

graphic.add(
    PinLabelGroup(
        x=198,
        y=28,
        pin_pitch=(0, 28.25),
        label_start=(30, 0),
        label_pitch=(0, 28.25),
        scale=(1, 1),
        labels=labeldata[30:14:-1],
    )
)

# Output from command-line:
# >>> py -m pinout.manager -e pinout_bitsy-v1_1b pinout_wip_bisty-v1.1b.svg -o
