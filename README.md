A command line utility for getting lunch data and nutrient information from the
Amica Smarthouse restaurant at Elektroniikkatie 8, Oulu.

Usage
-----

```
$ git clone git@github.com:koirikivi/amica-lunch.git
$ cd amica-lunch
$ pip install -r requirements.txt
$ python amica/lunch.py
Lunch options for Wednesday 2.9.
1. Lunch buffet
   Turkey and vegetables in coconut sauce
   Baltic herring patties
   Noodles
   Mashed potatoes
   Spinach mayonnaise
2. Just for you, lunch
   Chicken fillet filled with cheese and spinach
   Potato curry
   Yoghurt and pineapple sauce
3. Pizza buffet
   Chicken pan pizza seasoned with barbeque sauce
   Ham and pineapple pan pizza
4. Just for you, vegetable
   Pea crêpes
   Cottage cheese and herb filling for crêpes
5. Deli salad
   Shrimp and vegetable salad with herb and sour cream dressing
   Three onion soup with croutons
Dessert
   Yoghurt and orange smoothie
Get nutrients by entering index of menu (1-based): 2
2. Just for you, lunch
meal                                                         serv     kcal     prot      fat    carbs
Chicken fillet filled with cheese and spinach                100g      189     17,5     13,3      0,4
Potato curry                                                 100g      103      2,0      1,8     19,1
Yoghurt and pineapple sauce                                  100g       92      2,5      5,8      7,8
```

Exit with Ctrl-C :P

TODO
----

- Support for other restaurants that support the Amica API
- Exit more gracefully than with Ctrl-C
