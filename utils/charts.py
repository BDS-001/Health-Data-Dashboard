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

    fig.add_annotation(
        x=0.02, y=0.98,
        xref='paper', yref='paper',
        text=f'Correlation={r:.2f}',
        showarrow=False,
        font=dict(size=12, color='white'),
        borderpad=4
    )
    return fig
