import altair as alt

from src import *

def main():
    data = load_data('data/raw/animal-rescue.csv')

    chart = alt.Chart(data).mark_point().encode(
            alt.X('Easting_rounded',scale=alt.Scale(zero=False)),
            alt.Y('Northing_rounded',scale=alt.Scale(zero=False)))

    chart.save('chart.html')
    print("Chart created successfully")

if __name__ == '__main__':
    main()
