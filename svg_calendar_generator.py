import os
import sys
import calendar
from datetime import datetime, timedelta
import argparse
xframe = 1588
yframe = 1122
xsize = 280 # Tamaño horizontal de cada mes
ysize = 256 # Tamaño vertical de cada mes

def get_name(index):
        months = ["Enero", "Febrero", "Marzo",\
                  "Abril", "Mayo", "Junio",\
                  "Julio", "Agosto", "Septiembre",\
                  "Octubre", "Noviembre", "Diciembre"]
        return(months[index - 1])

def last_day_of(year, month):
        if (month == 4) \
        or (month == 6) \
        or (month == 9 ) \
        or (month == 11):
                return 30
        else:
                if (month == 2):
                        if (year % 400 == 0) \
                        or ((year % 4 == 0) and (year % 100 != 0)):
                                return 29
                        else:
                                return 28
                else:
                        return 31

def generate_month_svg(name, days, xpos, ypos):
        svg_month = f"\t<text x=\"{xpos + (xsize / 2)}\" y=\"{ypos + 30}\" font-family=\"Arial\" font-size=\"20\" text-anchor=\"middle\">{name}</text>\n"
        for i in range(0, 7, 1):
                svg_month = svg_month + f"<g>\n"
                for j in range(0, 7, 1):
                        fontw = ""
                        if i == 0:
                                fontw = " font-weight=\"bold\""
                        day = str(days[i][j])
                        if day == "0":
                                day = ""
                        fill = ""
                        if j == 5:
                                fill = " fill=\"blue\""
                        elif j == 6:
                                fill = " fill=\"red\""
                        svg_month = f"\t\t{svg_month}<text x=\"{xpos + (xsize / 8) + ((xsize / 8) * j)}\" y=\"{ypos + ((i * (ysize * 0.11)) + (ysize * 0.25))}\" font-family=\"Arial\" font-size=\"14\" text-anchor=\"middle\"{fill}{fontw}>{day}</text>\n"
                svg_month = svg_month + f"</g>\n"        
        return(svg_month)

def generate_month_array(year, month):
        array = [[0] * 7 for _ in range(7)]
        given_date = datetime.strptime(f"{year}-{month}-1", '%Y-%m-%d')
        dayweek = given_date.weekday()
        iterator = 1
        array[0] = ["L", "M", "X", "J", "V", "S", "D"]
        limit = 1
        last = last_day_of(year, month)
        while limit <= 7:
                array[limit][dayweek] = iterator
                iterator += 1
                dayweek = (dayweek + 1) % 7
                if dayweek == 0:
                        limit += 1
                if (iterator > last):
                        limit = 8
        return array


if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Year')
        parser.add_argument('-y','--year', nargs=1, help='<Required> Set year to generate a calendar for', required=True)
        args = parser.parse_args()

        year = int(args.year[0])
        svg_file = f"<svg width=\"{xframe}\" height=\"{yframe}\" xmlns=\"http://www.w3.org/2000/svg\">\n"
        for i in range(0, 3, 1):
                ypos = ((ysize + 20) * i) + 250 # Posición Y de cada mes
                for j in range(0, 4, 1):
                        month = (j + 1) + (4 * i)
                        arr = generate_month_array(year, month)
                        xpos = (xsize + 20) * j + ((xframe - ((xsize + 20) * 4)) / 2) # Posición X de cada mes
                        svg_file = svg_file + f"<g id=\"{get_name(month)}\">\n"
                        svg_file = svg_file + f"\t<rect x=\"{xpos}\" y=\"{ypos}\" rx=\"15\" ry=\"15\" width=\"{xsize}\" height=\"{ysize}\" fill=\"lightgrey\"/>\n"
                        svg_file = svg_file + f"{generate_month_svg(get_name(month) + f" {year}", arr, xpos, ypos)}"
                        svg_file = svg_file + f"</g>\n"       
        svg_file = svg_file + "</svg>"
        f = open("test.svg", "w") 
        f.write(svg_file)
        f.close()
