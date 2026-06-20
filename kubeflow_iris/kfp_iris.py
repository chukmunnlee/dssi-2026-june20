from kfp import dsl

# Loading
@dsl.component(base_image="python:3.12", packages_to_install=['scikit-learn'])
def load_iris_data(train_dataset: dsl.OutputPath("train_dataset")
                   , test_dataset: dsl.OutputPath("test_dataset")):
   from sklearn.datasets import load_iris
   from sklearn.model_selection import train_test_split
   import pickle

   iris_data = load_iris()

   X_data = iris_data.get('data')
   y_data = iris_data.get('target')

   X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.1)

   # pickle X_train, y_train, X_test, y_test
   with (open(train_dataset, 'wb')) as f:
      pickle.dump((X_train, y_train), f)

   with (open(test_dataset, 'wb')) as f:
      pickle.dump((X_test,y_test), f)

# Training
@dsl.component(base_image="python:3.12", packages_to_install=['scikit-learn'])
def train_model(train_dataset: dsl.InputPath('train_dataset')
                , model: dsl.OutputPath('model')):
   from sklearn import svm
   import pickle

   with (open(train_dataset, 'rb')) as f:
      #pickle.dump((X_train, y_train), f)
      X_train, y_train = pickle.load(f)

   # training in here, we write out the model

# Prediction

# Pipeline
@dsl.pipeline(name="Iris pipeline")
def iris_pipeline():
   load_step = load_iris_data()

   train_step = train_model(train_dataset=load_step.outputs['train_dataset'])

   # return the model accuracy
   print('Model accuracy: ', 0)