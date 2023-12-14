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
        # 0 - women, 1 - men
        # men -> 88.362 + (13.397 x weight in kg) + (4.799 x height in cm) - (5.677 x age in years)
        # women -> 447.593 + (9.247 x weight in kg) + (3.098 x height in cm) - (4.330 x age in years)
        if(self.gender == 0):
            return 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)

        elif(self.gender == 1):
            return 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)

        else:
            print("Gender not recognized")
    
    def calcActivityFactor(self):
        '''
        Sedentary (little to no exercise): 1.2
        Lightly active (light exercise/sports 1-3 days/week): 1.375
        Moderately active (moderate exercise/sports 3-5 days/week): 1.55
        Very active (hard exercise/sports 6-7 days/week): 1.725
        Super active (very hard exercise & physical job or training twice a day): 1.9
        '''

        physicalActTable = [1.2, 1.375, 1.375, 1.55, 1.55, 1.55, 1.725, 1.725, 1.9, 1.9, 1.9] # goes from 0 to 10
        return physicalActTable[self.physicalAct]

    # total daily energy expenditure
    def calcTDEE(self):
        # BMR x activity factor
        return self.calcBMR() * self.calcActivityFactor()

class Nutrient:
    def __init__(self, qty, unit):
        self.qty = qty
        self.unit = unit

    def compare(self, param):
        return round((param - self.qty), 3)

class EnergyPerDay(Nutrient):
    def __init__(self, qty, unit):
        super().__init__(qty, unit)

    def compWithDailyRec(self, tdee):
        return self.compare(tdee)

class LipidsPerDay(Nutrient):
    # daily lipids recommended per day is 30% of calories
    DAILY_RECOMMENDED = 0.3
    CONVERT_FACTOR = 9

    def __init__(self, qty, unit, calories):
        self.calories = calories
        super().__init__(qty, unit)
    
    def calcDailyRecPerKCAL(self):
        # calories * DAILY_RECOMMENDED
        cal_to_grams = self.convert_kcal_to_gram()
        return (cal_to_grams * self.DAILY_RECOMMENDED)

    def convert_kcal_to_gram(self):
        # calories / CONVERT_FACTOR
        return (self.calories / self.CONVERT_FACTOR)
    
    def compWithDailyRec(self):
        return self.compare(self.calcDailyRecPerKCAL())

class CarbonHidratsPerDay(Nutrient):
    # daily carbos recommended per day is 50% of calories
    DAILY_RECOMMENDED = 0.5
    CONVERT_FACTOR = 4

    def __init__(self, qty, unit, calories):
        self.calories = calories
        super().__init__(qty, unit)
    
    def calcDailyRecPerKCAL(self):
        # caloriesInGrams * DAILY_RECOMMENDED
        cal_to_grams = self.convert_kcal_to_gram()
        return (cal_to_grams * self.DAILY_RECOMMENDED)

    def convert_kcal_to_gram(self):
        # kcal / CONVERT_FACTOR
        return (self.calories / self.CONVERT_FACTOR)
    
    def compWithDailyRec(self):
        return self.compare(self.calcDailyRecPerKCAL())

class FiberPerDay(Nutrient):
    DAILY_RECOMMENDED = 30 # grams

    def __init__(self, qty, unit):
        super().__init__(qty, unit)

    def compWithDailyRec(self):
        return self.compare(self.DAILY_RECOMMENDED)

class ProteinPerDay(Nutrient):
    def __init__(self, qty, unit, weight, physicalAct):
        self.weight = weight
        self.physicalAct = physicalAct
        super().__init__(qty, unit)
    
    def calcActivityFactor(self):
        '''
        Sedentary/Lightly Active: 0.8 g/kg
        Moderate Activity: 1.0-1.2 g/kg
        High Activity: 1.2-1.7 g/kg
        '''
        physicalActTable = [0.8, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7] # goes from 0 to 10
        return physicalActTable[self.physicalAct]

    def calcDailyRecPerWeightAndAct(self):
        # proteinDailyRec = self.weight * self.calcActivityFactor()
        return self.weight * self.calcActivityFactor()
    
    def compWithDailyRec(self):
        return self.compare(self.calcDailyRecPerWeightAndAct())

class SaltPerDay(Nutrient):
    '''
    WHO (World Health Organization): recommends no more than 5g
    AHA (American Heart Association): recommends no more than 2.3g for most and 1.5g for heart risk persons
    '''
    DAILY_RECOMMENDED = 1.2 # grams

    def __init__(self, qty, unit):
        super().__init__(qty, unit)

    def compWithDailyRec(self):
        return self.compare(self.DAILY_RECOMMENDED)