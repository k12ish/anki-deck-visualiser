from aqt import mw
from aqt.qt import QAction, QStandardPaths, QUrl
from anki.utils import ids2str
from aqt.utils import openLink
import os

HTML = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>Generated Graph</title>
  </head>
  <body>
    <div id="plotly-sunburst" style="width:100%;height:100%"></div>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>{}
  </body>
</html>
"""


def main():
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
    plotly_javascript = """<script type="text/javascript">
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
""".format(str(ids),
           str(labels),
           str(parents),
           str(card_counts)
           )
    path = os.path.join(
        QStandardPaths.writableLocation(QStandardPaths.DownloadLocation),
        "deck-visualiser.html"
    )
    buf = open(path, "w", encoding="utf-8")
    buf.write(HTML.format(plotly_javascript))
    buf.close()
    openLink(QUrl.fromLocalFile(path))


action = QAction("Visualise decks", mw)
action.triggered.connect(main)
mw.form.menuTools.addAction(action)
