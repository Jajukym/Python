import xlwt
import xlrd
import random
from os import path

# Open Meals.xlsx to get data for meals
mealsBook = xlrd.open_workbook("C:\Python27\MyScripts\Meals.xlsx") #Change this path to the path of your Meals.xlsx
fullMealsSheet = mealsBook.sheet_by_name('Full Meals')
mainDishesSheet = mealsBook.sheet_by_name('Main Dishes')
sideDishesSheet = mealsBook.sheet_by_name('Side Dishes')

# List Initialization from Spreadsheet
fullMeals = [] 
for row_index in xrange(1, fullMealsSheet.nrows):
	fullMeals.append(fullMealsSheet.cell(row_index, 0).value) # Get column 0

fullMealIngredients = [] 
for row_index in xrange(1, fullMealsSheet.nrows):
	fullMealIngredients.append(fullMealsSheet.cell(row_index, 1).value) # Get column 1

mainDishes = [] 
for row_index in xrange(1, mainDishesSheet.nrows):
	mainDishes.append(mainDishesSheet.cell(row_index, 0).value)

mainDishIngredients = [] 
for row_index in xrange(1, mainDishesSheet.nrows):
	mainDishIngredients.append(mainDishesSheet.cell(row_index, 1).value)

sideDishes = [] 
for row_index in xrange(1, sideDishesSheet.nrows):
	sideDishes.append(sideDishesSheet.cell(row_index, 0).value)

sideDishIngredients = [] 
for row_index in xrange(1, sideDishesSheet.nrows):
	sideDishIngredients.append(sideDishesSheet.cell(row_index, 1).value)

mealNum = 10
n=1

# Welcome user and get input
print 'Welcome to Meal Planner!'
mealNum = input('How many meals do you want to create?  ')

# Create workbook and add sheet
book = xlwt.Workbook(encoding="utf-8")
sh = book.add_sheet("Meals")
sh.write(0, 0, "Meal")
sh.write(0, 1, "Ingredients")

# Get List Lengths
fullMealNum = len(fullMeals)-1
mainDishNum = len(mainDishes)-1
sideDishNum = len(sideDishes)-1

# Get random meals and add them to the spreadsheet
for meals in range(mealNum):
	# Full meal or main dish with side dish?
	mealType = random.randint(0,1)
	# Full meal
	if mealType == 0:
		randomFullMeal = random.randint(0,fullMealNum)
		sh.write(n, 0, fullMeals[randomFullMeal])
		sh.write(n, 1, fullMealIngredients[randomFullMeal])
	# Main dish with side dish
	if mealType == 1:
		randomMainDish = random.randint(0,mainDishNum)
		randomSideDish = random.randint(0,sideDishNum)
		randomDish = mainDishes[randomMainDish] + " and " + sideDishes[randomSideDish]
		randomDishIngredients = mainDishIngredients[randomMainDish] + ", " + sideDishIngredients[randomSideDish]
		sh.write(n, 0, randomDish)
		sh.write(n, 1, randomDishIngredients)
	n = n+1

# Save the workbook
book.save("MealPlan.xls")
print 'MealPlan.xls has been created with %d random meals!' %mealNum
