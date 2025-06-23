# render2d.py
from vispy import scene, app
from visualiser.colour_maps import get_colormap, available_maps
import numpy as np

class TrussViewer(scene.SceneCanvas):
    def __init__(self, data, scale=1.0, field_name='scalar', cmap='bwr'):
        super().__init__(keys='interactive', show=True)
        self.unfreeze()

        self.scale      = scale
        self.data       = data
        self.field_name = field_name

        if cmap not in available_maps():
            raise ValueError(f"Invalid cmap '{cmap}'. Valid options: {available_maps()}")
        self.cmap_name = cmap

        self.view = self.central_widget.add_view()
        self.view.camera = 'panzoom'
        self.view.camera.aspect = 1

        self.deformed_visual = None

        self.draw_undeformed()
        self.draw_deformed()            # always created (but hidden)
        self.deformed_visual.visible = False

        self.draw_supports()

        self.view.camera.set_range()
        self.freeze()

    def draw_undeformed(self):
        lines = []
        for n1, n2 in self.data.elements:
            lines.append(self.data.nodes[[n1, n2], :])
        lines = np.array(lines).reshape(-1, 2)
        scene.visuals.Line(
            pos=lines,
            color='lightgray',
            width=1,
            connect='segments',
            parent=self.view.scene
        )

    def draw_deformed(self):
        cmap    = get_colormap(self.cmap_name)
        max_val = np.max(np.abs(self.data.scalar_field))

        lines  = []
        colors = []

        for i, (n1, n2) in enumerate(self.data.elements):
            u  = self.data.displacements
            x1 = self.data.nodes[n1] + u[n1*2:n1*2+2] * self.scale
            x2 = self.data.nodes[n2] + u[n2*2:n2*2+2] * self.scale
            lines.extend([x1, x2])

            val = self.data.scalar_field[i] / max_val
            c   = cmap.map(val)[0, :3]
            colors.extend([c, c])

        pos         = np.array(lines)
        color_array = np.array(colors)

        self.deformed_visual = scene.visuals.Line(
            pos=pos,
            color=color_array,
            width=2.0,
            connect='segments',
            parent=self.view.scene
        )

    def draw_supports(self):
        for nid, (fx, fy) in self.data.bc_flags.items():
            node = self.data.nodes[nid]
            glyphs = []
            if fx:
                glyphs.append(node + [-0.05, 0])
            if fy:
                glyphs.append(node + [0, -0.05])
            for g in glyphs:
                scene.visuals.Markers(
                    pos=np.array([g]),
                    face_color='black',
                    symbol='triangle_down',
                    size=10,
                    parent=self.view.scene
                )

    def on_key_press(self, event):
        key = event.key.name.lower()
        if key == 'd' and self.deformed_visual:
            self.deformed_visual.visible = not self.deformed_visual.visible
        elif key == 'r':
            self.view.camera.set_range()
        elif key == 'c':
            # cycle through available colormaps
            idx = available_maps().index(self.cmap_name)
            self.cmap_name = available_maps()[(idx + 1) % len(available_maps())]
            # redraw deformed with new cmap
            self.deformed_visual.parent = None
            self.draw_deformed()
            self.deformed_visual.visible = True

if __name__ == '__main__':
    import numpy as _np
    from visualiser.mesh_adapter import VisualData
    from visualiser.viewer_app import launch_viewer

    # example usage
    nodes       = _np.array([[0,0],[1,1],[2,0]])
    elements    = [(0,1),(1,2),(0,2)]
    displ       = _np.array([0,0,0.02,0,0.01,-0.01])
    scalar      = _np.array([100.0, 50.0, -75.0])
    bc_flags    = {0: (True, True)}

    data = VisualData(nodes, elements, displ, scalar, bc_flags)
    viewer = TrussViewer(data, scale=10.0, cmap='bwr')
    app.run()
