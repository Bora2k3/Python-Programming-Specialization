# Неправильно
class AllScoresCalculator:
    def calculate_accuracy(self, y_true, y_pred):
        return sum(int(x == y) for x, y in zip(y_true, y_pred)) / len(y_true)

    def log_loss(self, y_true, y_pred):
        return sum((x * math.log(y) + (1 - x) * math.log(1 - y))
                   for x, y in zip(y_true, y_pred)) / len(y_true)


# Правильно
class CalculateLosses:
    def log_loss(self, y_true, y_pred):
        return sum((x * math.log(y) + (1 - x) * math.log(1 - y))
                   for x, y in zip(y_true, y_pred)) / len(y_true)


class CalculateMetrics:
    def calculate_accuracy(self, y_true, y_pred):
        return sum(int(x == y) for x, y in zip(y_true, y_pred)) / len(y_true)
