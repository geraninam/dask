from collections import defaultdict
from itertools import chain

from ..utils import ignoring

with ignoring(ImportError):
    from bokeh.models import ColumnDataSource, Range1d
    from bokeh.palettes import Spectral11
    from bokeh.plotting import figure

def resource_profile_plot(width=600, height=400):
    names = ['times','workers', 'cpu', 'memory-percent']
    source = ColumnDataSource({k: [] for k in names})

    p = figure(width=width, height=height, x_axis_type='datetime',
               tools='xpan,box_zoom,resize,wheel_zoom,reset')
    p.multi_line(xs='times', ys='cpu', line_width=2, line_alpha=0.6,
                 line_dash='solid', color=Spectral11, legend='CPU Usage',
                 source=source)
    p.multi_line(xs='times', ys='memory-percent', line_width=2, line_alpha=0.4,
                 line_dash='8 4', color=Spectral11, legend='Memory Usage',
                 source=source)
    p.legend[0].location = 'top_left'
    p.yaxis[0].axis_label = "Percent"
    p.xaxis[0].axis_label = "Time"

    return source, p

def resource_profile_update(source, worker_buffer, times_buffer):
    data = defaultdict(list)

    workers = sorted(list(set(chain(*list(w.keys() for w in worker_buffer)))))

    for name in ['cpu', 'memory-percent']:
        data[name] = [[msg[w][name] if w in msg else 'null' for msg in worker_buffer] for w in workers]

    data['workers'] = workers
    data['times'] = [[t if w in worker_buffer[i] else 'null' for i, t in enumerate(times_buffer)] for w in workers]

    source.data.update(data)
