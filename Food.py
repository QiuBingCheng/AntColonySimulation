from Element import Element


class Food(Element):
    def __init__(self, image, rect, capacity=50):
        super().__init__(image, rect)
        self.capacity = capacity
