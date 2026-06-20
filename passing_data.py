from kfp import dsl

@dsl.component(base_image="python:3.12")
def generate_data(payload: dsl.OutputPath("payload")):
   import random
   import pickle

   # this is the array
   data = []

   size = random.randint(50, 100)
   for _ in range(size):
      data.append(random.randint(0, 100))

   print('>>>> payload: ', payload)
   print('>>>>> generate_data: ', data)

   # open the OutputPath and serialize data
   with (open(payload, 'wb')) as f:
      pickle.dump(data, f)

   
@dsl.component(base_image="python:3.12")
def inspect_data(payload: dsl.InputPath("payload")):
   import pickle

   # open the InputPath and deserialize the object
   with (open(payload, 'rb')) as f:
      data = pickle.load(f)

   print('>>>> payload: ', payload)
   print('>>>>> inspect_data: ', data)

@dsl.pipeline(name = "passing_data")
def passing_data_pipeline(): 
   step1 = generate_data()
   print('>>>> step1: ', step1)

   step2 = inspect_data(payload=step1.outputs['payload'])
   print('>>>> step2: ', step2)