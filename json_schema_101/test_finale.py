from jsonschema import validate

# Funzione di esempio
def func(x):
    return x + 1

# Test per func
def test_func():
    assert func(3) == 4

# Schema JSON per la validazione
schema = {
    "type": "object",
    "properties": {
        "price": {"type": "number"},
        "name": {"type": "string"},
    },
    "required": ["name", "price"]
}

# Wrapper per la validazione JSON
def validate_wrapper(instance, schema):
    try:
        validate(instance=instance, schema=schema)
        return True
    except:
        return False

# Test per la validazione JSON
def test_validation_success():
    assert validate_wrapper({"name": "Eggs", "price": 34.99}, schema) == True

def test_validation_fail():
    assert validate_wrapper({"name": "Eggs", "price": "invalid"}, schema) == False

# Dati di esempio per test snapshot
sample_data = """frutti,prezzo,colore
pera,100,gialla
mela,10,verde
banana,20,gialla
arancia,60,arancione
papaya,40,rossa"""

# Test per snapshot della funzione func
def test_func_output_with_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'
    result = str(func(3))
    snapshot.assert_match(result, 'func_output.txt')

# Test per snapshot del file CSV
def test_csv_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'
    snapshot.assert_match(sample_data, 'frutti.csv')
