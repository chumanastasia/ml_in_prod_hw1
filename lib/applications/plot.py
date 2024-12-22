import time
import pandas as pd
import plotly.express as px
from lib.settings import settings
from loguru import logger


def main():
    while True:
        df = pd.read_csv(settings.metric_log_path)

        fig = px.histogram(
            df,
            x='absolute_error',
            nbins=20,
            title='РАО',
            labels={'absolute_error': 'Абсолютная Ошибка'},
            opacity=0.75
        )

        fig.update_layout(
            xaxis_title="Абсолютная Ошибка",
            yaxis_title="Количество",
            template="plotly_dark"
        )

        fig.write_image("logs/error_distribution.png")
        logger.info("Saved error distribution plot")
        time.sleep(settings.time_step)


if __name__ == "__main__":
    logger.add("logs/plot_app.log")
    logger.info("Starting plot app...")
    main()
