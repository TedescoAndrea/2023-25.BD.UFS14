from jsonschema import validate

#primo test
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4

#secondo test
schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },
}

def test_validation_success():
   assert validate_wrapper(instance={"name" : "Eggs", "price" : 34.99}, schema=schema) == True

def test_validation_fail():
    assert validate_wrapper(instance={"name" : "Eggs", "price" : "invalid"}, schema=schema,) == False
def validate_wrapper(instance, schema):
    try:
        validate(instance = instance, schema = schema)
        return True
    except:
        return False
    

def test_function_output_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'  # This line is optional.
    x = str(func(3))
    snapshot.assert_match(x, 'foo_output.txt')    

a = """frutti,prezzo,colore
pera,100,gialla
mela,10,verde
banana,20,gialla
arancia,60,arancione
papaya,40,rossa"""

def test_function_output_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'  # This line is optional.
    x = a
    snapshot.assert_match(x, 'frutti.csv')  