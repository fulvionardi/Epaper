# exec(open('my_script.py').read())

import pcbnew
import math

def draw_rectangular_coil(
    num_coils,
    thickness,
    corner_radius,
    start_x,
    start_y,
    width,
    height,
    spacing=1,
    layer=pcbnew.F_Cu
):
    board = pcbnew.GetBoard()
    step = thickness + spacing

    def add_segment(x1, y1, x2, y2):
        if abs(x1 - x2) < 1e-6 and abs(y1 - y2) < 1e-6:
            return  # skip zero-length segments
        line = pcbnew.PCB_SHAPE(board)
        line.SetShape(pcbnew.SHAPE_T_SEGMENT)
        line.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        line.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        line.SetLayer(layer)
        line.SetWidth(pcbnew.FromMM(thickness))
        board.Add(line)

    def add_arc(cx, cy, radius, start_angle_deg, end_angle_deg):
        arc = pcbnew.PCB_SHAPE(board)
        arc.SetShape(pcbnew.SHAPE_T_ARC)
        start_angle_rad = math.radians(start_angle_deg)
        sx = cx + radius * math.cos(start_angle_rad)
        sy = cy + radius * math.sin(start_angle_rad)
        mid_angle_rad = math.radians((start_angle_deg + end_angle_deg) / 2)
        mx = cx + radius * math.cos(mid_angle_rad)
        my = cy + radius * math.sin(mid_angle_rad)
        end_angle_rad = math.radians(end_angle_deg)
        ex = cx + radius * math.cos(end_angle_rad)
        ey = cy + radius * math.sin(end_angle_rad)
        arc.SetArcGeometry(
            pcbnew.VECTOR2I(pcbnew.FromMM(sx), pcbnew.FromMM(sy)),
            pcbnew.VECTOR2I(pcbnew.FromMM(mx), pcbnew.FromMM(my)),
            pcbnew.VECTOR2I(pcbnew.FromMM(ex), pcbnew.FromMM(ey)),
        )
        arc.SetLayer(layer)
        arc.SetWidth(pcbnew.FromMM(thickness))
        board.Add(arc)

    def add_arc_from_points(x1, y1, x2, y2, radius, clockwise=True):
        dx = x2 - x1
        dy = y2 - y1
        dist = math.sqrt(dx**2 + dy**2)

        if dist > 2 * radius:
            raise ValueError(f"Radius {radius} too small for distance {dist:.4f}. Need radius >= {dist/2:.4f}")

        # Midpoint between the two points
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2

        # Perpendicular distance from chord midpoint to circle center
        perp_dist = math.sqrt(max(0, radius**2 - (dist / 2)**2))

        # Perpendicular direction
        perp_x = -dy / dist
        perp_y =  dx / dist

        # Pick center based on direction
        if clockwise:
            cx = mx + perp_dist * perp_x
            cy = my + perp_dist * perp_y
        else:
            cx = mx - perp_dist * perp_x
            cy = my - perp_dist * perp_y

        # Angles from center to start and end points
        start_angle = math.atan2(y1 - cy, x1 - cx)
        end_angle   = math.atan2(y2 - cy, x2 - cx)

        # Force the short arc (< 180°)
        if clockwise:
            if end_angle > start_angle:
                end_angle -= 2 * math.pi
        else:
            if end_angle < start_angle:
                end_angle += 2 * math.pi

        mid_angle = (start_angle + end_angle) / 2

        # If still > 180°, flip to short side
        if abs(end_angle - start_angle) > math.pi:
            mid_angle += math.pi

        mid_x = cx + radius * math.cos(mid_angle)
        mid_y = cy + radius * math.sin(mid_angle)

        arc = pcbnew.PCB_SHAPE(board)
        arc.SetShape(pcbnew.SHAPE_T_ARC)
        arc.SetArcGeometry(
            pcbnew.VECTOR2I(pcbnew.FromMM(x1),    pcbnew.FromMM(y1)),
            pcbnew.VECTOR2I(pcbnew.FromMM(mid_x), pcbnew.FromMM(mid_y)),
            pcbnew.VECTOR2I(pcbnew.FromMM(x2),    pcbnew.FromMM(y2)),
        )
        arc.SetLayer(layer)
        arc.SetWidth(pcbnew.FromMM(thickness))
        board.Add(arc)

    for i in range(num_coils):
        #top
        #1: top-left
        #2: top-right
        x1 = start_x
        y1 = start_y - spacing * i - corner_radius
        x2 = start_x + width
        y2 = start_y - spacing * i - corner_radius

        add_segment(x1, y1, x2, y2)
    
        #right
        #3: top-right
        #4: bottom-right
        x3 = start_x + width + spacing * i + corner_radius
        y3 = start_y
        x4 = start_x + width + spacing * i + corner_radius
        y4 = start_y + height

        add_segment(x3, y3, x4, y4)
        add_arc_from_points(x2, y2, x3, y3, corner_radius + spacing * i)

        #bottom
        #5: bottom-left
        #6: bottom-right
        x5 = start_x - spacing
        y5 = start_y + height + spacing * i + corner_radius
        x6 = start_x + width
        y6 = start_y + height + spacing * i + corner_radius

        add_segment(x5, y5, x6, y6)
        add_arc_from_points(x4, y4, x6, y6, corner_radius + spacing * i)

        #left
        #7: top-left
        #8: bottom-left
        x7 = start_x - spacing * (i+1) - corner_radius
        y7 = start_y
        x8 = start_x - spacing * (i+1) - corner_radius
        y8 = start_y + height

        add_segment(x7, y7, x8, y8)
        add_arc_from_points(x5, y5, x8, y8, corner_radius + spacing * i)

        x9 = start_x
        y9 = start_y - spacing * (i + 1) - corner_radius

        add_arc_from_points(x7, y7, x9, y9, corner_radius + spacing * (i + 1))

    pcbnew.Refresh()


# --- Example usage ---
draw_rectangular_coil(
    num_coils=30,
    thickness=0.1,
    corner_radius=0.2,
    start_x=100,
    start_y=100,
    width=5,
    height=3,
    spacing=0.15,
    layer=pcbnew.F_Cu
)