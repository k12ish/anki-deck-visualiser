# import the main window object (mw) from aqt
from aqt import mw, gui_hooks
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import QAction

from anki.utils import ids2str

from aqt.stats import NewDeckStats
from aqt.webview import WebContent
import sys
import os

ADDON_PACKAGE = mw.addonManager.addonFromModule(__name__)
"/_addons/{ADDON_PACKAGE}/web/my-addon.js"


def generate_stats_data():
    names_and_ids = mw.col.decks.all_names_and_ids()
    ids, labels, parents, card_counts = [], [], [], []
    for item in names_and_ids:
        ids.append(str(item.name))
        split_name = [''] + str(item.name).rsplit('::', 1)
        labels.append(split_name[-1])
        parents.append(split_name[-2])
        card_counts.append(
            mw.col.db.scalar(
                "select count() from cards where did in {0} or "
                "odid in {0}".format(ids2str([item.id]))
            )
        )
    sys.stderr.write(
        """<script type="text/javascript">
var data = [{{
  type: "sunburst",
  ids: {},
  labels: {},
  parents: {},
  values: {},
  branchvalues: 'remainder',
  sort: false,
}}];
var layout = {{
  margin: {{l: 0, r: 0, b: 0, t:0}},
}};
Plotly.newPlot('plotly-sunburst', data, layout)
</script>
""".format(
            str(ids),
            str(labels),
            str(parents),
            str(card_counts)
        ))
    return ids, labels, parents, card_counts


def mytest(web):
    page = os.path.basename(web.page().url().path())
    if page != "graphs.html":
        return
    web.eval(
        """
    div = document.createElement("div");
    div.setAttribute("id", "plotly-sunburst");
    document.body.appendChild(div);
"""
    )


gui_hooks.webview_did_inject_style_into_page.append(mytest)

"""
106ms
def generate_stats_data():
    start = time.time()
    names_and_ids = mw.col.decks.all_names_and_ids()
    ids, labels, parents, card_counts = [], [], [], []
    for item in names_and_ids:
        ids.append(str(item.name))
        split_name = [''] + str(item.name).rsplit('::', 1)
        labels.append(split_name[-1])
        parents.append(split_name[-2])
        card_counts.append(
            mw.col.db.scalar(
                "select count() from cards where did in {0} or "
                "odid in {0}".format(ids2str([item.id]))
            )
        )
    sys.stderr.write("\n\n`generate_stats_data` took: "
                     + str(round((time.time() - start) * 1000))
                     + "ms")
    sys.stderr.write(str(labels))
    sys.stderr.write(str(card_counts))
    sys.stderr.write(str(parents))
    sys.stderr.write(str(labels))
"""
"""
>>> x = "aaaaa::bbbb::cccc"
>>> y = "aaaaa::bbbbbb"
>>> z = "aaaaaaaaa"
>>> x.rsplit("::", 1)
['aaaaa::bbbb', 'cccc']
>>> y.rsplit("::", 1)
['aaaaa', 'bbbbbb']
>>> z.rsplit("::", 1)
['aaaaaaaaa']
"""


def on_stats_dialog_will_show(dialog: NewDeckStats):
    showInfo(str(dialog))


def on_webview_will_set_content(web_content: WebContent, context):
    web_content.body += "my_html"
    web_content.head += ""


gui_hooks.stats_dialog_will_show.append(on_stats_dialog_will_show)
gui_hooks.webview_will_set_content.append(on_webview_will_set_content)


action = QAction("test", mw)
action.triggered.connect(generate_stats_data)
mw.form.menuTools.addAction(action)
