import numpy as np

def add_trendline(fig, x, y):
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    r = np.corrcoef(x, y)[0, 1]

    x_sorted = np.sort(x)

    fig.add_scatter(
        x=x_sorted,
        y=p(x_sorted),
        mode='lines',
        name=f'R={r:.2f}',
        line=dict(dash='dash'),
        showlegend=False
    )

    return fig, r
