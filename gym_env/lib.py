# Nutrition recommended consumption
class NRC:
    def __init__(self, age, gender, weight, height, physicalAct):
        self.age = age # years
        self.gender = gender # int 0, 1
        self.weight = weight # kg
        self.height = height # must be converted into cm
        self.physicalAct = physicalAct # int from 0 to 10

    # basal metabolic rate (using Harris-Benedict equation)
    def calcBMR(self):
        # men -> 88.362 + (13.397 x weight in kg) + (4.799 x height in cm) - (5.677 x age in years)
        # women -> 447.593 + (9.247 x weight in kg) + (3.098 x height in cm) - (4.330 x age in years)
        pass
    
    def calcActivityFactor(self):
        '''
        Sedentary (little to no exercise): BMR x 1.2
        Lightly active (light exercise/sports 1-3 days/week): BMR x 1.375
        Moderately active (moderate exercise/sports 3-5 days/week): BMR x 1.55
        Very active (hard exercise/sports 6-7 days/week): BMR x 1.725
        Super active (very hard exercise & physical job or training twice a day): BMR x 1.9
        '''
        pass

    # total daily energy expenditure
    def calcTDEE(self):
        # BMR x activity factor
        pass

class Nutrient:
    def __init__(self, qty, unit):
        self.qty = qty
        self.unit = unit

    def compare(self, param):
        # self.qty with param
        pass

class EnergyPerDay(Nutrient):
    def __init__(self, qty, unit):
        super().__init__(self, qty, unit)

    def compWithDailyRec(self, tdee):
        self.compare(tdee)

class LipidsPerDay(Nutrient):
    # daily lipids recommended per day is 30% of calories
    DAILY_RECOMMENDED = 0.3
    CONVERT_FACTOR = 9

    def __init__(self, qty, unit, calories):
        self.calories = calories
        super().__init__(self, qty, unit)
    
    def calcDailyRecPerKCAL(self):
        # calories * DAILY_RECOMMENDED
        pass

    def convert_kcal_to_gram(self, kcal):
        # kcal / CONVERT_FACTOR
        pass
    
    def compWithDailyRec(self):
        self.compare(self.convert_kcal_to_gram(self.calcDailyRecPerKCAL()))

class CarbonHidratsPerDay(Nutrient):
    DAILY_RECOMMENDED = 0.5
    CONVERT_FACTOR = 4

    def __init__(self, qty, unit):
        self.calories = calories
        super().__init__(self, qty, unit)
    
    def calcDailyRecPerKCAL(self):
        # calories * DAILY_RECOMMENDED
        pass

    def convert_kcal_to_gram(self, kcal):
        # kcal / CONVERT_FACTOR
        pass
    
    def compWithDailyRec(self):
        self.compare(self.convert_kcal_to_gram(self.calcDailyRecPerKCAL()))

class FiberPerDay(Nutrient):
    DAILY_RECOMMENDED = 30 # grams

    def __init__(self, qty, unit):
        super().__init__(self, qty, unit)

    def compWithDailyRec(self):
        self.compare(DAILY_RECOMMENDED)

class ProteinPerDay(Nutrient):
    def __init__(self, qty, unit):
        self.weight = weight
        self.physicalAct = physicalAct
        super().__init__(self, qty, unit)
    
    def calcActivityFactor(self, physicalAct):
        '''
        Sedentary/Lightly Active: 0.8 g/kg
        Moderate Activity: 1.0-1.2 g/kg
        High Activity: 1.2-1.7 g/kg
        '''
        pass

    def calcDailyRecPerWeightAndAct(self, weight):
        # proteinDailyRec = self.weight * self.calcActivityFactor()
        pass
    
    def compWithDailyRec(self, proteinDailyRec):
        self.compare(proteinDailyRec)

class SaltPerDay(Nutrient):
    '''
    WHO (World Health Organization): recommends no more than 5g
    AHA (American Heart Association): recommends no more than 2.3g for most and 1.5g for heart risk persons
    '''
    DAILY_RECOMMENDED = 1.2 # grams

    def __init__(self, qty, unit):
        super().__init__(self, qty, unit)

    def compWithDailyRec(self):
        self.compare(DAILY_RECOMMENDED)