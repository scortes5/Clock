from PyQt5 import QtWidgets


class CircularSpinBox(QtWidgets.QSpinBox):
    def stepBy(self, steps):
        # Calculate the new value
        new_value = self.value() + steps
        
        # Wrap around if the value goes beyond minimum or maximum
        if new_value > self.maximum():
            new_value = self.minimum() + (new_value - self.maximum() - 1)
        elif new_value < self.minimum():
            new_value = self.maximum() - (self.minimum() - new_value - 1)
        
        self.setValue(new_value)
