import drawSvg as draw

d = draw.Drawing(200, 100, origin='center', displayInline=False)

d.append(draw.Circle(-40, -10, 30, fill='none', stroke_width=2, stroke='black'))

d.saveSvg('example.svg')