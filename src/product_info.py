class ProductInfo:
    def __init__(self, protein: float, fats: float, carbo: float):
        self.protein = protein
        self.fats = fats
        self.carbo = carbo

    def __str__(self):
        return (
            "+---------- ИНФОРМАЦИЯ О ПРОДУКТЕ ----------+\n"
            f"Белки: {self.protein}\n"
            f"Жиры: {self.fats}\n"
            f"Углеводы: {self.carbo}\n"
            "+---------------------------------------+\n"
        )
