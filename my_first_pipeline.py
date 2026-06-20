from kfp import dsl

# Create a component with Python 3.12 to run this function
# Python function must include types
@dsl.component(base_image="python:3.12")
def power(base: int, exponent: int) -> int:
   result: int = 1
   for _ in range(exponent):
      result = result * base 
   return result

# make this into a component
@dsl.component(base_image="python:3.12")
def randint(min: int, max: int) -> int:
   import random
   return random.randint(min, max)

@dsl.pipeline(name="my first pipeline", description="Frivolous pipeline")
def my_first_pipeline(low: int = 5, high: int = 10) -> int:
   # Must use keyword, not position argument passing
   # The return result is wrapped in an object
   _base = randint(min=low, max=high)
   _exponent = randint(min=low, max=high)
   print(_base)

   _result = power(base=_base.output, exponent=_exponent.output)

   return _result.output
