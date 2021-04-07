from math import e, pi

from matplotlib import pyplot

sensors = [[50, 75, 100], [150, 75, 100]]

x0, y0, r = sensors[0]

segment_count = 100

width, height = [200, 150]

locus = [complex(y0, x0) + r * e ** (2j * pi / segment_count * segment) for segment in range(segment_count)]
print('Locus:', locus)

locus_in_room = [point for point in locus if height >= point.real >= 0 and width >= point.imag >= 0]
print('Locus in room:', locus_in_room)

locus_y = [point.real for point in locus_in_room]
locus_x = [point.imag for point in locus_in_room]

print('Locus y:', locus_y)
print('Locus x:', locus_x)

figure, axes = pyplot.subplots()
axes.plot(locus_x, locus_y)
axes.set(xlim=(0, width), ylim=(0, height))

axes.grid()

pyplot.show()

quit()