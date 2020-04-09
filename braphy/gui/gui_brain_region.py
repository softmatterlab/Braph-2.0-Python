import pyqtgraph.opengl as gl

class GUIBrainRegion(gl.GLMeshItem):
    def __init__(self, brain_region, size, selected, color, selected_color, ):
        self.brain_region = brain_region
        self.label = self.brain_region.label
        self.x = self.brain_region.x
        self.y = self.brain_region.y
        self.z = self.brain_region.z
        self.size = size
        self.color = color
        self.selected_color = selected_color
        meshdata = gl.MeshData.sphere(16, 16, radius=size)
        super().__init__(meshdata=meshdata, shader='shaded')
        self.set_selected(selected)
        self.translate(self.x, self.y, self.z)
        brain_region.add_observer(self.brain_region_changed)
        self.observers = []
        self.selected_observers = []

    def brain_region_changed(self):
        self.label = self.brain_region.label
        self.update_pos()
        self.notify_observers()

    def update_pos(self):
        dx = self.brain_region.x - self.x
        dy = self.brain_region.y - self.y
        dz = self.brain_region.z - self.z
        self.x += dx
        self.y += dy
        self.z += dz
        self.translate(dx, dy, dz)

    def add_observer(self, observer):
        self.observers.append(observer)

    def add_selected_observer(self, observer):
        self.selected_observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer()

    def notify_selected_observers(self):
        for observer in self.selected_observers:
            observer()

    def pos(self):
        return (self.x ,self.y, self.z)

    def toggle_selected(self):
        self.set_selected(not self.selected)
        self.notify_selected_observers()

    def set_selected(self, selected):
        self.selected = selected
        color = self.selected_color if selected else self.color
        self.setColor(color)

    def set_size(self, size):
        self.size = size
        meshdata = gl.MeshData.sphere(16, 16, radius=size)
        self.setMeshData(meshdata=meshdata)

    def set_color(self, color):
        self.color = color
        self.setColor(color)
