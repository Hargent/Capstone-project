from pprint import pprint
import inquirer
import math
import matplotlib.pyplot as plt

choices = [{
    "name": "Input parameters",
    "value": 1
}, {
    "name": "Simulate wells",
    "value": 2
}, {
    "name": "Analyze production",
    "value": 3
}, {
    "name": "Visualize results",
    "value": 4
}, {
    "name": "Exit",
    "value": 5
}]

# operation
# well data
# decline rate
# production rate
# production time

# function for getting which operation
# function to take input
# functiom to analyze production
# function to visualize results
# function to simulate wells
# function to exit


def get_operation(choices,message):
  operations = [
      inquirer.List(
          "Operation",
          message,
          choices=[choice["name"] for choice in choices],
      ),
  ]
  answers = inquirer.prompt(operations)
  # pprint(answers)

  if answers:
    option = list(filter(lambda x: x["name"] == answers["Operation"], choices)),answers["Operation"]
    
    return option[0][0]["value"] or 1 
  else:
    return 1
def get_confirmation(message):
  confirm = [
      inquirer.List(
          "confirm",
          message,
          choices=["Yes","No"],
      ),
  ]
  answers = inquirer.prompt(confirm)
  # pprint(answers)

  if answers:
    return answers['confirm'] == "Yes"
  else:
    return False

def get_inputs(wells=[],message="Enter the number of wells to save: "):
  # Prompt the user to input the number of wells
  while True:
      try:
          no_of_wells = int(input(message))
          if(no_of_wells<0) :
            raise ValueError("Number of wells cannot be less than 0")
          break
      except ValueError as err:
          print(f"{err}\nPlease enter a valid number.")


  # Get details for all wells
  for i in range(1, no_of_wells + 1):
    well ={}
    print(f"\nDetails for Well {i}:")
    well["name"] = input("Enter well name: ")
    
    # Prompt user for production rate with error handling
    while True:
        try:
          production_rate = float(input("Enter initial production rate (in bbl/day): "))
          if(production_rate<0) :
            raise ValueError("production rate cannot be less than 0")
          well["production_rate"] = production_rate
          break
        except ValueError as err:
            print(f"{err}\nPlease enter a valid number for initial production rate.")

    # Prompt user for decline rate with error handling
    while True:
        try:
            decline_rate = float(input("Enter decline rate (percentage): "))
            if(decline_rate<0) :
              raise ValueError("Rate cannot be less than 0")
            if(decline_rate>100) :
              raise ValueError("Rate cannot be greater than 100")
            well["decline_rate"] = decline_rate
            break
        except ValueError as err:
            print(f"{err}\nPlease enter a valid number for decline rate.")
    # Prompt user for time with error handling
    while True:
        try:
            time = float(input("Enter the time (years): "))
            if(time<0) :
              raise ValueError("Time cannot be negative")
            well["time"] = time
            break
        except ValueError as err:
            print(f"{err}\nPlease enter a valid number for time.")


    wells.append(well)
  return wells
def arp_model(initial_prod_rate,decline_rate,time):

  prod = initial_prod_rate*(math.e**(-(decline_rate/100)*time))
  return "{:.2f}".format(prod)
  
def run_simulaton(wells):
  print("Simulating wells...")
  prod_rate = []
  for well in wells:
    prod_rate.append({
      **well,
      "arp_production_rate":arp_model(well["production_rate"],well["decline_rate"],well["time"])
    })

  return prod_rate
  
def run_analysis(wells):
  calc_recovery_factor =get_confirmation(f"Do you want to calculate the oil recovery factor?")
  total_oil_in_place=1
  if calc_recovery_factor:
    while True:
      try:
          oil_in_place = float(input("Enter the total oil in place: "))
          if(oil_in_place<0) :
            raise ValueError("Total oil in place cannot be negative")
          elif oil_in_place ==0:
            total_oil_in_place=1
          else:
            total_oil_in_place=oil_in_place
          break
      except ValueError as err:
          print(f"{err}\nPlease enter a valid number for total oil in place.")
  print(f"Total oil in place: {total_oil_in_place}")
  analysis = {
    "wells":wells
  }
  
  cummulative_prod_rate = sum([int(well["production_rate"]) for well in wells])
  print(f"The cummulative production rate is {cummulative_prod_rate}")
  average_prod_rate= cummulative_prod_rate/len(wells)
  print(f"The average production rate is {average_prod_rate}")
  if calc_recovery_factor:
    recovery_factor = cummulative_prod_rate/total_oil_in_place
    print(f"The recovery factor is {recovery_factor}")
    analysis["analysis"]={ "cummulative_prod_rate":cummulative_prod_rate,
      "average_prod_rate":average_prod_rate,
      "recovery_factor":recovery_factor
    }
    return analysis
  else:
    analysis["analysis"]={ "cummulative_prod_rate":cummulative_prod_rate,
                         "average_prod_rate":average_prod_rate}
    return analysis

def visualize_results(wells):
  # print([well("name") for well in wells])
  production_rate=[well["production_rate"] for well in wells]
  time =[well["time"] for well in wells]
  plt.figure(figsize=(7,5))
  plt.plot(time, production_rate, marker='8', color = 'g',label = 'Production rate versus Time')
  
  plt.xlabel('Time')
  plt.ylabel('Production Rate')
  # plt.title("Production decline for one year")
  plt.legend()
  plt.grid()
  plt.show()
  return true


def check_wells_before_execution(wells,function,message):
  result = wells
  if len(wells)>0:
    is_new_wells = get_confirmation(message="Do you want to use the existing wells?")
    if is_new_wells:
      result=function(wells)
    else:
      wells = get_inputs(wells,message)
      result=function(wells)
  else:
    wells = get_inputs(wells,message)
    result=function(wells)

  return result

def Simulator(wells=[],choices=choices,message="What operation do you want to carry out?"):
  # wells = []
# get operation
  operation = get_operation(choices,message)
 
  # Exit if operation is 5
  if operation == 5:
    is_confirmed =get_confirmation(message="Do you want to exit the simulator?")

    if is_confirmed:
      print("Simulator closed!")
      return
    else:
      Simulator(wells,choices,message=f"What do you want to do ? ")
      
      
  # Input parameters if operation is 1
  if operation == 1:
    print("Input parameters")   
    wells = get_inputs(wells)
    Simulator(wells,choices,message=f"You have saved {len(wells)} parameters, what do you want to do ? ")
  # Simulate wells if operation is 2
  if operation == 2:
    print("Simulate wells")
    
    simulation_result =check_wells_before_execution(wells,run_simulaton,message="Enter the number of wells to simulate: ")
    print(simulation_result)
    Simulator(wells,choices,message=f"Simulation Complete, what do you want to do ? ")
    
  # Analyze production if operation is 3
  if operation == 3:
    print("Analyze production")
    analysis_result=check_wells_before_execution(wells,run_analysis,message="Enter the number of wells to analyse: ")
    print(analysis_result)
    Simulator(wells,choices,message=f"Analysis complete, what do you want to do ? ")
    
  # Visualize results if operation is 4
  if operation == 4:
    print("Visualize results")
    analysis_result=check_wells_before_execution(wells,visualize_results,message="Enter the number of wells to visualize: ")
    Simulator(wells,choices,message=f"Visualization complete, what do you want to do ? ")

try:
  
  Simulator()
except KeyboardInterrupt:
  print("\nKeyboard Interrupt detected. Exiting program...")